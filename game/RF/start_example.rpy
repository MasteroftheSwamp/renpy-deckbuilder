## EXAMPLE TEST WORLD ##
default route_line_test = [ ## SAVED ROUTE FROM EDITOR ##
    {'points': [[166, 303], [255, 184], [439, 151], [640, 122], [963, 154], [1095.0, 129.5], [1227, 105], [1375, 186], [1474.089549707437, 303.9247533708342], [1496, 330], [1562.5, 414.0], [1629, 498], [1654.7403059223427, 615.0571055039875], [1671, 689], [1655, 835], [1536, 891], [1273, 886], [1009, 807], [881, 790], [727, 768], [544, 696], [386, 716], [237, 608], [166, 467]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[166, 467], [166, 303]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[640, 122], [777.2634299427727, 306.05778105962713], [816, 358], [959, 510], [1110, 643], [1248, 731], [1311.6824309585097, 756.2809650538807], [1447, 810]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[1447, 810], [1536, 891]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[963, 154], [977, 203], [829, 291], [777.2634299427727, 306.05778105962713]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[1095.0, 129.5], [1038, 328], [1002, 472]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[1002, 472], [959, 510]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[1038, 328], [1167, 319], [1326, 338], [1424, 334], [1474.089549707437, 303.9247533708342]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[1562.5, 414.0], [1508, 435], [1311, 487], [1132, 506]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[1132, 506], [959, 510]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[1311, 487], [1347, 583], [1351, 636], [1326, 727], [1311.6824309585097, 756.2809650538807]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[1351, 636], [1481, 617], [1654.7403059223427, 615.0571055039875]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[881, 790], [905, 671], [928, 605]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[928, 605], [959, 510]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[905, 671], [794, 661], [681, 605], [667, 578]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[667, 578], [959, 510], [796, 478], [632, 475], [491, 473], [228, 350]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[386, 716], [485, 640]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[485, 640], [667, 578]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[228, 350], [166, 303]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[491, 473], [474, 359], [510, 274], [569, 182]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[569, 182], [640, 122]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[237, 608], [382, 529]], 'color': '#FF0000', 'editing': False, 'connected': False},
    {'points': [[382, 529], [491, 473]], 'color': '#FF0000', 'editing': False, 'connected': False}
]
default interactive_line = InteractiveRouteDisplayable(lines=[], width=2)
default test_follower = FollowerDisplayable(Follower(speed=400, route=interactive_line, img_id=android_lib))

default rl = RouteLines(lines=[], width=2)
default follower = FollowerDisplayable(Follower(turn=True, speed=400, route=rl, img_id=android_lib))
default persistent.dev_note = True
label start_example:
    $ selected_editor = "world"
    menu:
        "Run Test World(Free Form Examples)":
            jump test_world

        "Run Edit Route":
            jump start_example_cont
    $ renpy.pause(modal=False,hard=True)

label start_example_cont:
    if persistent.dev_note:
        "*This is a little note before you start - would you like to skip?*"
        menu:
            "*This is a little note before you start - would you like to skip?*"
            "Yes I've seen it already":
                pass

            "No let me see the note":
                "*Looking at start_example.rpy file-*"
                "*If you want to trace over a map route aka an image you created, you can add it by-*"
                "*Going into edit_world screen and adding the image in the screen below the route editor-*"
                "*You can also define a new follower and add it to the screen for testing-*"
                "*In order to use the special examples I made, you'll need to download the images here - {a=https://www.dropbox.com/scl/fo/qr0y4oqrpht1unxmy2iug/AJg9j8WQ5JDHUD1lqBdgI84?rlk...}(   HERE   ){/a}*"
                "*I do not own any of those images they are just for educational purposes to explain all the functions of the route follower*"

        menu:
            "Do you want to turn off this note in the future?"
            "Yes! (Recommended)":
                $ persistent.dev_note = False
            "Nah I wanna hear it again later":
                pass

    if selected_editor == "world":
        jump edit_world
    elif selected_editor == "route":
        jump edit_world2
    $ renpy.pause(modal=False,hard=True)

##----------------------------------------------------------------------------##
### TEST WORLD STUFF // EXAMPLES ###############################################
##----------------------------------------------------------------------------##
label test_world:
    window hide
    $ dev_mode = False
    $ light_togg = False
    $ wrench_togg = True
    $ show_hud()
    $ follower.load_interact_points(example_interact_points)
    $ load_predefined_route(rl, route_line_test)
    $ follower.set_teleport (962,507,follower.route.lines)
    # One-shot arena entrance: keep disabled if already used
    if arena_entrance_used:
        $ follower.togg_interact_point("arena_entrance", False)
    else:
        $ follower.togg_interact_point("arena_entrance", True)
    menu:
        "Would you like to use the independent horizontal images test? (Turn off auto flip image)"
        "Yes! Turn off auto flip! (follower.turn = False)":
            $ follower.turn = False
            $ follower.img_id = android2_lib
            "Ok look at the androids eyes to see it work!"
        "No! Keep auto flip on! (follower.turn = True)":
            $ follower.turn = True
            $ follower.img_id = android_lib
            "Ok the android will use a mirrored horizontal images!"
    $ follower.reset_follower()
    show screen test_world
    $ renpy.pause(modal=False,hard=True)

label set_center:
    $ renpy.pause(modal=False,hard=True)

label light_toggle:
    $ light_togg = True
    $ renpy.pause(modal=False,hard=True)

label wrench_grab:
    $renpy.notify("Wrench Picked Up")
    $ wrench_togg = False
    $ renpy.pause(modal=False,hard=True)

label stop_sign:
    $ lock_plyr_cntrl = True
    $ follower.pause_follower()
    "You wait at the stop sign"
    "{cps=15} . . ."
    $ follower.change_follower_act(act="angry")
    "Its taking a while . . ."
    "{cps=15} . . ."
    $ follower.change_follower_act(act="sad")
    "Almost there . . ."
    "{cps=15} . . ."
    $ follower.change_follower_act(act="happy")
    "Ok you can go now"
    $ follower.change_follower_dir(dir="down")
    $ renpy.pause(0.1,modal=False,hard=True)
    $ follower.play_follower()
    $ renpy.pause(0.1,modal=False,hard=True)
    $ lock_plyr_cntrl = False
    $ renpy.pause(modal=False,hard=True)


label enter_intro:
    # Arena entry from RF map / fight promoter
    $ mark_arena_entrance_used()
    $ lock_plyr_cntrl = False
    $ follower.stop_follower()
    $ rooftop_a_follower.stop_follower()
    hide screen rf_cinematic
    hide screen rf_map
    hide screen test_world
    hide screen editor_world
    jump intro


default example_interact_points = [
    {'name': 'point_1', 'point': (1637.510916459668, 536.7044058046804), 'label': 'wrench_grab', 'active': True, 'detected': False},
    {'name': 'point_2', 'point': (675.2557598324413, 747.6416104258785), 'label': 'stop_sign', 'active': True, 'detected': False},
    {'name': 'point_3', 'point': (338.8728287308628, 168.95759049935612), 'label': 'light_toggle', 'active': True, 'detected': False},
    # Arena entrance — walking here jumps to intro (one-shot via arena_entrance_used)
    {'name': 'arena_entrance', 'point': (1002.0, 472.0), 'label': 'enter_intro', 'active': True, 'detected': False},
]

default light_togg = False
default wrench_togg = False
##----------------------------------------------------------------------------##
### TEST WORLD STUFF // EXAMPLES ###############################################
##----------------------------------------------------------------------------##

label edit_world:
    window hide
    $ dev_mode = True
    $ test_follower.load_interact_points(example_interact_points) ## LOADS INTYERACT POINTS
    $ test_follower.togg_interact_point('point_1',False) ## MAKES INTEACT POINTS DISABLED
    $ test_follower.togg_interact_point('point_2',False) ## MAKES INTEACT POINTS DISABLED
    $ test_follower.togg_interact_point('point_3',False) ## MAKES INTEACT POINTS DISABLED
    $ load_predefined_route(interactive_line, route_line_test) ## LOADS ROUTE
    $ test_follower.set_teleport (962,507,test_follower.route.lines) ## TELEPORTS FOLLOWER TO ROUTE
    $ test_follower.reset_follower() ## RESETS FOLLOWERS IMAGE
    show screen editor_world
    $ renpy.pause(modal=False,hard=True)

screen test_world:
    zorder 0
    default follower_show = True
    default menu_hider = False
    add "RF/example images/map.png"
    if wrench_togg:
        add "RF/example images/map stuff/wrench.png" xoffset 1615 yoffset 500

    if light_togg:
        timer 1.5 action SetVariable("light_togg",False)
        add "RF/example images/map stuff/light_B.png" xoffset 264 yoffset 40
    else:
        add "RF/example images/map stuff/light_A.png" xoffset 264 yoffset 40

    add rl

    if follower_show:
        add follower

    add "RF/example images/map stuff/stop.png" xoffset 450 yoffset 550

    # Second stop sign — marks the arena entrance interact point
    if not arena_entrance_used:
        add "RF/example images/map stuff/stop.png" xoffset 777 yoffset 275

    vbox:
        xalign 1.0
        yalign 0.0
        if not menu_hider:
            textbutton _("MOVE FOLLOWER TO CENTER") text_idle_color "#2B5DBC" text_hover_color "#FFFFFF" xalign 1.0 action [Function(follower.set_reach,"set_center"),Function(follower.set_button_destination, 962,507, follower.route.lines)]
            textbutton _("Show follower // [follower_show]") text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0:
                if follower_show:
                    action SetScreenVariable("follower_show",False)
                else:
                    action SetScreenVariable("follower_show",True)
            textbutton _("DevMode// [dev_mode]//") text_idle_color "#36A839" text_hover_color "#5AFF49" action ToggleVariable("dev_mode",true_value=True,false_value=False) xalign 1.0
            textbutton _("Main Menu") action MainMenu() text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0
        textbutton _("HIDE MENU") text_size 15 text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0:
            if menu_hider:
                action SetScreenVariable("menu_hider",False)
            else:
                action SetScreenVariable("menu_hider",True)

#################################################################################

## EDIT WORLD CHANGE THIS BELOW TO CHANGE STUFF

#################################################################################
screen editor_world:
    zorder 0
    default follower_show = True
    default menu_hider = False
    add Solid("#262626") alpha 1.0

    add interactive_line


    if follower_show:
        add test_follower

    vbox:
        xalign 1.0
        yalign 0.0
        if not menu_hider:
            frame:
                xalign 1.0
                xysize(400, 55)
                background None
                add Transform(Solid("#000000", xysize=(400, 50)),alpha=0.95) xalign 1.0 yalign 0.5 xoffset 5
                text "Make sure to export the route/interact points, the data here will not auto save if you leave the editor." size 13 color "#FFFFFF" xalign 1.0 yalign 0.5
            frame:
                xalign 1.0
                xysize(416, 175)
                background None
                add Transform(Solid("#000000", xysize=(416, 175)),alpha=0.75)
                vbox:
                    xalign 0.0
                    yoffset 15
                    spacing 10
                    text "LMB - Select Point/Drag Point/Drag Line" size 12 color "#4070FF" yalign 0.0 yoffset 0 xoffset 5
                    text "RMB - Drop Point/Connect End Point/Add a point on a line" size 12 color "#4070FF" yalign 0.0 yoffset 0 xoffset 5
                    text "Del - Delete Hovered Point" size 12 color "#4070FF" yalign 0.0 yoffset 0 xoffset 5
                    text "Enter - Confirm Mesh/Deselect Mesh" size 12 color "#4070FF" yalign 0.0 yoffset 0 xoffset 5
                    text "Left Shift - Grid Magnet/Precise Alignment" size 12 color "#4070FF" yalign 0.0 yoffset 0 xoffset 5
                    text "Ctrl+RMB - Drop Interact Point {p}** {size=-2}Follower must be True or present to drop interact point" size 12 color "#4070FF" yalign 0.0 yoffset 0 xoffset 5
            textbutton _("Show follower // [follower_show]") text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0:
                if follower_show:
                    action SetScreenVariable("follower_show",False)
                else:
                    action SetScreenVariable("follower_show",True)
            textbutton _("DevMode// [dev_mode]//") text_idle_color "#36A839" text_hover_color "#5AFF49" action ToggleVariable("dev_mode",true_value=True,false_value=False) xalign 1.0
            textbutton _("Debug_Text// [debug_text_stuff]//") text_idle_color "#36A839" text_hover_color "#5AFF49" action ToggleVariable("debug_text_stuff",true_value=True,false_value=False) xalign 1.0
            textbutton _("Edit route Menu // [edit_route_menu]") action Function(toggle_edit_mode,interactive_line) text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0
            textbutton _("Poly route Dev // [poly_route_dev]") action Function(toggle_poly_route_mode) text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0
            textbutton _("Save Route") action Function(save_route,interactive_line) text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0
            textbutton _("Load Route") action Function(load_predefined_route, interactive_line, route_line_test) text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0
            textbutton _("Clear Route") action Function(clear_current_route, interactive_line) text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0
            textbutton _("Set Random Interact Point") action Function(test_follower.rando_drop_interact_point) text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0
            textbutton _("Save Interact Points") action Function(save_interact_points, test_follower) text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0
            textbutton _("Clear Interact Points") action Function(clear_interact_points, test_follower) text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0
            textbutton _("Main Menu") action MainMenu() text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0
        textbutton _("HIDE MENU") text_size 15 text_idle_color "#2B5DBC" text_hover_color "#00FFFF" xalign 1.0:
            if menu_hider:
                action SetScreenVariable("menu_hider",False)
            else:
                action SetScreenVariable("menu_hider",True)
