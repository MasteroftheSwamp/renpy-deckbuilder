# ---------------------------------------------------------------------------
# VN scene template — a visual-novel beat.
#
# A VN beat is: scene + character + dialogue + menu + jump.
# Duplicate jail / intro as a NEW scene. Do not replace jail.rpy.
#
# WHAT TO UPDATE
#   - scene image          (bg plain, bg jail, …)
#   - character name/color (define template_vn_char — rename when you copy)
#   - dialogue lines       (smart quotes: What’s, you’re)
#   - menu choices         and their jump targets
#   - whether to show_hud() / hide leftover battle screens
#
# Copy this file, rename the label / Character, fill the fields, jump it
# from an RF point, a menu, or the HUD Templates button.
# Live examples: game/scripts/story/jail.rpy, intro in start.rpy
# ---------------------------------------------------------------------------

define template_vn_char = Character("Template Speaker", color="#66c1e0")


label template_vn:

    # Leave the overworld map behind
    hide screen rf_map
    hide screen rf_cinematic
    hide screen test_world
    $ lock_plyr_cntrl = False

    # Clear leftover battle UI
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

    $ show_hud()

    show boy idle at center with dissolve

    template_vn_char "This is a placeholder beat. Copy this file and fill in the fields."

    template_vn_char "Replace my name, colour, and these lines."

    "The scene image, menu choices, and jump targets are listed at the top of this file."

    template_vn_char "When you’re done, jump back to the rooftop — or loop this beat."

    menu:
        "What’s next?"

        "Continue":
            hide boy
            jump rooftop_a_1

        "Another beat":
            jump template_vn
