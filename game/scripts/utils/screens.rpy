screen stat(name, current, max):
    text "[name]: [current]/[max]"
    bar value AnimatedValue(current, max):
        xsize 300


screen player_money():
    frame:
        background Solid((0, 0, 0, 100))
        text "Money: $[money]"
        xpos (40 if renpy.variant("web") else 0)


screen player_stats():
    vbox:
        yalign 1.0
        use player_deck(0, 0)
        frame:
            vbox:
                use stat("Health", player.health, player.health_max)
                null height 15
                use stat("Energy", player.energy, player.energy_max)
                if player.status_icons_text():
                    null height 10
                    text player.status_icons_text() size 28 xalign 0.5

    # Floating status icons above the player sprite
    if player.status_icons_text():
        text player.status_icons_text():
            size 36
            xalign player.XALIGN
            yalign 0.22


screen player_end_turn():
    frame:
        padding (10, 10)
        xalign 1.0
        yalign 1.0

        textbutton "End Turn":
            action Function(player.end_turn)


screen player_deck(xalign_pos, yalign_pos):
    frame:
        padding (10, 10)
        textbutton ("View Draw Pile" if levels.battle else "View Deck"):
            action Show("draw_pile")
        xalign xalign_pos
        yalign yalign_pos


screen tooltip():
    $ tooltip = GetTooltip()
    if tooltip:
        # Position the tooltip relative to the captured focus
        nearrect:
            focus "tooltip"
            prefer_top True
            frame:
                background Solid((255, 255, 255, 225))
                text tooltip color "#000"
                xalign 0.5


screen enemy_stats(enemy, xalign_pos):
    frame:
        background Solid((0, 0, 0, 50))
        xalign xalign_pos

        vbox:
            use stat("Health", enemy.health, enemy.health_max)

            button:
                action NullAction()
                text enemy.name
                tooltip (enemy.say() or "...")
                xalign 0.5

            if enemy.status_icons_text():
                null height 6
                text enemy.status_icons_text() size 26 xalign 0.5

    # Floating status icons above the enemy sprite
    if enemy.status_icons_text():
        text enemy.status_icons_text():
            size 36
            xalign xalign_pos
            yalign 0.22

    use tooltip


screen enemy_stats0(enemy, xalign_pos):
    use enemy_stats(enemy, xalign_pos)


screen enemy_stats1(enemy, xalign_pos):
    use enemy_stats(enemy, xalign_pos)


screen enemy_stats2(enemy, xalign_pos):
    use enemy_stats(enemy, xalign_pos)


screen enemy_stats3(enemy, xalign_pos):
    use enemy_stats(enemy, xalign_pos)


screen draw_pile():

    dismiss action Hide("draw_pile")

    frame:
        modal True
        padding (50, 50)
        xalign 0.5 yalign 0.5
        has vbox

        viewport:
            scrollbars "horizontal"
            ysize 450

            hbox:
                spacing 25
                for card in deck.draw_pile if levels.battle else deck.cards:
                    use card_frame(card)

        null height 50

        frame:
            xalign 0.5
            textbutton "Close":
                action Hide("draw_pile")


screen card_frame(card, draggable=None):
    frame:
        background Frame("cards/card.png")
        add card.image:
            xpos -5 ypos -5
            xysize card.WIDTH, card.HEIGHT
        label card.label_name():
            xalign 0.5
            ypos card.LABEL_NAME_YPOS
        label card.label_cost()
        label card.label_description():
            xalign 0.5
            ypos card.LABEL_DESCRIPTION_YPOS
            padding (5, 0)
        xysize card.WIDTH, card.HEIGHT

        if draggable:
            mousearea:
                area (0, 0, card.OFFSET, card.HEIGHT)
                hovered [
                    Queue(MUSIC_CHANNEL_UI, "ui/mouserelease1.ogg"),
                    Function(draggable.top),
                ]


# ---------------------------------------------------------------------------
# Special attack (JRPG-style) overlays
# ---------------------------------------------------------------------------

screen special_dim():
    add Solid("#000000") at special_dim


screen special_banner(title="SPECIAL ATTACK", colour="#ffcc00"):
    frame:
        at special_banner_slide
        background Solid((0, 0, 0, 200))
        xsize 900
        ysize 100
        xalign 0.5
        yalign 0.35
        padding (20, 10)

        text title:
            size 56
            color colour
            bold True
            xalign 0.5
            yalign 0.5
            outlines [(3, "#000000", 0, 0)]


screen special_cutin(image_name, is_player=True):
    if is_player:
        add image_name at special_cutin_player
    else:
        add image_name at special_cutin_enemy


screen special_impact():
    add Solid("#ffffff") at special_impact_flash
