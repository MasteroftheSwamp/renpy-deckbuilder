# Vespera / Elena Voss — declared CGs and combat stills (no Live2D).
# Files live under game/images/vespera/

# Combat sheet crops (left idle / mid attack / right hit)
image vespera combat idle = Transform("vespera/combat_idle.jpg", ysize=920)
image vespera combat attack = Transform("vespera/combat_attack.jpg", ysize=920)
image vespera combat hit = Transform("vespera/combat_hit.jpg", ysize=920)

# Capture sheet crops (struggle / kneel / stand)
image vespera capture struggle = Transform("vespera/capture_struggle.jpg", ysize=920)
image vespera capture kneel = Transform("vespera/capture_kneel.jpg", ysize=920)
image vespera capture stand = Transform("vespera/capture_stand.jpg", ysize=920)

# Standing CG (layers/01-master-full.png)
image vespera stand = Transform("vespera/standing.jpg", ysize=980)

# Character sheet
image vespera sheet = Transform("vespera/charactersheet.jpg", xysize=(1920, 1071))

# Post-suit plate (adult, 26) — capture beat only
image vespera body = Transform("vespera/body_base.jpg", ysize=980)

# Map pin
image vespera token = "vespera/token.png"
