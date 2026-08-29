# VN example. Fork game/scripts/templates/vn_scene.rpy
# Pattern: hide leftover battle UI, scene, show_hud, Character + dialogue + menu.
# Live label: jail (lose-state cell). Intro is in start.rpy.

label jail:

    # Clear any leftover battle UI
    hide screen player_end_turn
    hide screen player_stats
    hide screen player_money
    hide screen enemy_stats0
    hide screen enemy_stats1
    hide screen enemy_stats2
    hide screen enemy_stats3

    $ renpy.scene(layer="enemies")
    $ renpy.scene(layer="fx")
    scene bg jail with fade

    # Restore health to 10% of max (at least 1)
    $ player.health = max(1, int(player.health_max * 0.1))

    $ show_hud()

    # Placeholder full-body character sprite
    show boy idle at center with dissolve

    "You wake up in a cold cell."

    "Bars. Stone. The echo of distant footsteps."

    "This is the end of the road… for now."

    menu:
        "What now?"

        "Return to intro":
            hide boy
            jump intro

        "Accept your fate":
            hide boy
            $ hide_hud()
            jump end
