transform position(xalign_position=0.5, yalign_position=1.0):
    xalign xalign_position
    yalign yalign_position


transform shake:
    ease .06 yoffset 24
    ease .06 yoffset -24
    ease .05 yoffset 20
    ease .05 yoffset -20
    ease .04 yoffset 16
    ease .04 yoffset -16
    ease .03 yoffset 12
    ease .03 yoffset -12
    ease .02 yoffset 8
    ease .02 yoffset -8
    ease .01 yoffset 4
    ease .01 yoffset -4
    ease .01 yoffset 0


transform lunge(home_x, target_x, duration=0.55, y=1.0):
    xalign home_x
    yalign y
    easein duration * 0.35 xalign target_x
    pause duration * 0.25
    easeout duration * 0.40 xalign home_x


transform lunge_approach(home_x, target_x, duration=0.2, y=1.0):
    xalign home_x
    yalign y
    easein duration xalign target_x


transform lunge_return(from_x, home_x, duration=0.25, y=1.0):
    xalign from_x
    yalign y
    easeout duration xalign home_x


transform hit_reaction(home_x, knock_dir=1, duration=0.35, y=1.0):
    xalign home_x
    yalign y
    parallel:
        ease 0.08 xalign (home_x + 0.045 * knock_dir)
        ease 0.27 xalign home_x
    parallel:
        matrixcolor TintMatrix("#ff3333") * BrightnessMatrix(0.2)
        linear duration matrixcolor IdentityMatrix()
    parallel:
        ease 0.05 yoffset 14
        ease 0.05 yoffset -14
        ease 0.05 yoffset 10
        ease 0.05 yoffset -10
        ease 0.05 yoffset 6
        ease 0.05 yoffset 0


transform heal_glow:
    matrixcolor TintMatrix("#88ffaa") * BrightnessMatrix(0.2)
    linear 0.45 matrixcolor IdentityMatrix()


transform energy_flash:
    matrixcolor TintMatrix("#aaddff") * BrightnessMatrix(0.25)
    linear 0.35 matrixcolor IdentityMatrix()


transform hop:
    yalign 1.0
    ease 0.12 yoffset -40
    ease 0.18 yoffset 0


transform status_tint(colour="#ffffff"):
    matrixcolor TintMatrix(colour)


# ---------------------------------------------------------------------------
# Special attack transforms (names do NOT collide with screen names)
# ---------------------------------------------------------------------------

transform tf_special_dim:
    alpha 0.0
    linear 0.12 alpha 0.7


transform tf_special_banner:
    xalign -0.6
    yalign 0.32
    alpha 1.0
    easein 0.22 xalign 0.5
    pause 0.6
    easeout 0.22 xalign 1.6


transform tf_special_cutin_player:
    xalign -0.3
    yalign 1.0
    zoom 1.7
    alpha 0.0
    easein 0.2 xalign 0.12 alpha 1.0


transform tf_special_cutin_enemy:
    xalign 1.3
    yalign 1.0
    zoom 1.7
    alpha 0.0
    easein 0.2 xalign 0.88 alpha 1.0


transform tf_special_impact:
    alpha 0.0
    linear 0.04 alpha 0.9
    linear 0.18 alpha 0.0
