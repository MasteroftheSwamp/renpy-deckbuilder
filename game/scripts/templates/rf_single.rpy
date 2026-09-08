# ---------------------------------------------------------------------------
# RF SINGLE — one background image + one node map
#
# Use this when a level is a single walkable screen (one BG, one route graph).
#
# HOW TO AUTHOR (copy this file → e.g. game/RF/my_map.rpy)
#   1. Drop a 1920×1080 map under game/images/maps/… (assets stay out of templates/)
#   2. Fill the FILL ME block below (bg, start, route, points)
#   3. Register the room in a level dict (see schema)
#   4. Add a short label that sets current_rf_level and jumps rf_play
#   5. Wire an entry jump (menu, RF exit, VN beat, HUD)
#
# LIVE EXAMPLE
#   game/RF/rooftop_a_levels.rpy  (rooftop_a_1 is a single room)
#   game/RF/rf_points.rpy         (interact points for room 1)
#
# ENGINE — do not edit these to add a map
#   game/RF/follower_controller.rpy
#   game/RF/route_functions.rpy
#   screen rf_map / label rf_play
#
# ---------------------------------------------------------------------------
# FILL ME
#   map image:     maps/…/….jpg
#   start (x, y):  must sit on a route node
#   route lines:   from RF editor “Save Route” (do not hand-type huge arrays)
#   interact pts:  name, point, label, active, detected, once + optional fields
#   entry label:   my_map_enter → jump rf_play
# ---------------------------------------------------------------------------
#
# SCHEMA (one room)
#
#   default my_route = [
#       {"points": [[x, y], …], "color": "#FF0000", "editing": False, "connected": False},
#   ]
#
#   default my_points = [
#       {
#           "name": "npc_or_item_id",
#           "point": (x, y),
#           "label": "rf_npc",          # or rf_pickup / rf_dialogue / custom
#           "active": True,
#           "detected": False,
#           "once": False,
#           "char_name": "Name",
#           "map_sprite": "rf/placeholders/npc_marker.png",
#           "side_image": "rf/placeholders/npc_side.png",
#           "lines": ["Line one.", "Line two."],
#           # "item_name": "…", "card_id": "…", "fullscreen_image": "…", "blur": True,
#       },
#   ]
#
#   # Register like RF_ROOFTOP_A:
#   # "my_map": {"bg": "maps/…/….jpg", "route": "my_route", "start": (x, y)}
#   # Load points in rf_load_… when level_id == "my_map"
#
# NEVER `for _p in …` at init python — `_p` shadows Ren'Py’s translate helper.
# Use `_pt` or `_point`. Never put `background` on a viewport.
# ---------------------------------------------------------------------------

label template_rf_single:

    "RF single — one background, one node map."

    "Copy game/scripts/templates/rf_single.rpy, fill the FILL ME block, and register the room like rooftop_a_1."

    "Live demo: walking rooftop room 1 (single image)."

    jump rooftop_a_1
