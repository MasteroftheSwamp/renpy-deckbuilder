# ---------------------------------------------------------------------------
# Out-of-battle HUD + tabbed player menu
# ---------------------------------------------------------------------------

default menu_tab = "stats"


screen hud():
    zorder 50

    # ---- Top-left: health bar ----
    frame:
        background Solid((0, 0, 0, 160))
        padding (12, 10)
        xalign 0.0
        yalign 0.0
        offset (20, 20)

        vbox:
            spacing 6
            text "Health" size 22 color "#cccccc"
            hbox:
                spacing 10
                bar:
                    value AnimatedValue(player.health, player.health_max)
                    xsize 220
                    ysize 22
                    left_bar Solid("#cc3333")
                    right_bar Solid("#442222")
                text "[player.health]/[player.health_max]" size 22 yalign 0.5

    # ---- Top-right: menu button ----
    imagebutton:
        idle "gui/hud/menu.png"
        hover Transform("gui/hud/menu.png", matrixcolor=BrightnessMatrix(0.25))
        action Show("player_menu")
        xalign 1.0
        yalign 0.0
        offset (-20, 20)
        focus_mask True

    # ---- Top-right: quest tracker (below menu icon) ----
    frame:
        background Solid((0, 0, 0, 160))
        padding (12, 10)
        xalign 1.0
        yalign 0.0
        offset (-20, 100)
        xmaximum 320

        hbox:
            spacing 10
            add "gui/hud/quest_marker.png" yalign 0.0
            vbox:
                text "Quest" size 18 color "#aaaaaa"
                text "[quests.active_title()]" size 24 color "#ffcc44"


# ---------------------------------------------------------------------------
# Modal tabbed menu
# ---------------------------------------------------------------------------

screen player_menu():
    modal True
    zorder 100

    # Dim background; click does nothing (modal)
    add Solid("#000000aa")

    # Esc closes
    key "K_ESCAPE" action Hide("player_menu")

    frame:
        background Frame("gui/frame.png", 24, 24)
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 620
        padding (24, 20)

        vbox:
            spacing 12

            # Header
            hbox:
                xfill True
                text "Menu" size 40 color "#ffffff" yalign 0.5
                textbutton " ":
                    xalign 1.0
                    action Hide("player_menu")
                imagebutton:
                    idle "gui/hud/close.png"
                    hover Transform("gui/hud/close.png", matrixcolor=BrightnessMatrix(0.3))
                    action Hide("player_menu")
                    xalign 1.0

            # Tabs
            hbox:
                spacing 8
                use menu_tab_button("stats", "Stats", "gui/hud/tab_stats.png")
                use menu_tab_button("equipment", "Equipment", "gui/hud/tab_equipment.png")
                use menu_tab_button("items", "Items", "gui/hud/tab_items.png")
                use menu_tab_button("quest", "Quest", "gui/hud/tab_quest.png")

            null height 8

            # Tab body
            fixed:
                xsize 850
                ysize 480

                if menu_tab == "stats":
                    use menu_tab_stats
                elif menu_tab == "equipment":
                    use menu_tab_equipment
                elif menu_tab == "items":
                    use menu_tab_items
                else:
                    use menu_tab_quest


screen menu_tab_button(tab_id, label, icon):
    $ selected = (menu_tab == tab_id)
    button:
        xsize 160
        ysize 52
        background (Solid("#0099cc") if selected else Solid("#333333"))
        hover_background Solid("#66c1e0")
        action SetVariable("menu_tab", tab_id)
        padding (8, 6)

        hbox:
            spacing 8
            add icon yalign 0.5
            text label size 24 yalign 0.5


screen menu_tab_stats():
    vbox:
        spacing 18
        text "Character Stats" size 32

        use menu_stat_row("Health", player.health, player.health_max, "#cc3333")
        use menu_stat_row("Energy", player.energy, player.energy_max, "#66aadd")

        null height 10
        text "Money: $[money]" size 28
        text "Wins: [wins]" size 28
        text "Max health: [player.health_max]" size 24 color "#aaaaaa"
        text "Max energy: [player.energy_max]" size 24 color "#aaaaaa"


screen menu_stat_row(label, current, maximum, colour):
    vbox:
        spacing 4
        hbox:
            spacing 12
            text "[label]" size 26
            text "[current]/[maximum]" size 26 color colour
        bar:
            value AnimatedValue(current, maximum)
            xsize 500
            ysize 20
            left_bar Solid(colour)
            right_bar Solid("#333333")


screen menu_tab_equipment():
    vbox:
        spacing 12
        text "Equipment (Deck)" size 32
        text "Cards in your deck: [len(deck.cards)]" size 22 color "#aaaaaa"

        viewport:
            scrollbars "vertical"
            mousewheel True
            xsize 840
            ysize 400

            hbox:
                spacing 16
                box_wrap True
                xsize 820

                for card in deck.cards:
                    use card_frame(card)


screen menu_tab_items():
    vbox:
        spacing 12
        text "Items" size 32

        $ entries = inventory.list_entries()

        if not entries:
            text "Your inventory is empty." size 26 color "#888888"
        else:
            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 840
                ysize 400

                hbox:
                    spacing 16
                    box_wrap True
                    xsize 820

                    for item_def, count in entries:
                        use inventory_item_slot(item_def, count)

            use tooltip


screen inventory_item_slot(item_def, count):
    button:
        xsize 100
        ysize 120
        background Solid("#222222")
        hover_background Solid("#444444")
        padding (6, 6)
        action NullAction()
        tooltip "[item_def.name] ×[count]\n[item_def.description]"

        vbox:
            spacing 4
            xalign 0.5
            add item_def.icon xalign 0.5
            text "×[count]" size 20 xalign 0.5 color "#ffcc44"


screen menu_tab_quest():
    vbox:
        spacing 14
        text "Quest Log" size 32

        $ active = quests.get_active()
        if active:
            frame:
                background Solid("#1a1a22")
                padding (16, 14)
                xsize 800
                vbox:
                    spacing 8
                    text "Active" size 20 color "#88cc88"
                    text "[active.title]" size 34 color "#ffcc44"
                    text "[active.description]" size 26
        else:
            text "No quests right now." size 28 color "#888888"
            text "Check back when a new objective appears." size 22 color "#666666"

        null height 20
        text "Completed" size 24 color "#aaaaaa"
        $ any_done = False
        for qid, q in quests.quests.items():
            if q.status == "complete":
                $ any_done = True
                text "• [q.title]" size 24 color "#88aa88"
        if not any_done:
            text "• None yet" size 22 color "#666666"


# Helpers to show/hide HUD from labels
init python:
    def show_hud():
        renpy.show_screen("hud")

    def hide_hud():
        renpy.hide_screen("hud")
        renpy.hide_screen("player_menu")
