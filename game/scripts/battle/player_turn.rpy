label player_turn:

    $ deck.draw_cards(player.draw_cards)

    show screen player_end_turn

    jump player_hand


label player_hand:

    python:
        for enemy in list(enemies.enemies):
            if enemy.health <= 0:
                enemies.hide(enemy)

    if enemies.dead():
        jump win

    if player.health <= 0:
        jump lose

    call screen player_hand


screen player_hand():

    draggroup:
        for enemy in enemies.enemies:
            if enemy.health > 0:
                drag:
                    drag_name enemy.id
                    draggable False
                    droppable True
                    focus_mask True
                    idle_child Solid((0, 0, 0, 0), xsize=enemy.width, ysize=enemy.height)
                    selected_idle_child enemy.image("hover")
                    xalign enemies.xalign_position(enemy)
                    yalign Enemies.YALIGN

        for card in deck.hand:
            drag:
                as draggable
                drag_name card.id
                dragged ondrag
                droppable False
                drag_raise False
                pos card.get_pos()
                use card_frame(card, draggable)

        drag:
            drag_name player.id
            draggable False
            droppable True
            focus_mask True
            idle_child Solid((0, 0, 0, 0), xsize=player.width, ysize=player.height)
            selected_idle_child player.image("hover")
            xalign player.XALIGN
            yalign player.YALIGN


init python:
    def ondrag(drags, drop) -> None:
        """
        Handle dropping a card on a character.

        Card animations use renpy.pause(), which cannot run inside the
        screen interaction that owns this drag callback.  We therefore
        run card.use() inside a new context via invoke_in_new_context.
        """
        drag = drags[0]
        card_id = drag.drag_name
        card = deck.get_card(card_id)

        if not drop:
            drag.snap(card.get_xpos(), card.get_ypos(), 0.2)
            return

        character_id = drop.drag_name
        target = None
        if player.id == character_id:
            target = player
        elif character_id:
            target = enemies.get(character_id)

        if target is not None:
            # New context so play_action / play_attack / play_special can pause
            renpy.invoke_in_new_context(card.use, target)

        # Snap back if the card was not consumed (e.g. not enough energy)
        if card in deck.hand:
            drag.snap(card.get_xpos(), card.get_ypos(), 0.2)

        renpy.jump("player_hand")
