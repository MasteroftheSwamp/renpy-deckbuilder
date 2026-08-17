label start:

    $ quick_menu = False  # hide bottom menu

    # Fresh run state
    $ levels.restart()
    $ inventory.clear()
    $ quests.set_active("fight_arena")

    jump intro


label intro:

    $ quick_menu = False

    hide screen player_end_turn
    hide screen player_stats
    hide screen player_money
    hide screen player_deck
    hide screen enemy_stats0
    hide screen enemy_stats1
    hide screen enemy_stats2
    hide screen enemy_stats3

    scene black onlayer enemies
    scene bg plain with fade

    $ show_hud()

    "Welcome to the arena."

    "Prove yourself in battle — or fall and face the consequences."

    menu:
        "Ready?"

        "Enter battle":
            jump battle

        "Leave":
            $ hide_hud()
            jump end
