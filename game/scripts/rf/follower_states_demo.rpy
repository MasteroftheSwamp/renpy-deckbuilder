################################################################################
## Posture demo — jump follower_states_demo
##
## Shows screen follower_states_overlay (zorder 60, not modal) then jumps into
## the existing rooftop (rf_play). Buttons target rooftop_a_follower and, if
## present, test_follower so both update. Key C toggles crouch.
################################################################################

init python:
    def rf_posture_targets():
        """Followers that should receive set_posture from the overlay."""
        targets = []
        for name in ("rooftop_a_follower", "test_follower"):
            f = getattr(renpy.store, name, None)
            if f is not None and callable(getattr(f, "set_posture", None)):
                targets.append(f)
        return targets

    def rf_set_posture_demo(name):
        n = 0
        for f in rf_posture_targets():
            f.set_posture(name)
            n += 1
        if n == 0:
            renpy.notify("No follower with set_posture (copy follower_states.rpy into game/RF/)")
        else:
            renpy.notify("posture = %s" % name)

    def rf_toggle_crouch_demo():
        n = 0
        for f in rf_posture_targets():
            f.toggle_crouch()
            n += 1
        if n == 0:
            renpy.notify("No follower with toggle_crouch")
        else:
            p = f.get_posture() if n else "?"
            renpy.notify("posture = %s" % p)

    def rf_overlay_posture_label():
        f = getattr(renpy.store, "rooftop_a_follower", None)
        if f is None:
            f = getattr(renpy.store, "test_follower", None)
        if f is None:
            return "—"
        gp = getattr(f, "get_posture", None)
        if callable(gp):
            try:
                return gp()
            except Exception:
                pass
        return str(getattr(f, "posture", "normal"))


screen follower_states_overlay():
    zorder 60
    # Not modal — map clicks pass through empty space.

    key "c" action Function(rf_toggle_crouch_demo)
    key "C" action Function(rf_toggle_crouch_demo)

    frame:
        xalign 0.0
        yalign 1.0
        xoffset 12
        yoffset -12
        background "#000000cc"
        padding (14, 12)

        vbox:
            spacing 6
            text "Posture" size 18 color "#FFFFFF"
            text "now: [rf_overlay_posture_label()]" size 13 color "#FFD27A"
            textbutton "Normal" text_size 16 action Function(rf_set_posture_demo, "normal")
            textbutton "Crouch" text_size 16 action Function(rf_set_posture_demo, "crouch")
            textbutton "Injured" text_size 16 action Function(rf_set_posture_demo, "injured")
            textbutton "Handcuffed" text_size 16 action Function(rf_set_posture_demo, "handcuffed")
            text "C — toggle crouch" size 12 color "#AAAAAA"


label follower_states_demo:
    python:
        _show = getattr(renpy.store, "show_hud", None)
        if callable(_show):
            _show()
    show screen follower_states_overlay
    if renpy.has_label("rf_play"):
        jump rf_play
    elif renpy.has_label("rooftop_a_1"):
        jump rooftop_a_1
    "Posture overlay is up. No rf_play / rooftop_a_1 label — add the Route Follower rooftop map to walk around."
    $ renpy.pause(modal=False, hard=True)
