label lose:

    $ levels.end()

    hide screen player_end_turn
    hide screen player_stats
    hide screen player_money

    hide screen enemy_stats0
    hide screen enemy_stats1
    hide screen enemy_stats2
    hide screen enemy_stats3

    # Clear battle sprites (empty the layer — no full-screen black)
    $ renpy.scene(layer="enemies")
    $ renpy.scene(layer="fx")
    $ player.hide()

    # Resolve opponent name + which pre-declared side bust to use
    python:
        opponent_name = "Opponent"
        opponent_side = "opponent"  # maps to image "side opponent"

        if enemies.enemies:
            foe = enemies.enemies[0]
            opponent_name = foe.name or "Opponent"
            img = getattr(foe, "image_name", "") or ""
            # Only switch to a variant that was declared at init
            if img in ("boy", "girl"):
                opponent_side = f"opponent_{img}"  # side opponent_boy / side opponent_girl

    # Defeat background
    scene bg defeat with fade

    pause 1.0

    # Character image tag must match the "side <tag>" image name
    $ opponent = Character(opponent_name, image=opponent_side, color="#ee4b2b")

    opponent "You lose."

    opponent "How disappointing. Did you really think you could win?"

    jump jail
