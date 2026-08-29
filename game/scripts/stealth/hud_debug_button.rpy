# ---------------------------------------------------------------------------
# Optional HUD debug entry — DO NOT overwrite hud.rpy
#
# The playable level works from `jump window_lane` alone. This file is only
# comments plus a copy-paste block showing how to add a textbutton to the
# existing `screen hud()` (game/scripts/utils/hud.rpy). Paste the block inside
# that screen, playtest, then delete it. Do not replace the real HUD file.
# ---------------------------------------------------------------------------
#
# --- copy from here --------------------------------------------------------
#
#     # DEBUG: window-lane sneak (remove me)
#     textbutton "Window lane":
#         action Jump("window_lane")
#         xalign 0.0
#         yalign 1.0
#         offset (20, -20)
#         text_size 20
#         text_color "#eeeeee"
#         background Solid((0, 0, 0, 160))
#         hover_background Solid("#0099cc")
#         padding (12, 8)
#
# --- copy to here (paste inside screen hud()) ------------------------------
