label battle:

    # Quest: Fight in the arena — complete on entering battle
    $ quests.complete("fight_arena")

    $ hide_hud()

    hide screen player_money
    show screen player_stats

    $ levels.start()

    jump player_turn
