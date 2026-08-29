label battle:

    # Quest: Fight in the arena — complete on entering battle
    $ quests.complete("fight_arena")

    $ hide_hud()

    hide screen player_money
    show screen player_stats

    # Fight-start hook: vitality/stamina/strength → Player health/energy/attack.
    if getattr(renpy.store, "life_sim", None):
        $ life_sim.apply_to_player(player)

    $ levels.start()

    jump player_turn
