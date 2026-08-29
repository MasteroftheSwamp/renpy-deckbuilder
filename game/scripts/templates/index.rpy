# ---------------------------------------------------------------------------
# Template index — designer jump hub (debug HUD → Templates).
# Copy files from this folder; do not replace the live examples they point at.
# ---------------------------------------------------------------------------

label template_index:

    $ quick_menu = False

    # Leave the overworld map behind (same pattern as intro)
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

    "Designer templates — copy a file, fill in the fields, play."

    menu:
        "What do you want to author?"

        "VN scene":
            jump template_vn

        "RF map":
            jump template_rf

        "Fight instance":
            jump template_fight

        "Arena fight":
            jump template_arena

        "Cover lane":
            jump cover_lane

        "City map":
            jump city_map

        "Back to rooftop":
            jump rooftop_a_1
