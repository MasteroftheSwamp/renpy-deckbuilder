# ---------------------------------------------------------------------------
# Vespera patrol — rooftop RF slice (clone of rooftop_a_1 with new points).
#
#     jump vespera_patrol
#
# Engine: game/RF/follower_controller.rpy — DO NOT EDIT.
# Reuses rooftop-a map 1 + rooftop_a_route_1 + rooftop_a_follower.
# Registers as RF_ROOFTOP_A["vespera_patrol"] and wraps rf_load_rooftop.
# ---------------------------------------------------------------------------

define vespera = Character("Vespera", color="#b56cff")
define dr_hale = Character("Dr. Hale", color="#7aa3b8")

default vespera_suit_damaged = False
default vespera_intro_seen = False

default vespera_points = [
    {
        "name": "vespera_lookout",
        "point": (1106.7857142857142, 948.2142857142857),
        "label": "vespera_lookout",
        "active": True,
        "detected": False,
        "once": False,
        "map_sprite": "vespera/token.png",
    },
    {
        "name": "vespera_ambush",
        "point": (1818.2142857142856, 1047.857142857143),
        "label": "vespera_ambush_talk",
        "active": True,
        "detected": False,
        "once": False,
        "char_name": "Dr. Hale",
        "map_sprite": "rf/placeholders/npc_marker.png",
        "side_image": "rf/placeholders/npc_side.png",
    },
]


init 1 python:
    RF_ROOFTOP_A["vespera_patrol"] = {
        "bg": "maps/rooftop-a/map_rooftop-a_1.jpg",
        "route": "rooftop_a_route_1",
        "start": (838.9285714285714, 950.3571428571428),
    }

    if "vespera_ambush" not in FIGHTS:
        FIGHTS["vespera_ambush"] = {
            "scene": "bg rooftop night",
            "on_win": "vespera_patrol",
            "on_lose": "vespera_capture",
            "enemies": [
                {
                    "name": "Dr. Hale",
                    "image": "hale",
                    "health": 16,
                    "actions": [
                        {"say": "{name} flicks a suppressor cuff from his sleeve."},
                        {
                            "say": "{name} snaps a calibrated cuff-shot for 2 damage!",
                            "attack": 2,
                            "anim": "cast",
                        },
                        {
                            "say": "{name} floods the air with sedative mist. You are poisoned.",
                            "attack": 1,
                            "anim": "cast",
                            "status": "poisoned",
                            "status_duration": 3,
                            "status_stacks": 1,
                        },
                        {
                            "say": "{name} tags a gauntlet with a stun charge!",
                            "attack": 1,
                            "anim": "punch",
                            "stun": True,
                            "stun_duration": 1,
                        },
                        {
                            "say": "{name} injects a stabilizer and heals 1 health.",
                            "heal": 1,
                            "anim": "raise_hand",
                        },
                    ],
                },
            ],
        }

    _rf_load_rooftop_base = rf_load_rooftop

    def rf_load_rooftop(level_id):
        if level_id != "vespera_patrol":
            _rf_load_rooftop_base(level_id)
            return

        info = RF_ROOFTOP_A[level_id]
        renpy.store.current_rf_level = level_id
        route = getattr(renpy.store, info["route"])
        start = info["start"]

        load_predefined_route(renpy.store.rooftop_a_rl, route)
        for _pt in renpy.store.vespera_points:
            if not _pt.get("once") or _pt.get("active", True):
                _pt["detected"] = False
        renpy.store.rooftop_a_follower.load_interact_points(renpy.store.vespera_points)
        renpy.store.rooftop_a_follower.set_teleport(
            start[0], start[1], renpy.store.rooftop_a_follower.route.lines
        )
        renpy.store.rooftop_a_follower.reset_follower()

        try:
            if getattr(renpy.store, "vespera_suit_damaged", False):
                renpy.store.rooftop_a_follower.set_posture("injured")
            else:
                renpy.store.rooftop_a_follower.set_posture("normal")
        except Exception:
            pass

        load_predefined_route(renpy.store.interactive_line, route)
        renpy.store.test_follower.load_interact_points(
            renpy.store.rooftop_a_follower.follower.interact_points
        )
        renpy.store.test_follower.set_teleport(
            start[0], start[1], renpy.store.test_follower.route.lines
        )
        renpy.store.test_follower.reset_follower()


label vespera_patrol:
    if not vespera_intro_seen:
        hide screen rf_map
        hide screen rf_cinematic
        hide screen test_world
        hide screen city_rf_map
        $ lock_plyr_cntrl = False
        $ renpy.scene(layer="enemies")
        $ renpy.scene(layer="fx")
        scene bg rooftop night with fade
        $ show_hud()
        show vespera stand at center with dissolve
        "Night patrol. Elena Voss — twenty-six, violet suit, gold mask. Walk the roof."
        "The gold pin is a lookout. The far-right marker is trouble."
        $ vespera_intro_seen = True
        hide vespera with dissolve
    $ current_rf_level = "vespera_patrol"
    jump rf_play


label vespera_lookout:
    call rf_point_begin
    $ lock_plyr_cntrl = True

    if vespera_suit_damaged:
        show screen rf_cinematic("vespera damaged", dim=0.55, zoom=1.0)
        "The gold star clasp hangs by a thread. The violet leotard is split at the hip and over her ribs."
        vespera "Still me. Still twenty-six. Suit’s a wreck — I’m not."
        "Wind finds every new tear. She keeps the mask on anyway."
    else:
        show screen rf_cinematic("vespera stand", dim=0.45, zoom=0.85)
        "Night city. Violet high-cut, gold gauntlets, short cape snapping at her calves."
        vespera "Elena Voss on paper. Vespera on the roof. The grid shouldn’t be this quiet."
        "She rolls a gold-booted heel on the ledge and watches the dark blocks below."

    hide screen rf_cinematic
    jump rf_point_end


label vespera_ambush_talk:
    $ rf_active_point = rf_get_trigger_point()
    $ lock_plyr_cntrl = True
    $ rf_pause_walk()

    show screen rf_cinematic("vespera combat idle", dim=0.4, zoom=1.0)

    dr_hale "Vespera. I’ve been measuring that suit for weeks."
    vespera "You’re the one killing the grid."
    dr_hale "Dr. Hale. Forty-one. Independent lab. Those gauntlets will take my cuffs beautifully."
    vespera "Try it."

    hide screen rf_cinematic
    $ lock_plyr_cntrl = False
    $ rooftop_a_follower.stop_follower()
    hide screen rf_map
    hide screen rf_cinematic

    $ start_fight("vespera_ambush")
    jump vespera_patrol
