# ---------------------------------------------------------------------------
# Template index — designer jump hub (debug HUD → Templates).
# Copy a file from this folder; do not replace the live examples it points at.
# Assets (images, audio) live under game/images/ and game/audio/ — not here.
# ---------------------------------------------------------------------------

label template_index:

    $ quick_menu = False

    hide screen rf_map
    hide screen rf_cinematic
    hide screen test_world
    hide screen city_rf_map
    $ lock_plyr_cntrl = False

    hide screen player_end_turn
    hide screen player_stats
    hide screen player_money
    hide screen player_deck
    hide screen enemy_stats0
    hide screen enemy_stats1
    hide screen enemy_stats2
    hide screen enemy_stats3

    $ renpy.scene(layer="enemies")
    $ renpy.scene(layer="fx")
    scene bg plain with fade

    $ show_hud()

    "Level templates — copy a file, fill FILL ME, play. Assets stay in game/images/."

    menu:
        "What kind of level?"

        "Standard Ren'Py dialogue":
            jump template_vn

        "RF — single image":
            jump template_rf_single

        "RF — chain of images":
            jump template_rf_chain

        "Single battle":
            jump template_battle_single

        "Battle arena":
            jump template_battle_arena

        "Extras…":
            jump template_index_extras

        "Back to rooftop":
            jump rooftop_a_1


label template_index_extras:

    menu:
        "Extra demos"

        "Cover lane (stealth)":
            jump cover_lane

        "City map":
            jump city_map

        "Vespera patrol":
            jump vespera_patrol

        "Back":
            jump template_index
