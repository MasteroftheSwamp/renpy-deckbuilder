# ---------------------------------------------------------------------------
# Fuller template with doors/cover/layers is cover_lane.rpy.
# Fork new sneak levels from that file, not this one.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Window-lane sneak — self-contained side-on mini-level (Ren'Py 8)
#
# Copy game/scripts/stealth/ into the real project, then:
#     jump window_lane
#
# Do not patch follower_controller.rpy. This screen is the gameplay; it does
# not depend on Follower. Geometry matches stealth.py (1280x800 logic space,
# drawn at 1920x1080). Detection uses the same rules as stealth.py, with a
# ~120 ms grace so a one-pixel edge does not false-trigger.
# ---------------------------------------------------------------------------

default player_crouched = False
default window_lane_player_x = 86.0
default window_lane_dest_x = 86.0
default window_lane_facing = 1
default window_lane_moving = False
default window_lane_walk_t = 0.0
default window_lane_pacer_x = 570.0
default window_lane_pacer_dir = 1
default window_lane_outcome = None


define window_lane_voice = Character("Voice from the window", color="#c9a066")


# Named RF android art. Shown only when loadable; Solids are the fallback so
# this file still runs if the example images are not on disk yet.
image wl_android_stand = "RF/example images/android/body/stand/h/0.png"
image wl_android_walk:
    "RF/example images/android/body/walk/h/0.png"
    pause 0.12
    "RF/example images/android/body/walk/h/1.png"
    pause 0.12
    "RF/example images/android/body/walk/h/2.png"
    pause 0.12
    "RF/example images/android/body/walk/h/3.png"
    pause 0.12
    repeat
image wl_android_walk_0 = "RF/example images/android/body/walk/h/0.png"
image wl_android_walk_1 = "RF/example images/android/body/walk/h/1.png"
image wl_android_walk_2 = "RF/example images/android/body/walk/h/2.png"
image wl_android_walk_3 = "RF/example images/android/body/walk/h/3.png"


init python:
    import os
    import sys
    import time

    # 1280x800 logic space from stealth.py, drawn at 1920x1080.
    WL_VIEW_W = 1920
    WL_VIEW_H = 1080
    WL_LOGIC_W = 1280.0
    WL_LOGIC_H = 800.0
    WL_SCALE_X = WL_VIEW_W / WL_LOGIC_W
    WL_SCALE_Y = WL_VIEW_H / WL_LOGIC_H

    WINDOW_LANE_PLAYER_W = 36
    WINDOW_LANE_PLAYER_H = 78
    WINDOW_LANE_START_X = 86
    WINDOW_LANE_CLEAR_X = 1188
    WINDOW_LANE_STREET_Y = 552
    WINDOW_LANE_STAND_SPEED = 180.0
    WINDOW_LANE_CROUCH_SPEED_MULT = 0.45
    WINDOW_LANE_CROUCH_SCALE_Y = 0.62
    WINDOW_LANE_GRACE_MS = 120
    WINDOW_LANE_PATH_MIN = 64.0
    WINDOW_LANE_PATH_MAX = 1216.0
    WINDOW_LANE_CLICK_Y = 416.0

    WINDOW_LANE_PACER_W = 44
    WINDOW_LANE_PACER_H = 98
    WINDOW_LANE_PACER_Y = 232
    WINDOW_LANE_PACER_MIN_X = 490.0
    WINDOW_LANE_PACER_MAX_X = 762.0
    WINDOW_LANE_PACER_SPEED = 52.0

    WINDOW_LANE_WINDOWS = [
        {"id": "A", "x": 132, "y": 96, "w": 200, "h": 252, "npc": "sentry"},
        {"id": "B", "x": 478, "y": 96, "w": 200, "h": 252, "npc": "pacer"},
        {"id": "C", "x": 824, "y": 96, "w": 200, "h": 252, "npc": None},
    ]

    WL_STAND_PATH = "RF/example images/android/body/stand/h/0.png"
    WL_WALK_PATHS = [
        "RF/example images/android/body/walk/h/0.png",
        "RF/example images/android/body/walk/h/1.png",
        "RF/example images/android/body/walk/h/2.png",
        "RF/example images/android/body/walk/h/3.png",
    ]

    _wl_stealth_mod = None
    try:
        _wl_root = os.path.abspath(os.path.join(renpy.config.gamedir, ".."))
        if _wl_root not in sys.path:
            sys.path.append(_wl_root)
        import stealth as _wl_stealth_mod
    except Exception:
        _wl_stealth_mod = None

    _wl_last_t = [None]
    _wl_grace_ms = [0.0]
    _wl_bg_cache = [None]
    _wl_art_cache = [None]

    def wl_x(x):
        return int(round(float(x) * WL_SCALE_X))

    def wl_y(y):
        return int(round(float(y) * WL_SCALE_Y))

    def wl_w(w):
        return max(1, int(round(float(w) * WL_SCALE_X)))

    def wl_h(h):
        return max(1, int(round(float(h) * WL_SCALE_Y)))

    def wl_player_art_loaded():
        if _wl_art_cache[0] is None:
            try:
                _wl_art_cache[0] = bool(renpy.loadable(WL_STAND_PATH))
            except Exception:
                _wl_art_cache[0] = False
        return _wl_art_cache[0]

    def wl_walk_paths_loaded():
        paths = []
        for path in WL_WALK_PATHS:
            try:
                if renpy.loadable(path):
                    paths.append(path)
            except Exception:
                pass
        return paths

    def _window_lane_now():
        try:
            return renpy.get_game_runtime()
        except Exception:
            return time.time()

    def _wl_rects_overlap(a, b):
        return (
            a["x"] < b["x"] + b["w"]
            and b["x"] < a["x"] + a["w"]
            and a["y"] < b["y"] + b["h"]
            and b["y"] < a["y"] + a["h"]
        )

    def window_lane_pacer_rect():
        return {
            "x": float(renpy.store.window_lane_pacer_x),
            "y": WINDOW_LANE_PACER_Y,
            "w": WINDOW_LANE_PACER_W,
            "h": WINDOW_LANE_PACER_H,
        }

    def npc_watching(window, pacer_rect=None):
        """Sentry always watches. Pacer watches iff their body overlaps that window. Empty never."""
        kind = window.get("npc")
        if kind == "sentry":
            return True
        if kind == "pacer":
            if pacer_rect is None:
                pacer_rect = window_lane_pacer_rect()
            return _wl_rects_overlap(pacer_rect, window)
        return False

    def _wl_player_overlaps_window(player_x, window, player_w=WINDOW_LANE_PLAYER_W):
        half = player_w * 0.5
        return (player_x - half) < (window["x"] + window["w"]) and window["x"] < (player_x + half)

    def window_lane_rules_tick(player_x, crouched, pacer_rect=None, windows=None, player_w=WINDOW_LANE_PLAYER_W, clear_x=WINDOW_LANE_CLEAR_X):
        """Instant overlap check — same rules as stealth.window_lane_tick."""
        if _wl_stealth_mod is not None:
            return _wl_stealth_mod.window_lane_tick(
                player_x,
                crouched,
                windows=windows,
                pacer_rect=pacer_rect,
                player_w=player_w,
                clear_x=clear_x,
            )
        windows = WINDOW_LANE_WINDOWS if windows is None else windows
        for window in windows:
            if _wl_player_overlaps_window(player_x, window, player_w=player_w):
                if npc_watching(window, pacer_rect) and not crouched:
                    return "caught"
        if player_x >= clear_x:
            return "clear"
        return None

    def _wl_update_pacer(dt):
        x = float(renpy.store.window_lane_pacer_x)
        d = 1 if int(renpy.store.window_lane_pacer_dir) >= 0 else -1
        x += d * WINDOW_LANE_PACER_SPEED * dt
        if x <= WINDOW_LANE_PACER_MIN_X:
            x = WINDOW_LANE_PACER_MIN_X
            d = 1
        elif x >= WINDOW_LANE_PACER_MAX_X:
            x = WINDOW_LANE_PACER_MAX_X
            d = -1
        renpy.store.window_lane_pacer_x = x
        renpy.store.window_lane_pacer_dir = d

    def window_lane_pacer_watching():
        win_b = WINDOW_LANE_WINDOWS[1]
        return npc_watching(win_b, window_lane_pacer_rect())

    def window_lane_window_watching(window):
        return npc_watching(window, window_lane_pacer_rect())

    def toggle_crouch():
        """Flip crouched. Speed is applied in window_lane_advance (no Follower)."""
        renpy.store.player_crouched = not bool(renpy.store.player_crouched)

    def window_lane_hide_overworld():
        for name in ("rf_map", "test_world", "editor_world", "hud", "player_menu"):
            try:
                renpy.hide_screen(name)
            except Exception:
                pass

    def window_lane_reset():
        """Reset crouched, positions, pacer, and detection grace."""
        renpy.store.player_crouched = False
        renpy.store.window_lane_player_x = float(WINDOW_LANE_START_X)
        renpy.store.window_lane_dest_x = float(WINDOW_LANE_START_X)
        renpy.store.window_lane_facing = 1
        renpy.store.window_lane_moving = False
        renpy.store.window_lane_walk_t = 0.0
        renpy.store.window_lane_pacer_x = float(WINDOW_LANE_PACER_MIN_X + 80.0)
        renpy.store.window_lane_pacer_dir = 1
        renpy.store.window_lane_outcome = None
        _wl_grace_ms[0] = 0.0
        _wl_last_t[0] = None

    def window_lane_prepare():
        window_lane_hide_overworld()
        window_lane_reset()

    def window_lane_click_street():
        mx, my = renpy.get_mouse_pos()
        logic_y = my / WL_SCALE_Y
        if logic_y < WINDOW_LANE_CLICK_Y:
            return
        logic_x = mx / WL_SCALE_X
        dest = max(WINDOW_LANE_PATH_MIN, min(WINDOW_LANE_PATH_MAX, logic_x))
        renpy.store.window_lane_dest_x = float(dest)

    def window_lane_advance():
        """Move player, move pacer, then detection. Returns caught/clear/None."""
        now = _window_lane_now()
        dt = 0.016
        if _wl_last_t[0] is not None:
            dt = max(0.0, min(0.1, now - _wl_last_t[0]))
        _wl_last_t[0] = now
        if dt <= 0.0:
            dt = 0.016

        crouched = bool(renpy.store.player_crouched)
        speed = WINDOW_LANE_STAND_SPEED
        if crouched:
            speed *= WINDOW_LANE_CROUCH_SPEED_MULT

        x = float(renpy.store.window_lane_player_x)
        dest = float(renpy.store.window_lane_dest_x)
        dx = dest - x
        step = speed * dt
        if abs(dx) <= step:
            x = dest
            renpy.store.window_lane_moving = False
        else:
            facing = 1 if dx > 0 else -1
            x += facing * step
            renpy.store.window_lane_facing = facing
            renpy.store.window_lane_moving = True
            renpy.store.window_lane_walk_t = float(renpy.store.window_lane_walk_t) + dt
        renpy.store.window_lane_player_x = x

        _wl_update_pacer(dt)

        instant = window_lane_rules_tick(
            x,
            crouched,
            pacer_rect=window_lane_pacer_rect(),
        )
        if instant == "caught":
            _wl_grace_ms[0] += dt * 1000.0
            if _wl_grace_ms[0] >= WINDOW_LANE_GRACE_MS:
                return "caught"
        else:
            _wl_grace_ms[0] = 0.0
            if instant == "clear":
                return "clear"
        return None

    def window_lane_step():
        if renpy.store.window_lane_outcome:
            return
        result = window_lane_advance()
        if result:
            renpy.store.window_lane_outcome = result

    def _wl_put(parts, x, y, w, h, color):
        parts.append(((int(x), int(y)), Solid(color, xsize=max(1, int(w)), ysize=max(1, int(h)))))

    def wl_build_background():
        """Static night facade + street at 1920x1080."""
        parts = []
        _wl_put(parts, 0, 0, WL_VIEW_W, WL_VIEW_H, "#07080e")
        _wl_put(parts, 0, 0, WL_VIEW_W, wl_y(440), "#10131c")
        stars = (
            (80, 40, 3), (140, 22, 2), (210, 58, 3), (320, 18, 2),
            (410, 44, 3), (520, 28, 2), (640, 16, 3), (760, 38, 2),
            (880, 22, 3), (980, 50, 2), (1080, 14, 3), (1240, 36, 2),
        )
        for sx, sy, sr in stars:
            _wl_put(parts, wl_x(sx), wl_y(sy), sr, sr, "#cdd6e6")

        # Far alley
        _wl_put(parts, wl_x(1148), wl_y(210), wl_w(132), wl_h(230), "#0e1016")
        _wl_put(parts, wl_x(1188), wl_y(268), wl_w(92), wl_h(172), "#12141c")

        # Facade
        _wl_put(parts, wl_x(18), 0, wl_w(1140), wl_h(10), "#3d3a34")
        _wl_put(parts, wl_x(18), wl_y(8), wl_w(1140), wl_h(16), "#2a2723")
        _wl_put(parts, wl_x(28), wl_y(18), wl_w(1118), wl_h(422), "#1c1916")
        # Brick rows (sparse so the screen stays light)
        brick_colors = ("#2a2420", "#26211d", "#231e1b", "#251f1c")
        row = 0
        by = wl_y(24)
        while by < wl_y(420):
            col = 0
            bx = wl_x(36) + (wl_w(20) if row % 2 else 0)
            while bx < wl_x(1140):
                _wl_put(parts, bx, by, wl_w(38), wl_h(12), brick_colors[(col + row) % 4])
                bx += wl_w(42)
                col += 1
            by += wl_h(16)
            row += 1
        for px, pw in ((48, 22), (368, 28), (714, 28), (1060, 22)):
            _wl_put(parts, wl_x(px), wl_y(36), wl_w(pw), wl_h(384), "#24211d")
        _wl_put(parts, wl_x(18), wl_y(420), wl_w(1140), wl_h(20), "#2c2a26")
        _wl_put(parts, wl_x(18), wl_y(420), wl_w(1140), wl_h(4), "#3a3732")

        # Street
        _wl_put(parts, 0, wl_y(440), WL_VIEW_W, wl_h(360), "#1a1b20")
        _wl_put(parts, 0, wl_y(440), wl_w(1148), wl_h(126), "#2a2b30")
        _wl_put(parts, 0, wl_y(562), wl_w(1148), wl_h(6), "#323338")
        _wl_put(parts, 0, wl_y(568), wl_w(1148), wl_h(10), "#3a3b40")
        _wl_put(parts, 0, wl_y(578), WL_VIEW_W, wl_h(222), "#141518")
        _wl_put(parts, 0, wl_y(548), wl_w(1164), wl_h(8), "#30323c")
        _wl_put(parts, 0, wl_y(550), wl_w(1164), wl_h(2), "#5a5c68")

        # Alley mouth / exit
        _wl_put(parts, wl_x(1148), wl_y(440), wl_w(132), wl_h(138), "#0c0d12")
        _wl_put(parts, wl_x(1148), wl_y(210), wl_w(132), wl_h(368), "#00000048")
        _wl_put(parts, wl_x(1204), wl_y(390), wl_w(8), wl_h(56), "#2a4a38")
        _wl_put(parts, wl_x(1204), wl_y(382), wl_w(12), wl_h(12), "#6aaa6a")

        # Lamp post near start
        _wl_put(parts, wl_x(108), wl_y(432), wl_w(6), wl_h(140), "#2a2a28")
        _wl_put(parts, wl_x(96), wl_y(426), wl_w(30), wl_h(6), "#3a382e")
        _wl_put(parts, wl_x(40), wl_y(500), wl_w(140), wl_h(70), "#d2b46e22")

        args = []
        for pos, disp in parts:
            args.append(pos)
            args.append(disp)
        args.append((wl_x(1168), wl_y(18)))
        args.append(Text("●", size=36, color="#c8c4b0"))
        args.append((wl_x(1178), wl_y(14)))
        args.append(Text("●", size=32, color="#07080e"))
        args.append((wl_x(1188), wl_y(448)))
        args.append(Text("EXIT", size=16, color="#889988"))
        return Composite((WL_VIEW_W, WL_VIEW_H), *args)

    def wl_background():
        if _wl_bg_cache[0] is None:
            _wl_bg_cache[0] = wl_build_background()
        return _wl_bg_cache[0]

    def wl_window_frame(win, watching, empty=False):
        """Interior + frame + sill for one bay (glass drawn after NPCs)."""
        x, y, w, h = wl_x(win["x"]), wl_y(win["y"]), wl_w(win["w"]), wl_h(win["h"])
        parts = []
        _wl_put(parts, x, y, w, h, "#07080c")
        if empty:
            _wl_put(parts, x + wl_w(16), y + wl_h(20), w - wl_w(32), h - wl_h(48), "#161820b3")
        elif watching:
            _wl_put(parts, x, y, w, h, "#5a371c8c")
        else:
            _wl_put(parts, x, y, w, h, "#12141c80")
        args = []
        for pos, disp in parts:
            args.append(pos)
            args.append(disp)
        return Composite((WL_VIEW_W, WL_VIEW_H), *args)

    def wl_window_glass(win, watching):
        x, y, w, h = wl_x(win["x"]), wl_y(win["y"]), wl_w(win["w"]), wl_h(win["h"])
        parts = []
        glass = "#b48c4620" if watching else "#14182466"
        _wl_put(parts, x, y, w, h, glass)
        _wl_put(parts, x + wl_w(4), y + wl_h(4), w - wl_w(8), h - wl_h(8), "#00000000")
        frame = "#3e3b36"
        _wl_put(parts, x, y, w, wl_h(8), frame)
        _wl_put(parts, x, y + h - wl_h(8), w, wl_h(8), frame)
        _wl_put(parts, x, y, wl_w(8), h, frame)
        _wl_put(parts, x + w - wl_w(8), y, wl_w(8), h, frame)
        mullion = "#d2a05059" if watching else "#32364280"
        _wl_put(parts, x + w // 2 - 1, y + wl_h(8), 2, h - wl_h(16), mullion)
        sill = "#4a4030" if watching else "#32302c"
        sill_hi = "#6a5a40" if watching else "#45423c"
        _wl_put(parts, x - wl_w(8), y + h, w + wl_w(16), wl_h(12), sill)
        _wl_put(parts, x - wl_w(8), y + h, w + wl_w(16), wl_h(3), sill_hi)
        if watching:
            _wl_put(parts, x - wl_w(6), y + h + wl_h(10), w + wl_w(12), wl_h(8), "#dc8a4622")
        args = []
        for pos, disp in parts:
            args.append(pos)
            args.append(disp)
        return Composite((WL_VIEW_W, WL_VIEW_H), *args)

    def wl_silhouette(w, h, body, head, eyes=None, facing=1):
        w = int(w)
        h = int(h)
        parts = []
        leg_w = max(6, w // 5)
        leg_h = max(10, h // 5)
        _wl_put(parts, int(w * 0.22), h - leg_h, leg_w, leg_h, "#15141a")
        _wl_put(parts, int(w * 0.58), h - leg_h, leg_w, leg_h, "#15141a")
        body_w = int(w * 0.72)
        body_h = int(h * 0.55)
        _wl_put(parts, int((w - body_w) / 2), h - leg_h - body_h + 4, body_w, body_h, body)
        head_w = int(w * 0.42)
        head_h = int(h * 0.22)
        hx = int((w - head_w) / 2)
        hy = int(h * 0.08)
        _wl_put(parts, hx, hy, head_w, head_h, head)
        _wl_put(parts, hx - 1, hy - 2, head_w + 2, max(4, head_h // 3), "#121014")
        if eyes:
            eye = max(3, w // 12)
            eye_y = hy + head_h // 2 - eye // 2
            off = 3 if facing >= 0 else -3
            _wl_put(parts, hx + head_w // 2 - eye - 2 + off, eye_y, eye, eye, eyes)
            _wl_put(parts, hx + head_w // 2 + 2 + off, eye_y, eye, eye, eyes)
        args = []
        for pos, disp in parts:
            args.append(pos)
            args.append(disp)
        child = Composite((w, h), *args)
        if facing < 0:
            child = Transform(child, xzoom=-1, xanchor=0.5, xpos=w // 2)
        return child

    def wl_fallback_body(w, h):
        return wl_silhouette(w, h, body="#1c1e28", head="#5a5348", eyes=None, facing=1)

    def wl_player_child():
        h = wl_h(WINDOW_LANE_PLAYER_H)
        w = wl_w(WINDOW_LANE_PLAYER_W)
        if wl_player_art_loaded():
            path = WL_STAND_PATH
            if renpy.store.window_lane_moving:
                walks = wl_walk_paths_loaded()
                if walks:
                    idx = int(float(renpy.store.window_lane_walk_t) / 0.12) % len(walks)
                    path = walks[idx]
            return Transform(path, ysize=h, nearest=True)
        return wl_fallback_body(w, h)

    def wl_sentry_child():
        w = wl_w(WINDOW_LANE_PACER_W + 4)
        h = wl_h(WINDOW_LANE_PACER_H + 8)
        return wl_silhouette(w, h, body="#1c1a22", head="#2a241e", eyes="#e8c070", facing=1)

    def wl_pacer_child(watching):
        w = wl_w(WINDOW_LANE_PACER_W)
        h = wl_h(WINDOW_LANE_PACER_H)
        facing = 1 if int(renpy.store.window_lane_pacer_dir) >= 0 else -1
        eyes = "#f0c878" if watching else None
        return wl_silhouette(w, h, body="#222018", head="#2c261e", eyes=eyes, facing=facing)


# ---------------------------------------------------------------------------
# Gameplay screen — this IS the level. jump window_lane to play.
# ---------------------------------------------------------------------------

screen window_lane_scene():
    modal True
    zorder 80

    add wl_background()

    # Window interiors (A always warm / watched, B depends on pacer, C empty)
    add wl_window_frame(WINDOW_LANE_WINDOWS[0], True, empty=False)
    add wl_window_frame(WINDOW_LANE_WINDOWS[1], window_lane_pacer_watching(), empty=False)
    add wl_window_frame(WINDOW_LANE_WINDOWS[2], False, empty=True)

    # Sentry — static in window A, facing out, eyes/glow
    $ _wa = WINDOW_LANE_WINDOWS[0]
    viewport:
        xpos wl_x(_wa["x"])
        ypos wl_y(_wa["y"])
        xsize wl_w(_wa["w"])
        ysize wl_h(_wa["h"])
        draggable False
        mousewheel False
        scrollbars None
        add Solid("#d2964666"):
            xanchor 0.5
            yanchor 0.5
            xpos wl_w(_wa["w"]) // 2
            ypos wl_h(_wa["h"]) - wl_h(90)
            xsize wl_w(90)
            ysize wl_h(110)
        add wl_sentry_child():
            xanchor 0.5
            yanchor 1.0
            xpos wl_w(_wa["w"]) // 2
            ypos wl_h(_wa["h"]) - wl_h(8)

    # Pacer — clipped to window B; glow only when watching
    $ _wb = WINDOW_LANE_WINDOWS[1]
    $ _pacer_watch = window_lane_pacer_watching()
    viewport:
        xpos wl_x(_wb["x"])
        ypos wl_y(_wb["y"])
        xsize wl_w(_wb["w"])
        ysize wl_h(_wb["h"])
        draggable False
        mousewheel False
        scrollbars None
        if _pacer_watch:
            add Solid("#d2964666"):
                xanchor 0.5
                yanchor 0.5
                xpos wl_x(window_lane_pacer_x + WINDOW_LANE_PACER_W * 0.5) - wl_x(_wb["x"])
                ypos wl_y(WINDOW_LANE_PACER_Y + WINDOW_LANE_PACER_H * 0.4) - wl_y(_wb["y"])
                xsize wl_w(90)
                ysize wl_h(110)
        add wl_pacer_child(_pacer_watch):
            xanchor 0.5
            yanchor 1.0
            xpos wl_x(window_lane_pacer_x + WINDOW_LANE_PACER_W * 0.5) - wl_x(_wb["x"])
            ypos wl_y(WINDOW_LANE_PACER_Y + WINDOW_LANE_PACER_H) - wl_y(_wb["y"])

    add wl_window_glass(WINDOW_LANE_WINDOWS[0], True)
    add wl_window_glass(WINDOW_LANE_WINDOWS[1], _pacer_watch)
    add wl_window_glass(WINDOW_LANE_WINDOWS[2], False)

    # Watched street bands
    for _win in WINDOW_LANE_WINDOWS:
        if window_lane_window_watching(_win):
            add Solid("#b45a2818"):
                xpos wl_x(_win["x"])
                ypos wl_y(WINDOW_LANE_STREET_Y - 18)
                xsize wl_w(_win["w"])
                ysize wl_h(16)

    # Click-to-move: street / ground only. Reclick replaces dest.
    button:
        xpos 0
        ypos wl_y(WINDOW_LANE_CLICK_Y)
        xsize WL_VIEW_W
        ysize WL_VIEW_H - wl_y(WINDOW_LANE_CLICK_Y)
        background Solid((0, 0, 0, 1))
        action Function(window_lane_click_street)

    # Destination marker
    if abs(window_lane_dest_x - window_lane_player_x) > 1.0:
        add Transform(Solid("#ffcc44", xsize=14, ysize=14), rotate=45):
            xpos wl_x(window_lane_dest_x)
            ypos wl_y(WINDOW_LANE_STREET_Y)
            xanchor 0.5
            yanchor 0.5

    # Player — Y planted on the sidewalk. Crouch ducks with yzoom 0.62.
    add Solid("#00000059"):
        xpos wl_x(window_lane_player_x)
        ypos wl_y(WINDOW_LANE_STREET_Y + 2)
        xanchor 0.5
        yanchor 0.5
        xsize wl_w(28)
        ysize wl_h(6)
    add wl_player_child():
        id "wl_player"
        xpos wl_x(window_lane_player_x)
        ypos wl_y(WINDOW_LANE_STREET_Y)
        xanchor 0.5
        yanchor 1.0
        xzoom window_lane_facing
        yzoom (WINDOW_LANE_CROUCH_SCALE_Y if player_crouched else 1.0)

    # HUD — stock game feel
    frame:
        background Solid((0, 0, 0, 160))
        padding (12, 10)
        xalign 0.0
        yalign 0.0
        offset (20, 20)
        xminimum 248

        vbox:
            spacing 6
            if player_crouched:
                text "Crouched" size 22 color "#ffcc44"
            else:
                text "Standing" size 22 color "#cccccc"
            textbutton ("Stand" if player_crouched else "Crouch"):
                action Function(toggle_crouch)
                text_size 20
                text_color "#eeeeee"
                xfill True
                background Solid("#333333")
                hover_background Solid("#0099cc")
                padding (12, 8)
            text "C to toggle. Crouch before a watched window." size 14 color "#888899"

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

    key "c" action Function(toggle_crouch)
    key "C" action Function(toggle_crouch)
    key "K_c" action Function(toggle_crouch)

    timer 0.016 repeat True action Function(window_lane_step)
    if window_lane_outcome:
        timer 0.01 action Return(window_lane_outcome)


label window_lane:
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
    $ window_lane_prepare()
    call screen window_lane_scene
    if _return == "caught":
        jump window_lane_caught
    jump window_lane_clear


label window_lane_caught:
    window_lane_voice "“Hey! What are you doing out there?”"
    "They’ve seen you on the sidewalk."
    menu:
        "Try again":
            jump window_lane
        "Leave":
            jump rooftop_a_1


label window_lane_clear:
    "You slip past the windows."
    menu:
        "Again":
            jump window_lane
        "Return to rooftop":
            jump rooftop_a_1
