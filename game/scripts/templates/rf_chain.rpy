# ---------------------------------------------------------------------------
# RF CHAIN — several background images, each with its own node map
#
# Use this when one “level” is a sequence (or graph) of rooms:
#   room A (bg + route + points) → exit → room B (bg + route + points) → …
#
# HOW TO AUTHOR (copy this file → e.g. game/RF/my_dungeon.rpy)
#   1. One 1920×1080 image per room under game/images/maps/…
#   2. Per room: start, route, interact points (same fields as RF single)
#   3. Define exits that swap the active room (bg + route + points + teleport)
#   4. Entry label loads the entry room and jumps rf_play
#
# LIVE EXAMPLE
#   Rooftop A is already a three-room chain:
#     rooftop_a_1 / rooftop_a_2 / rooftop_a_3 in game/RF/rooftop_a_levels.rpy
#   Each key has its own bg + route + start; jump rooftop_a_N to enter that room.
#
# TARGET AUTHORING SHAPE (preferred for new levels)
#
#   init python:
#       RF_LEVELS["my_level"] = {
#           "entry": "room_a",
#           "rooms": {
#               "room_a": {
#                   "bg": "maps/my_level/a.jpg",
#                   "start": (x, y),
#                   "route": "my_level_route_a",   # store name of default route list
#                   "points": "my_level_points_a", # store name of points list (or inline)
#               },
#               "room_b": {
#                   "bg": "maps/my_level/b.jpg",
#                   "start": (x, y),
#                   "route": "my_level_route_b",
#                   "points": "my_level_points_b",
#               },
#           },
#           # Optional explicit exits (also doable as interact points that jump):
#           "exits": {
#               ("room_a", "east"): "room_b",
#               ("room_b", "west"): "room_a",
#           },
#       }
#
# RUNTIME LIBRARY (buildalpha)
#   rf_register_room / rf_register_chain in game/RF/library_loader.rpy
#   Enter: jump rooftop_a  or  $ rf_enter_chain("rooftop_a")
#   Swap:  $ rf_chain_exit("rooftop_a_2")
#   Catalog: library/manifest.json + LIBRARY.md
#
# ENGINE — do not edit follower_controller to add rooms.
# ---------------------------------------------------------------------------
# FILL ME
#   level id:     my_level
#   rooms:        room_a, room_b, …
#   per room:     bg, start, route list, points list
#   entry room:   room_a
#   exits:        interact point → jump other room’s enter label
# ---------------------------------------------------------------------------

label template_rf_chain:

    "RF chain — several backgrounds, each with its own node map."

    "Copy game/scripts/templates/rf_chain.rpy. Model new chains on rooftop_a_1 → _2 → _3."

    "Live demo: entering the rooftop chain at room 1. Jump rooftop_a_2 / rooftop_a_3 for the other rooms."

    jump rooftop_a_1
