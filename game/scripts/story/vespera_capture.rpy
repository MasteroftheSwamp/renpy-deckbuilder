# VN capture beat. Fork of game/scripts/templates/vn_scene.rpy
# Lose path for fight instance vespera_ambush. Explicit on-screen; not fade-to-black.
# Live label: vespera_capture

label vespera_capture:

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
    $ player.hide()

    scene bg rooftop night with fade

    $ player.health = max(1, int(player.health_max * 0.1))
    $ show_hud()

    show vespera combat hit at center with dissolve

    "The suppressor charge dumps her on the roof. Gold boots scrape. The short cape twists under her back."

    dr_hale "Heart rate spiking. Good. Stay awake, Vespera — I want you to feel the cuffs seat."

    hide vespera
    scene bg lab with fade
    show vespera capture struggle at center with dissolve

    "White sleeves. Steel. He wrenches her gauntlets together. The lock bites over the gold stars on her wrists."

    vespera "Get — off — me."

    menu:
        "The cuffs are on. What does she do?"

        "Yank until the chain screams":
            vespera "You don’t get to keep me."
            "She hauls. Metal rings. The high-cut leotard splits further at her hip; a gold gauntlet edge gouges her own thigh."
            dr_hale "Struggle all you like. The alloy is rated for those boots kicking, too."

        "Drive a gold heel into his ribs":
            "The boot connects. He grunts, catches her ankle, and wrenches her down onto both knees."
            dr_hale "Forty-one, not frail. Kick again and I’ll cuff the other end to the vent pipe."
            vespera "Do it. I’ll still spit."

        "Go still and let him work":
            "She stops fighting. He notices. Fingers slide under the torn violet at her navel and test the fabric."
            dr_hale "Obedient? No — exhausted. That’s fine. I can cut."
            "The remaining strap over her sternum parts. Cool air. The mask stays. Everything else is his problem now."
            hide vespera
            show vespera body at center with dissolve
            "He makes her stand. Lab-white light on skin. Twenty-six, athletic, cuffed, and very much on display."
            vespera "Look your fill. Then unlock me."
            dr_hale "In time."

    hide vespera
    show vespera capture kneel at center with dissolve

    "Knees on tar paper. Wrists locked in front. The leotard is a wreck — tears at the ribs, the hip, the deep V gone wider than the designer ever meant."

    dr_hale "Elena Voss. I read the thesis. Cute. The suit is better science than the paper."

    menu:
        "He’s close enough to smell the sedative on his breath."

        "Headbutt the glasses":
            "Bone meets frame. He swears, fist in her ponytail, and yanks her head back."
            dr_hale "That’s a bruise you’ll keep. Hands behind."
            "He spins the cuffs, threads them through a belt loop of his own coat, then behind her back. Shoulders burn."

        "Tell him the truth":
            vespera "You’re not walking off this roof with me."
            dr_hale "I’m walking you to the van. Hands behind — now."
            "He recuffs her at the small of her back. The short cape is a joke of coverage. Gold boots scrape as he hauls her up."

        "Bite the fingers on her collar":
            "She sinks her teeth into the glove. He hisses, backhands her — not hard enough to drop her, hard enough to make the point."
            dr_hale "Feral. Noted. Hands behind the back, heroine."
            "The second cuffing is rougher. Chain short. Chin up because he fists the ponytail until she looks at him."

    hide vespera
    show vespera capture stand at center with dissolve

    "Standing. Mask on. Hands locked behind. Torn violet, gold scuffed, ponytail yanked crooked."

    dr_hale "Beautiful work. Don’t go anywhere — the van is in the alley."

    "He takes the stairs. She counts to four, then works the left gauntlet like a wrench against the cuff until something gives."

    vespera "Not your van. Not tonight."

    $ vespera_suit_damaged = True

    hide vespera with dissolve
    $ show_hud()
    jump vespera_patrol
