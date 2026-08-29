# ---------------------------------------------------------------------------
# RF map template — how to add a Route Finder map.
#
# Do NOT paste huge rooftop route coordinate arrays here.
# Walk the live rooftop while you read these comments: label template_rf
# jumps rooftop_a_1.
#
# Live example: game/RF/rooftop_a_levels.rpy + game/RF/rf_points.rpy
# Playable city example (static token + location pins): game/scripts/rf/city_map.rpy
# Engine:       game/RF/follower_controller.rpy
#               DO NOT EDIT follower_controller to add a map.
#
# HOW A NEW RF MAP IS ADDED
#   1. Maps are 1920x1080 images under game/images/maps/
#      (see maps/rooftop-a/map_rooftop-a_1.jpg).
#   2. Register in a dict like RF_ROOFTOP_A:
#        keys: bg, route (store name of the default route list), start (x, y)
#        start must sit on a path node.
#   3. default some_route = [
#          {"points": [[x, y], ...], "color": "#FF0000", "editing": False, "connected": False},
#      ]
#      Built in the RF editor (Save Route), not by hand.
#   4. default some_follower = FollowerDisplayable(
#          Follower(turn=True, speed=400, route=some_rl, img_id=android_lib)
#      )
#   5. Interact points list — copy the field list from rooftop_a_points_1:
#        name, point (x, y), label, active, detected, once
#        optional: char_name, map_sprite, side_image, lines,
#                  item_name, card_id, fullscreen_image, blur
#   6. Labels: one per map. rooftop_a_1 sets current_rf_level then jump rf_play.
#   7. rf_play loads the route, teleports the follower, show screen rf_map.
#   8. Do not edit follower_controller to add a map.
#
# POSTURE (game/RF/follower_states.rpy) — do not rewrite follower_controller:
#     rooftop_a_follower.set_posture("crouch")
#     rooftop_a_follower.set_posture("injured")
#     rooftop_a_follower.set_posture("handcuffed")
#     rooftop_a_follower.set_posture("normal")
#
# NEVER `for _p in ...` at init python — `_p` shadows Ren'Py’s translate helper
# and crashes gui.about. Use `_pt` or `_point`.
# NEVER put `background` on a viewport.
#
# EXAMPLE interact-point dict (one NPC). Paste into a new points list:
#
#     {
#         "name": "template_npc",
#         "point": (1106.7857142857142, 948.2142857142857),
#         "label": "rf_npc",
#         "active": True,
#         "detected": False,
#         "once": False,
#         "char_name": "Stranger",
#         "map_sprite": "rf/placeholders/npc_marker.png",
#         "side_image": "rf/placeholders/npc_side.png",
#         "lines": [
#             "Hey — copy this dict into your map’s points list.",
#         ],
#         # "item_name": "Strange Card",
#         # "card_id": "placeholder",
#         # "fullscreen_image": "rf/placeholders/show_fullscreen.png",
#         # "blur": True,
#     }
# ---------------------------------------------------------------------------

label template_rf:
    "This is the RF template — walking the live rooftop map."
    jump rooftop_a_1
