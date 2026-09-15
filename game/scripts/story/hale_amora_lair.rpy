# ---------------------------------------------------------------------------
# Hale's Lair — opening VN beat (first level).
#
#     jump hale_amora_lair
#
# Chamber CGs carry action/blocking; only spoken lines appear in the say box.
# After this beat: jump vespera_patrol (rooftop slice).
# ---------------------------------------------------------------------------

label hale_amora_lair:

    $ quick_menu = True

    hide screen rf_map
    hide screen rf_cinematic
    hide screen test_world
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

    $ show_hud()

    # --- INT. HALE'S LAIR – NIGHT ---
    scene bg hale amora chamber 01 with fade
    pause 0.6

    scene bg hale amora chamber 02 with dissolve

    dr_hale angry "Every plan. Every single time. That heroine bitch—"

    scene bg hale amora chamber 03 with dissolve

    amora amused "Such rage, darling. You'll give yourself an aneurysm before she ever does. Try breathing. Or wine. Or both."

    scene bg hale amora chamber 04 with dissolve

    dr_hale angry "Don't. I've spent months—resources, people, entire operations—and she swats them aside like insects. Look at her. Look how effortless it is for her."

    scene bg hale amora chamber 05 with dissolve

    amora cold "Then stop throwing insects at her."

    scene bg hale amora chamber 06 with dissolve
    pause 0.4
    scene bg hale amora chamber 07 with dissolve

    amora smirk "You're thinking too small. Robberies. Heists. Distracted. She's a problem solver. Give her a problem, she solves it."

    amora cold "What if we stop giving her problems… and start making her the problem?"

    scene bg hale amora chamber 08 with dissolve

    dr_hale surprised "Capture her."

    scene bg hale amora chamber 09 with dissolve

    amora sadistic "Not just capture. Break her. Publicly. Privately. Whatever it takes so the city watches their precious Vespera fall and never get back up."

    scene bg hale amora chamber 10 with dissolve

    amora smirk "I already have the first pieces in place. A lure she won't be able to ignore… and a cage that even her little shadow tricks won't open easily."

    scene bg hale amora chamber 11 with dissolve

    dr_hale smug "Then let's begin."

    jump hale_amora_lair_end


label hale_amora_lair_end:

    scene black with fade
    jump vespera_patrol
