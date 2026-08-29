# ---------------------------------------------------------------------------
# Cover-lane sneak — one self-contained sneak level (Ren'Py 8).
#
#     jump cover_lane
#
# Does not patch follower_controller.rpy. This screen is the gameplay.
#
# HOW TO FORK A NEW LEVEL
#   - Copy this file to game/scripts/stealth/<new>_lane.rpy
#   - Rename prefixes so Ren'Py does not clash:
#       cover_lane -> your name, COVER_LANE_ -> yours, cl_ / _cl_ -> yours,
#       cover_lane_crouched, labels cover_lane / _caught / _clear,
#       screen cover_lane_scene, Character, image names.
#   - Add a HUD debug button next to Cover lane in game/scripts/utils/hud.rpy:
#       textbutton "...": action Jump("<your_label>")
#   - Keep `default` names unique or two levels will share crouched/x/pacer.
#   - NEVER name an init-python loop variable `_p` (shadows Ren'Py `_p()`
#     and crashes `gui.about`).
#   - NEVER put `background` on a `viewport` (Ren'Py 8.5 error). Viewports
#     are already transparent.
#
# LOGIC SPACE
#   Author x/y/w/h in 1280x800. cl_x/cl_y/cl_w/cl_h scale to 1920x1080.
#   Player x is the sprite CENTRE. Cover x is the LEFT edge.
#   Feet plant at COVER_LANE_STREET_Y (yanchor 1.0).
#
# OPENINGS LIST  COVER_LANE_OPENINGS
#   id     unique string
#   kind   window — crouch hides, even while moving
#          door   — crouch does NOT hide; time the pacer or stop behind
#                   layer=behind cover
#   x,y,w,h  building-space rect. Windows ~h 252 with a sill. Doors taller
#            (~h 332) down toward the plinth, no high sill.
#   npc    sentry = always watching
#          pacer  = watching only while their body overlaps this rect
#          None   = never watches
#   Caught if player x-range overlaps this rect AND npc is watching AND
#   player is not hidden.
#   Hidden if (a) kind=window AND crouched, OR (b) stopped AND x overlaps
#   a cover prop with layer `behind`.
#   Front-layer props never hide you.
#   120 ms grace is applied in cover_lane_advance only (not in unit tests).
#   Clear when player_x >= COVER_LANE_CLEAR_X and not caught.
#
# COVER LIST  COVER_LANE_COVER
#   id, kind (`dumpster`/`planter`/`crate`/`bin` — kind only picks art in
#   cl_cover_child; add a branch there for new art)
#   x, w, h (no y; planted on STREET_Y)
#   layer  `behind` = between building and player, grants hide when stopped
#          `front`  = after player, visual only
#   Missing layer defaults to behind.
#
# PAINT ORDER IS Z-ORDER (later = in front). Screen comments numbered 1-9:
#   1 bg, 2 interiors, 3 NPC viewports, 4 glass, 5 watch bands,
#   6 click/dest, 7 behind props, 8 player, 9 front items + HUD
#
# PACER
#   COVER_LANE_PACER_MIN_X/MAX_X is the ledge they walk. They watch the
#   opening whose npc is `pacer` only while overlapping it. Blind brick
#   to the right of B is the timing window.
#
# COPY-THESE-BLOCKS FOR A NEW LAYOUT
#   A new level is usually just editing OPENINGS, COVER, PACER min/max,
#   START_X/CLEAR_X, and the screen's hardcoded COVER_LANE_OPENINGS[0]/[1]/[2]
#   sentry/pacer/empty wiring (if you add a 4th opening you must add
#   frame/glass/viewport rows).
# ---------------------------------------------------------------------------

default cover_lane_crouched = False
default cover_lane_player_x = 86.0
default cover_lane_dest_x = 86.0
default cover_lane_facing = 1
default cover_lane_moving = False
default cover_lane_walk_t = 0.0
default cover_lane_pacer_x = 570.0
default cover_lane_pacer_dir = 1
default cover_lane_outcome = None


define cover_lane_voice = Character("Voice from the window", color="#c9a066")


# Named RF android art. Shown only when loadable; Solids are the fallback so
# this file still runs if the example images are not on disk yet.
image cl_android_stand = "RF/example images/android/body/stand/h/0.png"
image cl_android_walk:
    "RF/example images/android/body/walk/h/0.png"
    pause 0.12
    "RF/example images/android/body/walk/h/1.png"
    pause 0.12
    "RF/example images/android/body/walk/h/2.png"
    pause 0.12
    "RF/example images/android/body/walk/h/3.png"
    pause 0.12
    repeat
image cl_android_walk_0 = "RF/example images/android/body/walk/h/0.png"
image cl_android_walk_1 = "RF/example images/android/body/walk/h/1.png"
image cl_android_walk_2 = "RF/example images/android/body/walk/h/2.png"
image cl_android_walk_3 = "RF/example images/android/body/walk/h/3.png"


init python:
    import os
    import sys
    import time

    # Logic space 1280x800, drawn at 1920x1080 via cl_x/cl_y/cl_w/cl_h.
    # Player x = sprite CENTRE; cover x = LEFT edge; feet at STREET_Y (yanchor 1.0).
    CL_VIEW_W = 1920
    CL_VIEW_H = 1080
    CL_LOGIC_W = 1280.0
    CL_LOGIC_H = 800.0
    CL_SCALE_X = CL_VIEW_W / CL_LOGIC_W
    CL_SCALE_Y = CL_VIEW_H / CL_LOGIC_H

    COVER_LANE_PLAYER_W = 36
    COVER_LANE_PLAYER_H = 78
    COVER_LANE_START_X = 86
    COVER_LANE_CLEAR_X = 1188
    COVER_LANE_STREET_Y = 552
    COVER_LANE_STAND_SPEED = 180.0
    COVER_LANE_CROUCH_SPEED_MULT = 0.45
    COVER_LANE_CROUCH_SCALE_Y = 0.62
    COVER_LANE_GRACE_MS = 120
    COVER_LANE_PATH_MIN = 64.0
    COVER_LANE_PATH_MAX = 1216.0
    COVER_LANE_CLICK_Y = 416.0

    # Pacer ledge: MIN_X/MAX_X is the walk range (door B + blind brick to its
    # right). They watch the opening whose npc is "pacer" only while overlapping
    # it. Blind brick to the right of B is the timing window to cross the door.
    COVER_LANE_PACER_W = 44
    COVER_LANE_PACER_H = 98
    COVER_LANE_PACER_Y = 330
    COVER_LANE_PACER_MIN_X = 490.0
    COVER_LANE_PACER_MAX_X = 762.0
    COVER_LANE_PACER_SPEED = 52.0

    # Openings: id, kind (window|door), x/y/w/h in 1280x800, npc (sentry|pacer|None).
    # Window: crouch hides even while moving. Door: crouch does not; time pacer
    # or stop behind layer=behind cover. Caught = x-overlap + watching + not hidden.
    # Hidden = (window AND crouched) OR (stopped AND behind-cover overlap).
    # Clear at COVER_LANE_CLEAR_X if not caught. Grace is in cover_lane_advance only.
    COVER_LANE_OPENINGS = [
        {"id": "A", "kind": "window", "x": 132, "y": 96, "w": 200, "h": 252, "npc": "sentry"},
        {"id": "B", "kind": "door", "x": 478, "y": 96, "w": 200, "h": 332, "npc": "pacer"},
        {"id": "C", "kind": "window", "x": 824, "y": 96, "w": 200, "h": 252, "npc": None},
    ]

    # Cover props: id, kind (art only — dumpster/planter/crate/bin), x/w/h, layer.
    # No y; planted on STREET_Y. x is LEFT edge. layer behind grants hide when
    # stopped; front is visual only. Missing layer defaults to behind.
    COVER_LANE_COVER = [
        {"id": "crate", "kind": "crate", "x": 72, "w": 28, "h": 32, "layer": "front"},
        {"id": "planter", "kind": "planter", "x": 356, "w": 50, "h": 56, "layer": "behind"},
        {"id": "dumpster", "kind": "dumpster", "x": 608, "w": 80, "h": 70, "layer": "behind"},
    ]

    CL_STAND_PATH = "RF/example images/android/body/stand/h/0.png"
    CL_WALK_PATHS = [
        "RF/example images/android/body/walk/h/0.png",
        "RF/example images/android/body/walk/h/1.png",
        "RF/example images/android/body/walk/h/2.png",
        "RF/example images/android/body/walk/h/3.png",
    ]

    _cl_stealth_mod = None
    try:
        _cl_root = os.path.abspath(os.path.join(renpy.config.gamedir, ".."))
        if _cl_root not in sys.path:
            sys.path.append(_cl_root)
        import cover_lane as _cl_stealth_mod
    except Exception:
        _cl_stealth_mod = None

    _cl_last_t = [None]
    _cl_grace_ms = [0.0]
    _cl_bg_cache = [None]
    _cl_art_cache = [None]

    def cl_x(x):
        return int(round(float(x) * CL_SCALE_X))

    def cl_y(y):
        return int(round(float(y) * CL_SCALE_Y))

    def cl_w(w):
        return max(1, int(round(float(w) * CL_SCALE_X)))

    def cl_h(h):
        return max(1, int(round(float(h) * CL_SCALE_Y)))

    def cl_player_art_loaded():
        if _cl_art_cache[0] is None:
            try:
                _cl_art_cache[0] = bool(renpy.loadable(CL_STAND_PATH))
            except Exception:
                _cl_art_cache[0] = False
        return _cl_art_cache[0]

    def cl_walk_paths_loaded():
        paths = []
        for path in CL_WALK_PATHS:
            try:
                if renpy.loadable(path):
                    paths.append(path)
            except Exception:
                pass
        return paths

    def _cover_lane_now():
        try:
            return renpy.get_game_runtime()
        except Exception:
            return time.time()

    def _cl_rects_overlap(a, b):
        return (
            a["x"] < b["x"] + b["w"]
            and b["x"] < a["x"] + a["w"]
            and a["y"] < b["y"] + b["h"]
            and b["y"] < a["y"] + a["h"]
        )

    def cover_lane_pacer_rect():
        return {
            "x": float(renpy.store.cover_lane_pacer_x),
            "y": COVER_LANE_PACER_Y,
            "w": COVER_LANE_PACER_W,
            "h": COVER_LANE_PACER_H,
        }

    def cover_lane_npc_watching(window, pacer_rect=None):
        """Sentry always watches. Pacer watches iff their body overlaps that window. Empty never."""
        kind = window.get("npc")
        if kind == "sentry":
            return True
        if kind == "pacer":
            if pacer_rect is None:
                pacer_rect = cover_lane_pacer_rect()
            return _cl_rects_overlap(pacer_rect, window)
        return False

    def _cl_player_overlaps_window(player_x, window, player_w=COVER_LANE_PLAYER_W):
        half = player_w * 0.5
        return (player_x - half) < (window["x"] + window["w"]) and window["x"] < (player_x + half)

    def _cl_player_overlaps_cover(player_x, cover, player_w=COVER_LANE_PLAYER_W):
        half = player_w * 0.5
        return (player_x - half) < (cover["x"] + cover["w"]) and cover["x"] < (player_x + half)

    # Detection in one place. Instant overlap — no grace. Hidden if stopped
    # on behind-cover, or crouched at a window. Front props never hide.
    # cover_lane_advance adds the 120 ms grace on top of this; tests do not.
    def cl_cover_layer(cover):
        """behind = hide-behind; front = visual only.

        Missing/unknown defaults to behind so the old hide list and tests
        without a layer key still grant cover. New objects should set layer.
        """
        layer = cover.get("layer")
        if layer == "front":
            return "front"
        return "behind"

    def _cl_player_in_cover(player_x, moving, cover=None, player_w=COVER_LANE_PLAYER_W):
        """Stopped + overlap a behind prop. Front items never hide.

        Detection uses layer == "behind" only; missing is treated as behind.
        """
        if moving:
            return False
        cover = COVER_LANE_COVER if cover is None else cover
        for item in cover:
            layer = item.get("layer")
            if layer is not None and layer != "behind":
                continue
            if _cl_player_overlaps_cover(player_x, item, player_w=player_w):
                return True
        return False

    def _cl_hidden_from_opening(opening, crouched, in_cover):
        if in_cover:
            return True
        if opening.get("kind", "window") == "window" and crouched:
            return True
        return False

    def cover_lane_rules_tick(player_x, crouched, pacer_rect=None, windows=None, player_w=COVER_LANE_PLAYER_W, clear_x=COVER_LANE_CLEAR_X, moving=False, cover=None):
        """Instant overlap check — same rules as cover_lane.cover_lane_tick."""
        windows = COVER_LANE_OPENINGS if windows is None else windows
        cover = COVER_LANE_COVER if cover is None else cover
        if _cl_stealth_mod is not None:
            return _cl_stealth_mod.cover_lane_tick(
                player_x,
                crouched,
                windows=windows,
                pacer_rect=pacer_rect,
                player_w=player_w,
                clear_x=clear_x,
                moving=moving,
                cover=cover,
            )
        in_cover = _cl_player_in_cover(player_x, moving, cover=cover, player_w=player_w)
        for window in windows:
            if _cl_player_overlaps_window(player_x, window, player_w=player_w):
                if cover_lane_npc_watching(window, pacer_rect) and not _cl_hidden_from_opening(window, crouched, in_cover):
                    return "caught"
        if player_x >= clear_x:
            return "clear"
        return None

    def _cl_update_pacer(dt):
        x = float(renpy.store.cover_lane_pacer_x)
        d = 1 if int(renpy.store.cover_lane_pacer_dir) >= 0 else -1
        x += d * COVER_LANE_PACER_SPEED * dt
        if x <= COVER_LANE_PACER_MIN_X:
            x = COVER_LANE_PACER_MIN_X
            d = 1
        elif x >= COVER_LANE_PACER_MAX_X:
            x = COVER_LANE_PACER_MAX_X
            d = -1
        renpy.store.cover_lane_pacer_x = x
        renpy.store.cover_lane_pacer_dir = d

    def cover_lane_pacer_watching():
        win_b = COVER_LANE_OPENINGS[1]
        return cover_lane_npc_watching(win_b, cover_lane_pacer_rect())

    def cover_lane_window_watching(window):
        return cover_lane_npc_watching(window, cover_lane_pacer_rect())

    def cover_lane_toggle_crouch():
        """Flip crouched. Speed is applied in cover_lane_advance (no Follower)."""
        renpy.store.cover_lane_crouched = not bool(renpy.store.cover_lane_crouched)

    def cover_lane_hide_overworld():
        for name in ("rf_map", "test_world", "editor_world", "hud", "player_menu"):
            try:
                renpy.hide_screen(name)
            except Exception:
                pass

    def cover_lane_reset():
        """Reset crouched, positions, pacer, and detection grace."""
        renpy.store.cover_lane_crouched = False
        renpy.store.cover_lane_player_x = float(COVER_LANE_START_X)
        renpy.store.cover_lane_dest_x = float(COVER_LANE_START_X)
        renpy.store.cover_lane_facing = 1
        renpy.store.cover_lane_moving = False
        renpy.store.cover_lane_walk_t = 0.0
        renpy.store.cover_lane_pacer_x = float(COVER_LANE_PACER_MIN_X + 80.0)
        renpy.store.cover_lane_pacer_dir = 1
        renpy.store.cover_lane_outcome = None
        _cl_grace_ms[0] = 0.0
        _cl_last_t[0] = None

    def cover_lane_prepare():
        cover_lane_hide_overworld()
        cover_lane_reset()

    def cover_lane_click_street():
        mx, my = renpy.get_mouse_pos()
        logic_y = my / CL_SCALE_Y
        if logic_y < COVER_LANE_CLICK_Y:
            return
        logic_x = mx / CL_SCALE_X
        dest = max(COVER_LANE_PATH_MIN, min(COVER_LANE_PATH_MAX, logic_x))
        renpy.store.cover_lane_dest_x = float(dest)

    def cover_lane_advance():
        """Move player, move pacer, then detection. Returns caught/clear/None."""
        now = _cover_lane_now()
        dt = 0.016
        if _cl_last_t[0] is not None:
            dt = max(0.0, min(0.1, now - _cl_last_t[0]))
        _cl_last_t[0] = now
        if dt <= 0.0:
            dt = 0.016

        crouched = bool(renpy.store.cover_lane_crouched)
        speed = COVER_LANE_STAND_SPEED
        if crouched:
            speed *= COVER_LANE_CROUCH_SPEED_MULT

        x = float(renpy.store.cover_lane_player_x)
        dest = float(renpy.store.cover_lane_dest_x)
        dx = dest - x
        step = speed * dt
        if abs(dx) <= step:
            x = dest
            renpy.store.cover_lane_moving = False
        else:
            facing = 1 if dx > 0 else -1
            x += facing * step
            renpy.store.cover_lane_facing = facing
            renpy.store.cover_lane_moving = True
            renpy.store.cover_lane_walk_t = float(renpy.store.cover_lane_walk_t) + dt
        renpy.store.cover_lane_player_x = x

        _cl_update_pacer(dt)

        instant = cover_lane_rules_tick(
            x,
            crouched,
            pacer_rect=cover_lane_pacer_rect(),
            moving=bool(renpy.store.cover_lane_moving),
            cover=COVER_LANE_COVER,
        )
        if instant == "caught":
            _cl_grace_ms[0] += dt * 1000.0
            if _cl_grace_ms[0] >= COVER_LANE_GRACE_MS:
                return "caught"
        else:
            _cl_grace_ms[0] = 0.0
            if instant == "clear":
                return "clear"
        return None

    def cover_lane_step():
        if renpy.store.cover_lane_outcome:
            return
        result = cover_lane_advance()
        if result:
            renpy.store.cover_lane_outcome = result

    def _cl_put(parts, x, y, w, h, color):
        parts.append(((int(x), int(y)), Solid(color, xsize=max(1, int(w)), ysize=max(1, int(h)))))

    def cl_build_background():
        """Static night facade + street at 1920x1080."""
        parts = []
        _cl_put(parts, 0, 0, CL_VIEW_W, CL_VIEW_H, "#07080e")
        _cl_put(parts, 0, 0, CL_VIEW_W, cl_y(440), "#10131c")
        stars = (
            (80, 40, 3), (140, 22, 2), (210, 58, 3), (320, 18, 2),
            (410, 44, 3), (520, 28, 2), (640, 16, 3), (760, 38, 2),
            (880, 22, 3), (980, 50, 2), (1080, 14, 3), (1240, 36, 2),
        )
        for sx, sy, sr in stars:
            _cl_put(parts, cl_x(sx), cl_y(sy), sr, sr, "#cdd6e6")

        # Far alley
        _cl_put(parts, cl_x(1148), cl_y(210), cl_w(132), cl_h(230), "#0e1016")
        _cl_put(parts, cl_x(1188), cl_y(268), cl_w(92), cl_h(172), "#12141c")

        # Facade
        _cl_put(parts, cl_x(18), 0, cl_w(1140), cl_h(10), "#3d3a34")
        _cl_put(parts, cl_x(18), cl_y(8), cl_w(1140), cl_h(16), "#2a2723")
        _cl_put(parts, cl_x(28), cl_y(18), cl_w(1118), cl_h(422), "#1c1916")
        # Brick rows (sparse so the screen stays light)
        brick_colors = ("#2a2420", "#26211d", "#231e1b", "#251f1c")
        row = 0
        by = cl_y(24)
        while by < cl_y(420):
            col = 0
            bx = cl_x(36) + (cl_w(20) if row % 2 else 0)
            while bx < cl_x(1140):
                _cl_put(parts, bx, by, cl_w(38), cl_h(12), brick_colors[(col + row) % 4])
                bx += cl_w(42)
                col += 1
            by += cl_h(16)
            row += 1
        for px, pw in ((48, 22), (368, 28), (714, 28), (1060, 22)):
            _cl_put(parts, cl_x(px), cl_y(36), cl_w(pw), cl_h(384), "#24211d")
        _cl_put(parts, cl_x(18), cl_y(420), cl_w(1140), cl_h(20), "#2c2a26")
        _cl_put(parts, cl_x(18), cl_y(420), cl_w(1140), cl_h(4), "#3a3732")

        # Street
        _cl_put(parts, 0, cl_y(440), CL_VIEW_W, cl_h(360), "#1a1b20")
        _cl_put(parts, 0, cl_y(440), cl_w(1148), cl_h(126), "#2a2b30")
        _cl_put(parts, 0, cl_y(562), cl_w(1148), cl_h(6), "#323338")
        _cl_put(parts, 0, cl_y(568), cl_w(1148), cl_h(10), "#3a3b40")
        _cl_put(parts, 0, cl_y(578), CL_VIEW_W, cl_h(222), "#141518")
        _cl_put(parts, 0, cl_y(548), cl_w(1164), cl_h(8), "#30323c")
        _cl_put(parts, 0, cl_y(550), cl_w(1164), cl_h(2), "#5a5c68")

        # Alley mouth / exit
        _cl_put(parts, cl_x(1148), cl_y(440), cl_w(132), cl_h(138), "#0c0d12")
        _cl_put(parts, cl_x(1148), cl_y(210), cl_w(132), cl_h(368), "#00000048")
        _cl_put(parts, cl_x(1204), cl_y(390), cl_w(8), cl_h(56), "#2a4a38")
        _cl_put(parts, cl_x(1204), cl_y(382), cl_w(12), cl_h(12), "#6aaa6a")

        # Lamp post near start
        _cl_put(parts, cl_x(108), cl_y(432), cl_w(6), cl_h(140), "#2a2a28")
        _cl_put(parts, cl_x(96), cl_y(426), cl_w(30), cl_h(6), "#3a382e")
        _cl_put(parts, cl_x(40), cl_y(500), cl_w(140), cl_h(70), "#d2b46e22")

        args = []
        for pos, disp in parts:
            args.append(pos)
            args.append(disp)
        args.append((cl_x(1168), cl_y(18)))
        args.append(Text("●", size=36, color="#c8c4b0"))
        args.append((cl_x(1178), cl_y(14)))
        args.append(Text("●", size=32, color="#07080e"))
        args.append((cl_x(1188), cl_y(448)))
        args.append(Text("EXIT", size=16, color="#889988"))
        return Composite((CL_VIEW_W, CL_VIEW_H), *args)

    def cl_background():
        if _cl_bg_cache[0] is None:
            _cl_bg_cache[0] = cl_build_background()
        return _cl_bg_cache[0]

    # kind=window: high sill (crouch reads as below it). kind=door: taller
    # bay, floor threshold, no crouch-sill. Frame = interior; glass after NPCs.
    def cl_window_frame(win, watching, empty=False):
        """Interior for one bay (glass / door drawn after NPCs)."""
        x, y, w, h = cl_x(win["x"]), cl_y(win["y"]), cl_w(win["w"]), cl_h(win["h"])
        opening_kind = win.get("kind", "window")
        parts = []
        _cl_put(parts, x, y, w, h, "#07080c")
        if empty:
            _cl_put(parts, x + cl_w(16), y + cl_h(20), w - cl_w(32), h - cl_h(48), "#161820b3")
        elif watching:
            _cl_put(parts, x, y, w, h, "#5a371c8c")
        else:
            _cl_put(parts, x, y, w, h, "#12141c80")
        if opening_kind == "door":
            _cl_put(parts, x + cl_w(10), y + h - cl_h(36), w - cl_w(20), cl_h(24), "#14120e99")
        args = []
        for pos, disp in parts:
            args.append(pos)
            args.append(disp)
        return Composite((CL_VIEW_W, CL_VIEW_H), *args)

    def cl_window_glass(win, watching):
        x, y, w, h = cl_x(win["x"]), cl_y(win["y"]), cl_w(win["w"]), cl_h(win["h"])
        opening_kind = win.get("kind", "window")
        parts = []
        glass = "#b48c4620" if watching else "#14182466"
        _cl_put(parts, x, y, w, h, glass)
        frame = "#3e3b36"
        _cl_put(parts, x, y, w, cl_h(8), frame)
        _cl_put(parts, x, y, cl_w(8), h, frame)
        _cl_put(parts, x + w - cl_w(8), y, cl_w(8), h, frame)
        mullion = "#d2a05059" if watching else "#32364280"
        if opening_kind == "door":
            # Double-door split + floor-level threshold (thin strip, not a crouch sill).
            _cl_put(parts, x + w // 2 - 2, y + cl_h(8), 4, h - cl_h(14), mullion)
            thresh = "#3a3834" if watching else "#2c2a28"
            thresh_hi = "#524e46" if watching else "#3a3834"
            _cl_put(parts, x, y + h - cl_h(6), w, cl_h(6), thresh)
            _cl_put(parts, x, y + h - cl_h(6), w, cl_h(2), thresh_hi)
            handle = "#c4a46a" if watching else "#6a6458"
            hx = x + w // 2 + cl_w(12)
            hy = y + int(h * 0.52)
            _cl_put(parts, hx, hy, cl_w(5), cl_h(22), handle)
            _cl_put(parts, hx + cl_w(4), hy + cl_h(7), cl_w(10), cl_h(5), handle)
            if watching:
                _cl_put(parts, x + cl_w(8), y + h - cl_h(4), w - cl_w(16), cl_h(10), "#dc8a4622")
        else:
            _cl_put(parts, x, y + h - cl_h(8), w, cl_h(8), frame)
            _cl_put(parts, x + w // 2 - 1, y + cl_h(8), 2, h - cl_h(16), mullion)
            sill = "#4a4030" if watching else "#32302c"
            sill_hi = "#6a5a40" if watching else "#45423c"
            _cl_put(parts, x - cl_w(8), y + h, w + cl_w(16), cl_h(12), sill)
            _cl_put(parts, x - cl_w(8), y + h, w + cl_w(16), cl_h(3), sill_hi)
            if watching:
                _cl_put(parts, x - cl_w(6), y + h + cl_h(10), w + cl_w(12), cl_h(8), "#dc8a4622")
        args = []
        for pos, disp in parts:
            args.append(pos)
            args.append(disp)
        return Composite((CL_VIEW_W, CL_VIEW_H), *args)

    def cl_silhouette(w, h, body, head, eyes=None, facing=1):
        w = int(w)
        h = int(h)
        parts = []
        leg_w = max(6, w // 5)
        leg_h = max(10, h // 5)
        _cl_put(parts, int(w * 0.22), h - leg_h, leg_w, leg_h, "#15141a")
        _cl_put(parts, int(w * 0.58), h - leg_h, leg_w, leg_h, "#15141a")
        body_w = int(w * 0.72)
        body_h = int(h * 0.55)
        _cl_put(parts, int((w - body_w) / 2), h - leg_h - body_h + 4, body_w, body_h, body)
        head_w = int(w * 0.42)
        head_h = int(h * 0.22)
        hx = int((w - head_w) / 2)
        hy = int(h * 0.08)
        _cl_put(parts, hx, hy, head_w, head_h, head)
        _cl_put(parts, hx - 1, hy - 2, head_w + 2, max(4, head_h // 3), "#121014")
        if eyes:
            eye = max(3, w // 12)
            eye_y = hy + head_h // 2 - eye // 2
            off = 3 if facing >= 0 else -3
            _cl_put(parts, hx + head_w // 2 - eye - 2 + off, eye_y, eye, eye, eyes)
            _cl_put(parts, hx + head_w // 2 + 2 + off, eye_y, eye, eye, eyes)
        args = []
        for pos, disp in parts:
            args.append(pos)
            args.append(disp)
        child = Composite((w, h), *args)
        if facing < 0:
            child = Transform(child, xzoom=-1, xanchor=0.5, xpos=w // 2)
        return child

    def cl_fallback_body(w, h):
        return cl_silhouette(w, h, body="#1c1e28", head="#5a5348", eyes=None, facing=1)

    def cl_player_child():
        h = cl_h(COVER_LANE_PLAYER_H)
        w = cl_w(COVER_LANE_PLAYER_W)
        if cl_player_art_loaded():
            path = CL_STAND_PATH
            if renpy.store.cover_lane_moving:
                walks = cl_walk_paths_loaded()
                if walks:
                    idx = int(float(renpy.store.cover_lane_walk_t) / 0.12) % len(walks)
                    path = walks[idx]
            return Transform(path, ysize=h, nearest=True)
        return cl_fallback_body(w, h)

    def cl_sentry_child():
        w = cl_w(COVER_LANE_PACER_W + 4)
        h = cl_h(COVER_LANE_PACER_H + 8)
        return cl_silhouette(w, h, body="#1c1a22", head="#2a241e", eyes="#e8c070", facing=1)

    def cl_pacer_child(watching):
        w = cl_w(COVER_LANE_PACER_W)
        h = cl_h(COVER_LANE_PACER_H)
        facing = 1 if int(renpy.store.cover_lane_pacer_dir) >= 0 else -1
        eyes = "#f0c878" if watching else None
        return cl_silhouette(w, h, body="#222018", head="#2c261e", eyes=eyes, facing=facing)

    def _cl_parts_composite(size, parts):
        args = []
        for pos, disp in parts:
            args.append(pos)
            args.append(disp)
        return Composite(size, *args)

    def cl_dumpster_art(w, h):
        """Dark green metal dumpster. w/h are view pixels."""
        w = int(w)
        h = int(h)
        parts = []
        wheel = max(6, h // 10)
        _cl_put(parts, int(w * 0.12), h - wheel, max(8, w // 6), wheel, "#1a1c18")
        _cl_put(parts, int(w * 0.68), h - wheel, max(8, w // 6), wheel, "#1a1c18")
        body_h = int(h * 0.70)
        body_y = h - wheel - body_h + 4
        _cl_put(parts, 2, body_y, w - 4, body_h, "#1e3328")
        _cl_put(parts, 4, body_y + 6, w - 8, body_h - 12, "#243a2e")
        _cl_put(parts, 2, body_y, w - 4, max(5, h // 12), "#2a4434")
        _cl_put(parts, 6, body_y + max(10, h // 8), w - 12, max(3, h // 18), "#162820")
        _cl_put(parts, int(w * 0.46), body_y + 4, max(3, w // 18), body_h - 8, "#1a2c24")
        lid_h = max(7, h // 9)
        _cl_put(parts, 0, body_y - lid_h + 2, w, lid_h, "#243a2e")
        _cl_put(parts, 2, body_y - lid_h, int(w * 0.62), max(5, h // 12), "#2c4636")
        _cl_put(parts, int(w * 0.38), body_y + int(body_h * 0.38), max(12, w // 5), max(5, h // 14), "#3a4a40")
        return _cl_parts_composite((w, h), parts)

    def cl_planter_art(w, h):
        """Box planter with muted night foliage."""
        w = int(w)
        h = int(h)
        parts = []
        box_h = max(14, int(h * 0.40))
        box_y = h - box_h
        _cl_put(parts, 2, box_y, w - 4, box_h, "#3a3228")
        _cl_put(parts, 2, box_y, w - 4, max(3, h // 16), "#4a4034")
        _cl_put(parts, 4, box_y + max(4, h // 14), w - 8, max(3, h // 18), "#2a241c")
        _cl_put(parts, 6, box_y + 2, w - 12, max(4, h // 14), "#2a2018")
        _cl_put(parts, int(w * 0.18), int(h * 0.18), max(8, w // 4), box_y - int(h * 0.10), "#2a4a38")
        _cl_put(parts, int(w * 0.46), int(h * 0.04), max(10, w // 3), box_y + 2, "#3a5a40")
        _cl_put(parts, int(w * 0.28), int(h * 0.28), max(7, w // 5), int(h * 0.24), "#1e3a2c")
        return _cl_parts_composite((w, h), parts)

    def cl_crate_art(w, h):
        """Short wooden crate — front-layer street clutter over legs/feet."""
        w = int(w)
        h = int(h)
        parts = []
        _cl_put(parts, 1, 2, w - 2, h - 2, "#3a2e22")
        _cl_put(parts, 2, 4, w - 4, h - 6, "#4a3a2a")
        _cl_put(parts, 3, 5, w - 6, max(3, h // 8), "#2a2218")
        _cl_put(parts, 3, int(h * 0.42), w - 6, max(3, h // 10), "#2a2218")
        _cl_put(parts, 3, h - max(6, h // 6), w - 6, max(3, h // 10), "#5a4a38")
        _cl_put(parts, int(w * 0.46), 4, max(2, w // 12), h - 8, "#2c241c")
        _cl_put(parts, 2, 3, w - 4, max(2, h // 14), "#6a5844")
        return _cl_parts_composite((w, h), parts)

    def cl_bin_art(w, h):
        """Short street bin — same front-layer pass as crate."""
        w = int(w)
        h = int(h)
        parts = []
        _cl_put(parts, 3, int(h * 0.12), w - 6, h - int(h * 0.12), "#2a3230")
        _cl_put(parts, 4, int(h * 0.18), w - 8, h - int(h * 0.22), "#343e3c")
        _cl_put(parts, 2, int(h * 0.08), w - 4, max(5, h // 8), "#3a4440")
        _cl_put(parts, int(w * 0.38), int(h * 0.10), max(8, w // 4), max(4, h // 10), "#4a5450")
        _cl_put(parts, int(w * 0.18), int(h * 0.40), max(3, w // 10), int(h * 0.28), "#1e2624")
        return _cl_parts_composite((w, h), parts)

    # Art picker: kind -> dumpster/crate/bin/planter (else planter). Add a
    # branch + art function for a new kind; detection only cares about layer.
    def cl_cover_child(cover):
        w = cl_w(cover["w"])
        h = cl_h(cover["h"])
        kind = cover.get("kind")
        if kind == "dumpster":
            return cl_dumpster_art(w, h)
        if kind == "crate":
            return cl_crate_art(w, h)
        if kind == "bin":
            return cl_bin_art(w, h)
        return cl_planter_art(w, h)


# ---------------------------------------------------------------------------
# Gameplay screen — this IS the level. jump cover_lane to play.
# Paint order = z-order (later = in front). Numbered 1-9 below.
# ---------------------------------------------------------------------------

screen cover_lane_scene():
    modal True
    zorder 80

    # 1. Background (night facade + street). Later children draw in front.
    add cl_background()

    # 2. Interiors — hardcoded [0] sentry / [1] pacer / [2] empty.
    #    A 4th opening needs another frame (+ glass + viewport) row.
    add cl_window_frame(COVER_LANE_OPENINGS[0], True, empty=False)
    add cl_window_frame(COVER_LANE_OPENINGS[1], cover_lane_pacer_watching(), empty=False)
    add cl_window_frame(COVER_LANE_OPENINGS[2], False, empty=True)

    # 3. NPC viewports — clip silhouettes to the opening. Do NOT set
    #    `background` on a viewport (Ren'Py 8.5 error); already transparent.
    # Sentry — static in opening [0].
    $ _wa = COVER_LANE_OPENINGS[0]
    viewport:
        xpos cl_x(_wa["x"])
        ypos cl_y(_wa["y"])
        xsize cl_w(_wa["w"])
        ysize cl_h(_wa["h"])
        draggable False
        mousewheel False
        scrollbars None
        add Solid("#d2964666"):
            xanchor 0.5
            yanchor 0.5
            xpos cl_w(_wa["w"]) // 2
            ypos cl_h(_wa["h"]) - cl_h(90)
            xsize cl_w(90)
            ysize cl_h(110)
        add cl_sentry_child():
            xanchor 0.5
            yanchor 1.0
            xpos cl_w(_wa["w"]) // 2
            ypos cl_h(_wa["h"]) - cl_h(8)

    # Pacer — clipped to opening [1]; glow only while overlapping that rect.
    $ _wb = COVER_LANE_OPENINGS[1]
    $ _pacer_watch = cover_lane_pacer_watching()
    viewport:
        xpos cl_x(_wb["x"])
        ypos cl_y(_wb["y"])
        xsize cl_w(_wb["w"])
        ysize cl_h(_wb["h"])
        draggable False
        mousewheel False
        scrollbars None
        if _pacer_watch:
            add Solid("#d2964666"):
                xanchor 0.5
                yanchor 0.5
                xpos cl_x(cover_lane_pacer_x + COVER_LANE_PACER_W * 0.5) - cl_x(_wb["x"])
                ypos cl_y(COVER_LANE_PACER_Y + COVER_LANE_PACER_H * 0.4) - cl_y(_wb["y"])
                xsize cl_w(90)
                ysize cl_h(110)
        add cl_pacer_child(_pacer_watch):
            xanchor 0.5
            yanchor 1.0
            xpos cl_x(cover_lane_pacer_x + COVER_LANE_PACER_W * 0.5) - cl_x(_wb["x"])
            ypos cl_y(COVER_LANE_PACER_Y + COVER_LANE_PACER_H) - cl_y(_wb["y"])

    # 4. Glass / door frames (after NPCs so they sit behind the pane).
    add cl_window_glass(COVER_LANE_OPENINGS[0], True)
    add cl_window_glass(COVER_LANE_OPENINGS[1], _pacer_watch)
    add cl_window_glass(COVER_LANE_OPENINGS[2], False)

    # 5. Watch bands — street glow under a currently-watched opening.
    for _win in COVER_LANE_OPENINGS:
        if cover_lane_window_watching(_win):
            add Solid("#b45a2818"):
                xpos cl_x(_win["x"])
                ypos cl_y(COVER_LANE_STREET_Y - 18)
                xsize cl_w(_win["w"])
                ysize cl_h(16)

    # 6. Click-to-move (street / ground only) + dest marker. Reclick replaces dest.
    button:
        xpos 0
        ypos cl_y(COVER_LANE_CLICK_Y)
        xsize CL_VIEW_W
        ysize CL_VIEW_H - cl_y(COVER_LANE_CLICK_Y)
        background Solid((0, 0, 0, 1))
        action Function(cover_lane_click_street)

    if abs(cover_lane_dest_x - cover_lane_player_x) > 1.0:
        add Transform(Solid("#ffcc44", xsize=14, ysize=14), rotate=45):
            xpos cl_x(cover_lane_dest_x)
            ypos cl_y(COVER_LANE_STREET_Y)
            xanchor 0.5
            yanchor 0.5

    # 7. Behind props — hide-behind cover, drawn before the player.
    for _cov in COVER_LANE_COVER:
        if cl_cover_layer(_cov) == "behind":
            add cl_cover_child(_cov):
                xpos cl_x(_cov["x"])
                ypos cl_y(COVER_LANE_STREET_Y)
                xanchor 0.0
                yanchor 1.0

    # 8. Player — xpos is CENTRE; ypos STREET_Y; yanchor 1.0. Crouch yzoom 0.62.
    add Solid("#00000059"):
        xpos cl_x(cover_lane_player_x)
        ypos cl_y(COVER_LANE_STREET_Y + 2)
        xanchor 0.5
        yanchor 0.5
        xsize cl_w(28)
        ysize cl_h(6)
    add cl_player_child():
        id "cl_player"
        xpos cl_x(cover_lane_player_x)
        ypos cl_y(COVER_LANE_STREET_Y)
        xanchor 0.5
        yanchor 1.0
        xzoom cover_lane_facing
        yzoom (COVER_LANE_CROUCH_SCALE_Y if cover_lane_crouched else 1.0)

    # 9. Front items — visual street clutter over the sprite; does not hide.
    #    HUD follows (on top of 1-9).
    for _cov in COVER_LANE_COVER:
        if cl_cover_layer(_cov) == "front":
            add cl_cover_child(_cov):
                xpos cl_x(_cov["x"])
                ypos cl_y(COVER_LANE_STREET_Y)
                xanchor 0.0
                yanchor 1.0

    # HUD — last, on top of the scene.
    frame:
        background Solid((0, 0, 0, 160))
        padding (12, 10)
        xalign 0.0
        yalign 0.0
        offset (20, 20)
        xminimum 248

        vbox:
            spacing 6
            if cover_lane_crouched:
                text "Crouched" size 22 color "#ffcc44"
            else:
                text "Standing" size 22 color "#cccccc"
            textbutton ("Stand" if cover_lane_crouched else "Crouch"):
                action Function(cover_lane_toggle_crouch)
                text_size 20
                text_color "#eeeeee"
                xfill True
                background Solid("#333333")
                hover_background Solid("#0099cc")
                padding (12, 8)
            text "C toggles crouch. Duck at windows. Hide against the building; street items sit over you." size 14 color "#888899"

    frame:
        background Solid((0, 0, 0, 160))
        padding (12, 10)
        xalign 1.0
        yalign 0.0
        offset (-20, 20)
        xmaximum 320

        vbox:
            spacing 4
            text "Goal" size 18 color "#aaaaaa"
            text "Reach the alley exit" size 22 color "#ffcc44"

    key "c" action Function(cover_lane_toggle_crouch)
    key "C" action Function(cover_lane_toggle_crouch)
    key "K_c" action Function(cover_lane_toggle_crouch)

    timer 0.016 repeat True action Function(cover_lane_step)
    if cover_lane_outcome:
        timer 0.01 action Return(cover_lane_outcome)


# Entry. Caught / clear Leave+Return jump rooftop_a_1 — change if this
# level's overworld entry differs.
label cover_lane:
    window hide
    python:
        try:
            renpy.hide_screen("rf_map")
        except Exception:
            pass
        try:
            renpy.hide_screen("test_world")
        except Exception:
            pass
    $ cover_lane_prepare()
    call screen cover_lane_scene
    if _return == "caught":
        jump cover_lane_caught
    jump cover_lane_clear


label cover_lane_caught:
    cover_lane_voice "“Hey! What are you doing out there?”"
    "They’ve seen you on the sidewalk — past a window, or standing in a door."
    menu:
        "Try again":
            jump cover_lane
        "Leave":
            jump rooftop_a_1


label cover_lane_clear:
    "You slip past the windows and the glass door."
    menu:
        "Again":
            jump cover_lane
        "Return to rooftop":
            jump rooftop_a_1
