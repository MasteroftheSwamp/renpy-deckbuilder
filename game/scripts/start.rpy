label start:

    $ quick_menu = False  # hide bottom menu

    # Fresh run state
    $ levels.restart()
    $ inventory.clear()
    $ quests.set_active("fight_arena")
    $ reset_arena_entrance()

    # HUD visible from the very beginning (overworld + intro)
    $ show_hud()

    # Enter the route-finder overworld
    jump rooftop_a_1


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

    # Clear sprite/FX layers (do NOT fill them with black — that covers the BG)
    $ renpy.scene(layer="enemies")
    $ renpy.scene(layer="fx")
    scene bg plain with fade

    # HUD should already be up from start / overworld; ensure it is
    $ show_hud()

    "Welcome to the arena."

    "Prove yourself in battle — or fall and face the consequences."

    menu:
        "Ready?"

        "Enter battle":
            jump battle

        "Leave":
            # Return to the overworld map
            jump return_to_overworld


label return_to_overworld:
    """
    Re-enter the route-finder map from intro / other story labels.
    """
    $ show_hud()
    jump rooftop_a_1
