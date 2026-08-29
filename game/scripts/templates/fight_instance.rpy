# ---------------------------------------------------------------------------
# Fight instance template — a named one-off battle.
#
# Instance vs arena:
#   battle_mode "instance" — named one-off; does not advance levels.level.
#   battle_mode "arena"    — ladder in levels.json; win calls levels.next().
#
# Live example: promoter_bout in game/scripts/data/fights.rpy
# Do not break promoter_bout. Copy this file (or the dict below) for a new id.
#
# WHAT TO UPDATE
#   - id          FIGHTS key (template_bout → your_id)
#   - scene       e.g. "bg plain"
#   - on_win      label after victory (e.g. "rooftop_a_1")
#   - on_lose     label after defeat (e.g. "lose")
#   - enemies[]   name, image, health, actions
#
# Action keys:
#   say, attack, heal,
#   anim (kick / punch / slash / cast / raise_hand),
#   status + status_duration + status_stacks,
#   stun + stun_duration
#
# Images live under game/images/enemies/ (boy, girl, …).
#
# How to start:
#   $ start_fight("your_id")
#   or jump start_fight_instance with fight_id
#   or Jump from an RF point (see fight_promoter on rooftop_a_1)
# ---------------------------------------------------------------------------

init 1 python:
    # Commented duplicate of promoter_bout — distinguishable say lines.
    # Guard so a second copy of this file does not overwrite a live entry.
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


label template_fight:
    $ start_fight("template_bout")
    # start_fight already jumps battle; if it returns, jump rooftop_a_1
    jump rooftop_a_1
