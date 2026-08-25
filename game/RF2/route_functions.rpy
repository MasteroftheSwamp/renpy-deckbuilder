## ROUTE FOLLOWER FUNCTIONS ##

init python:
################################################################################
## ROUTE TOOLS ##
################################################################################

    import os
    import copy

    def load_predefined_route(route, predefined_route):
        """ LOADS THE DEFINED ROUTE TO THE DEFINED ROUTE CLASS """
        # Validate the predefined route
        if not isinstance(predefined_route, list) or not all(isinstance(line, dict) and 'points' in line for line in predefined_route):
            renpy.notify("Invalid route! - Please submit a correct route")
            return

        # Clear the existing lines and update with the predefined ones
        route.lines.clear()
        route.lines.extend(predefined_route)

        if dev_mode:
            renpy.notify("Route Loaded!")

    def disable_renpy_bind():
            ## REMOVES ALL RENPY BINDINGS EXCEPT FOR ONES INVOLVED FOR DIALOGUE AND MOUSE BUTTON - used in the dev menus
            """Remove all key bindings from config.keymap, except for the preserved keys."""
            preserved_keys = {
                "dismiss": ["K_RETURN", "K_SPACE", "K_KP_ENTER", "mouseup_1"],
                "button_select": ["K_RETURN", "K_KP_ENTER", "mouseup_1"],
                "drag_activate": ["mousedown_1"],
                "bar_activate": ["mousedown_1", "K_RETURN", "K_KP_ENTER"],
                "bar_deactivate": ["mouseup_1", "K_RETURN", "K_KP_ENTER"],
                "viewport_drag_start": ["mousedown_1"],
                "viewport_drag_end": ["mouseup_1"],
                "drag_activate": [ 'mousedown_1' ],
                "drag_deactivate": [ 'mouseup_1' ],
                "viewport_leftarrow": [ 'anyrepeat_K_LEFT', 'anyrepeat_KP_LEFT' ],
                "viewport_rightarrow": [ 'anyrepeat_K_RIGHT', 'anyrepeat_KP_RIGHT' ],
                "viewport_uparrow": [ 'anyrepeat_K_UP', 'anyrepeat_KP_UP' ],
                "viewport_downarrow": [ 'anyrepeat_K_DOWN', 'anyrepeat_KP_DOWN' ],
                "viewport_wheelup": [ 'mousedown_4' ],
                "viewport_wheeldown": [ 'mousedown_5' ],
                "viewport_pageup": [ 'anyrepeat_K_PAGEUP', 'anyrepeat_KP_PAGEUP' ],
                "viewport_pagedown": [ 'anyrepeat_K_PAGEDOWN', 'anyrepeat_KP_PAGEDOWN' ],
                "bar_activate": [ 'mousedown_1', 'K_RETURN', 'K_KP_ENTER', 'K_SELECT' ],
                "bar_deactivate": [ 'mouseup_1', 'K_RETURN', 'K_KP_ENTER', 'K_SELECT' ],
                "bar_left": [ 'anyrepeat_K_LEFT', 'anyrepeat_KP_LEFT' ],
                "bar_right": [ 'anyrepeat_K_RIGHT', 'anyrepeat_KP_RIGHT' ],
                "bar_up": [ 'anyrepeat_K_UP', 'anyrepeat_KP_UP' ],
                "bar_down": [ 'anyrepeat_K_DOWN', 'anyrepeat_KP_DOWN' ],
                "button_ignore": [ 'mousedown_1' ],
                "button_select": [ 'K_RETURN', 'K_KP_ENTER', 'K_SELECT', 'mouseup_1',  ],
                "button_alternate": [ 'mouseup_3' ],
                "button_alternate_ignore": [ 'mousedown_3' ],
            }

            # Clear all keymap bindings
            for key in config.keymap:
                config.keymap[key] = []

            # Reapply the preserved keys
            for key, bindings in preserved_keys.items():
                config.keymap[key] = bindings

            renpy.clear_keymap_cache()  # Ensure Ren'Py updates the keymap cache
################################################################################
################################################################################
