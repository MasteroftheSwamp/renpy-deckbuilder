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


# Full lunge (approach + pause + return) — used for simple non-coordinated moves
transform lunge(home_x, target_x, duration=0.55, y=1.0):
    xalign home_x
    yalign y
    easein duration * 0.35 xalign target_x
    pause duration * 0.25
    easeout duration * 0.40 xalign home_x


# Split lunge so contact timing can trigger a hit reaction mid-sequence
transform lunge_approach(home_x, target_x, duration=0.2, y=1.0):
    xalign home_x
    yalign y
    easein duration xalign target_x


transform lunge_return(from_x, home_x, duration=0.25, y=1.0):
    xalign from_x
    yalign y
    easeout duration xalign home_x


# Hit reaction: knockback + red flash + vertical shake
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


# Soft green glow for heal
transform heal_glow:
    matrixcolor TintMatrix("#88ffaa") * BrightnessMatrix(0.2)
    linear 0.45 matrixcolor IdentityMatrix()


# Blue flash for energy / power-up
transform energy_flash:
    matrixcolor TintMatrix("#aaddff") * BrightnessMatrix(0.25)
    linear 0.35 matrixcolor IdentityMatrix()


# Small hop for drink / self-buff
transform hop:
    yalign 1.0
    ease 0.12 yoffset -40
    ease 0.18 yoffset 0


# Persistent status tint (applied while a status is active on idle)
transform status_tint(colour="#ffffff"):
    matrixcolor TintMatrix(colour)
