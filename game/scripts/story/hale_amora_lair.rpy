# ---------------------------------------------------------------------------
# Hale's Lair — opening VN beat (first level).
#
#     jump hale_amora_lair
#
# Uses chamber CGs (bg hale amora chamber 01–11) + side busts via
# dr_hale / amora Character image tags.
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

    # Soft HUD for a pure VN open; still reachable if needed
    $ show_hud()

    # --- INT. HALE'S LAIR – NIGHT ---
    scene bg hale amora chamber 01 with fade

    "A large, dimly lit chamber. Multiple screens. Soft blue light from the monitors is the only real illumination."

    scene bg hale amora chamber 02 with dissolve

    "Hale paces aggressively in front of the largest screen. He stops, slams a fist onto the console."

    dr_hale angry "Every plan. Every single time. That heroine bitch—"

    "He spins toward the desk."

    scene bg hale amora chamber 03 with dissolve

    "Amora is reclining in a chair, boots casually crossed on the desk. She slowly swirls a glass of dark liquid, watching him with mild amusement rather than concern."

    amora amused "Such rage, darling. You'll give yourself an aneurysm before she ever does. Try breathing. Or wine. Or both."

    scene bg hale amora chamber 04 with dissolve

    dr_hale angry "Don't. I've spent months—resources, people, entire operations—and she swats them aside like insects. Look at her. Look how effortless it is for her."

    scene bg hale amora chamber 05 with dissolve

    amora cold "Then stop throwing insects at her."

    scene bg hale amora chamber 06 with dissolve

    "She stands, walks slowly behind him,"

    scene bg hale amora chamber 07 with dissolve

    "and rests her hands lightly on his shoulders, speaking close to his ear."

    amora smirk "You're thinking too small. Robberies. Heists. Distracted. She's a problem solver. Give her a problem, she solves it."

    amora cold "What if we stop giving her problems… and start making her the problem?"

    scene bg hale amora chamber 08 with dissolve

    "Hale turns his head slightly, interest cutting through the anger."

    dr_hale surprised "Capture her."

    scene bg hale amora chamber 09 with dissolve

    amora sadistic "Not just capture. Break her. Publicly. Privately. Whatever it takes so the city watches their precious Vespera fall and never get back up."

    scene bg hale amora chamber 10 with dissolve

    "She steps around to face him, expression sharper now."

    amora smirk "I already have the first pieces in place. A lure she won't be able to ignore… and a cage that even her little shadow tricks won't open easily."

    scene bg hale amora chamber 11 with dissolve

    "Hale stares at the screen one last time, then slowly smiles—cold and vicious."

    dr_hale smug "Then let's begin."

    jump hale_amora_lair_end


label hale_amora_lair_end:

    # Hand off into the rooftop patrol slice
    scene black with fade
    jump vespera_patrol
