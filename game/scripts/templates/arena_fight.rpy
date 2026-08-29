# ---------------------------------------------------------------------------
# Arena ladder template — sequential fights keyed "0", "1", … in levels.json.
#
# Arena vs instance:
#   battle_mode must be "arena" (not "instance").
#   levels.start() builds enemies from Levels.get() — or generate() for
#   missing keys. After a win, levels.next() advances the ladder.
#   A fight instance (promoter_bout) does NOT advance levels.level.
#
# Live example: game/scripts/data/levels.json + game/scripts/battle/battle.rpy
# Fork: copy a block into game/scripts/data/levels.json (do not edit this
# label unless you are jumping into a specific ladder index).
#
# WHAT TO UPDATE (in levels.json)
#   - key            "0", "1", … (string)
#   - scene          e.g. "bg plain"
#   - enemies[]      name, image, health
#   - authored       actions[] like level "0" (say / attack / heal / anim /
#                    status / stun)
#   - procedural     attack_min / attack_max / heal_min / heal_max like "1"
#
# Commented JSON example (comments only — not Python, not live JSON):
#
#   # Authored actions (like "0"):
#   # "2": {
#   #   "scene": "bg plain",
#   #   "enemies": [
#   #     {
#   #       "name": "Challenger",
#   #       "image": "girl",
#   #       "health": 12,
#   #       "actions": [
#   #         { "say": "{name} studies your stance..." },
#   #         { "say": "{name} slashes for 2 damage.", "attack": 2, "anim": "slash" },
#   #         { "say": "{name} heals 1 health.", "heal": 1, "anim": "raise_hand" }
#   #       ]
#   #     }
#   #   ]
#   # }
#   #
#   # Procedural attack_min/max (like "1"):
#   # "3": {
#   #   "scene": "bg plain",
#   #   "enemies": [
#   #     {
#   #       "name": "Guy",
#   #       "image": "boy",
#   #       "health": 10,
#   #       "attack_min": 2,
#   #       "attack_max": 4,
#   #       "heal_min": 1,
#   #       "heal_max": 2
#   #     }
#   #   ]
#   # }
# ---------------------------------------------------------------------------

label template_arena:
    $ battle_mode = "arena"
    $ current_fight_id = None
    $ levels.level = 0
    jump battle
