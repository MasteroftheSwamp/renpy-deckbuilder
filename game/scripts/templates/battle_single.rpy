# ---------------------------------------------------------------------------
# BATTLE SINGLE — one-off named fight (not arena ladder)
#
# battle_mode "instance" — named bout; does NOT advance levels.level.
# For a ladder, use battle_arena.rpy instead.
#
# HOW TO AUTHOR
#   1. Copy this file (or paste the FIGHTS dict into game/scripts/data/fights.rpy)
#   2. Change id template_bout → your_id
#   3. Set scene, on_win, on_lose, enemies[]
#   4. Start with:  $ start_fight("your_id")
#      or jump template_battle_single after swapping the id
#
# LIVE EXAMPLE: promoter_bout in game/scripts/data/fights.rpy
# Images: game/images/enemies/ (boy, girl, hale, …)
#
# Action keys: say, attack, heal, anim (kick/punch/slash/cast/raise_hand),
#              status + status_duration + status_stacks, stun + stun_duration
# ---------------------------------------------------------------------------

init 1 python:
    if "template_bout" not in FIGHTS:
        FIGHTS["template_bout"] = {
            "scene": "bg plain",
            "on_win": "rooftop_a_1",
            "on_lose": "lose",
            "enemies": [
                {
                    "name": "Sparring Partner",
                    "image": "boy",
                    "health": 18,
                    "actions": [
                        {"say": "{name} sizes you up."},
                        {
                            "say": "{name} throws a test kick for 2 damage!",
                            "attack": 2,
                            "anim": "kick",
                        },
                        {
                            "say": "{name} flicks a practice dart. You are poisoned.",
                            "attack": 1,
                            "anim": "cast",
                            "status": "poisoned",
                            "status_duration": 3,
                            "status_stacks": 1,
                        },
                        {
                            "say": "{name} tags you with a stunning tap!",
                            "attack": 1,
                            "anim": "punch",
                            "stun": True,
                            "stun_duration": 1,
                        },
                        {
                            "say": "{name} catches a breath and heals 1 health.",
                            "heal": 1,
                            "anim": "raise_hand",
                        },
                    ],
                },
            ],
        }


label template_battle_single:
    $ start_fight("template_bout")
    jump rooftop_a_1
