# ---------------------------------------------------------------------------
# Fight instances — one-off battles (separate from the arena level ladder)
# ---------------------------------------------------------------------------

default battle_mode = "arena"       # "arena" | "instance"
default current_fight_id = None


init python:
    FIGHTS = {
        "promoter_bout": {
            "scene": "bg plain",
            "on_win": "rooftop_a_1",
            "on_lose": "lose",
            "enemies": [
                {
                    "name": "Rookie",
                    "image": "boy",
                    "health": 18,
                    "actions": [
                        {"say": "{name} glares at you."},
                        {
                            "say": "{name} kicks for 2 damage!",
                            "attack": 2,
                            "anim": "kick",
                        },
                        {
                            "say": "{name} throws a poison dart! You are poisoned.",
                            "attack": 1,
                            "anim": "cast",
                            "status": "poisoned",
                            "status_duration": 3,
                            "status_stacks": 1,
                        },
                        {
                            "say": "{name} lands a stunning blow!",
                            "attack": 1,
                            "anim": "punch",
                            "stun": True,
                            "stun_duration": 1,
                        },
                        {
                            "say": "{name} heals 1 health.",
                            "heal": 1,
                            "anim": "raise_hand",
                        },
                    ],
                },
            ],
        },
    }

    def get_fight(fight_id):
        return FIGHTS.get(fight_id)

    def start_fight(fight_id):
        """Set instance mode and jump into battle (call from a label)."""
        if fight_id not in FIGHTS:
            renpy.notify("Unknown fight: {}".format(fight_id))
            return
        renpy.store.battle_mode = "instance"
        renpy.store.current_fight_id = fight_id
        renpy.jump("battle")

    def clear_fight_mode():
        renpy.store.battle_mode = "arena"
        renpy.store.current_fight_id = None

    def fight_on_win_label():
        fid = renpy.store.current_fight_id
        data = FIGHTS.get(fid) or {}
        return data.get("on_win", "rooftop_a_1")


label start_fight_instance(fight_id):
    $ battle_mode = "instance"
    $ current_fight_id = fight_id
    jump battle
