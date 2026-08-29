# ---------------------------------------------------------------------------
# City overworld — Route Finder map (static token + location pins).
#
#     jump city_map
#
# Does not patch follower_controller.rpy. Playable city example of a
# click-to-pathfind overworld with location icons (not the rooftop android).
#
# HOW TO ADD ANOTHER LOCATION ICON
#   1. Drop a pin PNG in game/images/rf/ (transparent bg, ~48–72px). Distinct
#      from rf/city_player.png.
#   2. Append a dict to city_points (copy the alleyway block below):
#        name          unique string
#        point         (x, y) — MUST sit on a city_route node
#        label         a travel label you write (copy city_travel_alley)
#        active        True
#        detected      False
#        once          False to allow every visit, True for one-shot
#        map_sprite    "rf/<your_pin>.png"
#   3. Write that travel label: yes → hide screen city_rf_map, jump the
#      destination; no → rf_resume_walk, stay on this map.
#   4. city_map_markers() already draws every active map_sprite — no screen
#      edit needed for a new pin.
#   5. radius (optional, default CITY_HIT_RADIUS) — click/arrive this many
#      pixels from the pin still counts. Rooftop stays at 10.
#
# HOW TO ADD A STREET
#   Append a polyline to city_route:
#       {"points": [[x, y], ...], "color": "#FF0000", "editing": False, "connected": False}
#   Paint that same centerline on game/images/maps/city/map_city.png (1920x1080).
#   Grid used here: XS = [240, 640, 960, 1280, 1680], YS = [280, 540, 800]
#   START = (240, 800)   ALLEY = (1680, 280)
#
# NEVER name an init-python loop variable `_p` (shadows Ren'Py `_p()` and
# crashes gui.about). Use `_pt` or `_point`.
# NEVER put `background` on a `viewport`.
# Do NOT add another `label start`.
# ---------------------------------------------------------------------------

default city_route = [
    {"points": [[240, 280], [640, 280], [960, 280], [1280, 280], [1680, 280]], "color": "#FF0000", "editing": False, "connected": False},
    {"points": [[240, 540], [640, 540], [960, 540], [1280, 540], [1680, 540]], "color": "#FF0000", "editing": False, "connected": False},
    {"points": [[240, 800], [640, 800], [960, 800], [1280, 800], [1680, 800]], "color": "#FF0000", "editing": False, "connected": False},
    {"points": [[240, 280], [240, 540], [240, 800]], "color": "#FF0000", "editing": False, "connected": False},
    {"points": [[640, 280], [640, 540], [640, 800]], "color": "#FF0000", "editing": False, "connected": False},
    {"points": [[960, 280], [960, 540], [960, 800]], "color": "#FF0000", "editing": False, "connected": False},
    {"points": [[1280, 280], [1280, 540], [1280, 800]], "color": "#FF0000", "editing": False, "connected": False},
    {"points": [[1680, 280], [1680, 540], [1680, 800]], "color": "#FF0000", "editing": False, "connected": False},
]

default city_rl = RouteLines(lines=[], width=2)

# directional_mode "1" uses key "idle". Duplicate the static token onto
# stand_*/walk_* so the posture wrap cannot KeyError.
default city_token_lib = {
    "idle": {"image": Transform("rf/city_player.png"), "xoff": 0, "yoff": 0},
    "stand_u": {"image": Transform("rf/city_player.png"), "xoff": 0, "yoff": 0},
    "stand_h": {"image": Transform("rf/city_player.png"), "xoff": 0, "yoff": 0},
    "stand_d": {"image": Transform("rf/city_player.png"), "xoff": 0, "yoff": 0},
    "walk_u": {"image": Transform("rf/city_player.png"), "xoff": 0, "yoff": 0},
    "walk_h": {"image": Transform("rf/city_player.png"), "xoff": 0, "yoff": 0},
    "walk_d": {"image": Transform("rf/city_player.png"), "xoff": 0, "yoff": 0},
}

default city_follower = FollowerDisplayable(
    Follower(turn=True, directional_mode="1", speed=350, route=city_rl, img_id=city_token_lib)
)

default city_points = [
    {
        "name": "alleyway",
        "point": (1680, 280),
        "label": "city_travel_alley",
        "active": True,
        "detected": False,
        "once": False,
        "map_sprite": "rf/loc_alley.png",
        "radius": 47,
    },
]


init python:
    CITY_HIT_RADIUS = 47

    def city_map_markers():
        """Like rf_map_markers, but reads city_follower.interact_points."""
        fdisp = getattr(renpy.store, "city_follower", None)
        if fdisp is None:
            return []
        out = []
        try:
            pts = fdisp.follower.interact_points or []
        except Exception:
            pts = []
        for _pt in pts:
            if not _pt.get("active", True):
                continue
            spr = _pt.get("map_sprite")
            if not spr:
                continue
            out.append((_pt, spr))
        return out

    def city_load():
        load_predefined_route(renpy.store.city_rl, renpy.store.city_route)
        for _pt in renpy.store.city_points:
            if not _pt.get("once") or _pt.get("active", True):
                _pt["detected"] = False
        renpy.store.city_follower.load_interact_points(renpy.store.city_points)
        renpy.store.city_follower.set_teleport(240, 800, renpy.store.city_follower.route.lines)
        renpy.store.city_follower.reset_follower()
        # Arrive/click radius (~1/3 of the original 140) so nearby still counts.
        renpy.store.city_follower.interact_radius = CITY_HIT_RADIUS

    def city_go_to(name):
        """Pathfind to a named city_points pin (used by the large click pads)."""
        if getattr(renpy.store, "lock_plyr_cntrl", False):
            return
        fdisp = getattr(renpy.store, "city_follower", None)
        if fdisp is None:
            return
        for _pt in getattr(renpy.store, "city_points", []) or []:
            if _pt.get("name") != name:
                continue
            if not _pt.get("active", True):
                return
            _x, _y = _pt["point"]
            fdisp.set_destination(_x, _y, fdisp.route.lines)
            return


label city_map:
    window hide
    $ show_hud()
    hide screen rf_map
    hide screen test_world
    hide screen editor_world
    hide screen city_rf_map
    $ city_load()
    show screen city_rf_map
    $ renpy.pause(modal=False, hard=True)


screen city_rf_map:
    zorder 0

    add "maps/city/map_city.png"

    # Routes only visible if dev_mode (RouteLines already gates the draw).
    add city_rl

    # Location icons BEHIND the player
    for _mk in city_map_markers():
        $ _mk_pt, _mk_spr = _mk
        $ _mk_x, _mk_y = _mk_pt["point"]
        add _mk_spr:
            xpos int(_mk_x)
            ypos int(_mk_y)
            xanchor 0.5
            yanchor 1.0

    # Must fill the screen so LMB click-to-move works (same as rooftop).
    add city_follower

    # Large click pads sit ON TOP of the follower so a near-miss on a pin
    # still paths to it. Drawn after city_follower so they get the event.
    for _mk in city_map_markers():
        $ _mk_pt, _mk_spr = _mk
        $ _mk_x, _mk_y = _mk_pt["point"]
        $ _hit = int(_mk_pt.get("radius") or CITY_HIT_RADIUS)
        button:
            xpos int(_mk_x)
            ypos int(_mk_y)
            xanchor 0.5
            yanchor 0.5
            xsize _hit * 2
            ysize _hit * 2
            background Solid((0, 0, 0, 1))
            action Function(city_go_to, _mk_pt["name"])
            focus_mask None

    text "CITY" size 14 color "#88ccee" xpos 20 ypos 6


label city_travel_alley:
    $ rf_active_point = rf_get_trigger_point()
    $ lock_plyr_cntrl = True
    $ rf_pause_walk()
    window show
    menu:
        "Travel to alleyway?"
        "Yes":
            $ lock_plyr_cntrl = False
            python:
                try:
                    city_follower.stop_follower()
                except Exception:
                    pass
            hide screen city_rf_map
            hide screen rf_map
            window hide
            jump rooftop_a_1
        "No":
            window hide
            $ rf_resume_walk()
            $ lock_plyr_cntrl = False
            $ renpy.pause(modal=False, hard=True)
