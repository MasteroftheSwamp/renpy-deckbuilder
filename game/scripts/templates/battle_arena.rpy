# ---------------------------------------------------------------------------
# BATTLE ARENA — ladder fights keyed "0", "1", … in levels.json
#
# battle_mode must be "arena". Win calls levels.next() and advances the ladder.
# A single named bout (battle_single) does NOT advance levels.level.
#
# HOW TO AUTHOR
#   1. Add / edit blocks in game/scripts/data/levels.json
#   2. Keys are strings: "0", "1", …
#   3. Each fight: scene + enemies[] (authored actions OR attack_min/max)
#   4. Jump template_battle_arena (or set battle_mode="arena" and jump battle)
#
# LIVE EXAMPLE: game/scripts/data/levels.json + game/scripts/battle/battle.rpy
#
# Authored actions example (comments only — edit the real JSON file):
#   "2": {
#     "scene": "bg plain",
#     "enemies": [{
#       "name": "Challenger", "image": "girl", "health": 12,
#       "actions": [
#         { "say": "{name} studies your stance..." },
#         { "say": "{name} slashes for 2 damage.", "attack": 2, "anim": "slash" }
#       ]
#     }]
#   }
#
# Procedural ranges example:
#   "3": {
#     "scene": "bg plain",
#     "enemies": [{
#       "name": "Guy", "image": "boy", "health": 10,
#       "attack_min": 2, "attack_max": 4, "heal_min": 1, "heal_max": 2
#     }]
#   }
# ---------------------------------------------------------------------------

label template_battle_arena:
    $ battle_mode = "arena"
    $ current_fight_id = None
    $ levels.level = 0
    jump battle
