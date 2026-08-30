# Vespera / Elena Voss — declared CGs, battle stills, Hale, story bgs.
# Files live under game/images/vespera/

# Combat stills (Dreamkrate story pack)
image vespera combat idle = Transform("vespera/battle_idle.jpg", ysize=920)
image vespera combat attack = Transform("vespera/battle_attack.jpg", ysize=920)
image vespera combat hit = Transform("vespera/battle_hit.jpg", ysize=920)

# Capture sheet crops (struggle / kneel / stand)
image vespera capture struggle = Transform("vespera/capture_struggle.jpg", ysize=920)
image vespera capture kneel = Transform("vespera/capture_kneel.jpg", ysize=920)
image vespera capture stand = Transform("vespera/capture_stand.jpg", ysize=920)

# Standing CG (layers/01-master-full.png)
image vespera stand = Transform("vespera/standing.jpg", ysize=980)

# Post-fight damaged suit (clothed, mask on)
image vespera damaged = Transform("vespera/damaged.jpg", ysize=980)

# Character sheet
image vespera sheet = Transform("vespera/charactersheet.jpg", xysize=(1920, 1071))

# Post-suit plate (adult, 26) — capture beat only
image vespera body = Transform("vespera/body_base.jpg", ysize=980)

# Map pin
image vespera token = "vespera/token.png"

# Dr. Hale
image hale stand = Transform("vespera/hale_stand.jpg", ysize=920)
image hale battle = Transform("vespera/hale_battle.jpg", ysize=720)

# Hale battle tags — engine also probes images/enemies/hale hover.png for size
image hale attack = Image("enemies/hale.png")
image hale heal = Image("enemies/hale.png")
image hale kick = Image("enemies/hale.png")
image hale punch = Image("enemies/hale.png")
image hale slash = Image("enemies/hale.png")
image hale raise_hand = Image("enemies/hale.png")
image hale drink = Image("enemies/hale.png")
image hale cast = Image("enemies/hale.png")
image hale hurt = Image("enemies/hale.png")
image hale hover = Image("enemies/hale hover.png")
image hale idle = Image("enemies/hale.png")
image hale idle_low = Image("enemies/hale.png")
image hale idle_stunned = Image("enemies/hale.png")
image hale idle_stunned_low = Image("enemies/hale.png")
image hale idle_poisoned = Image("enemies/hale.png")
image hale idle_poisoned_low = Image("enemies/hale.png")
image hale idle_burned = Image("enemies/hale.png")
image hale idle_burned_low = Image("enemies/hale.png")
image hale idle_frozen = Image("enemies/hale.png")
image hale idle_frozen_low = Image("enemies/hale.png")
image hale idle_weak = Image("enemies/hale.png")
image hale idle_weak_low = Image("enemies/hale.png")
image hale idle_vulnerable = Image("enemies/hale.png")
image hale idle_vulnerable_low = Image("enemies/hale.png")
image hale idle_shielded = Image("enemies/hale.png")
image hale idle_shielded_low = Image("enemies/hale.png")

# Story backgrounds
image bg rooftop night = Transform("vespera/bg_rooftop_night.jpg", xysize=(1920, 1080))
image bg lab = Transform("vespera/bg_lab.jpg", xysize=(1920, 1080))

# Player battle tags for this branch — Vespera stills instead of DarkDame.
# Idle / status share idle; attack actions share attack; hurt uses hit.
image player attack = Transform("vespera/battle_attack.jpg", ysize=700)
image player heal = Transform("vespera/battle_idle.jpg", ysize=700)
image player kick = Transform("vespera/battle_attack.jpg", ysize=700)
image player punch = Transform("vespera/battle_attack.jpg", ysize=700)
image player slash = Transform("vespera/battle_attack.jpg", ysize=700)
image player raise_hand = Transform("vespera/battle_idle.jpg", ysize=700)
image player drink = Transform("vespera/battle_idle.jpg", ysize=700)
image player cast = Transform("vespera/battle_attack.jpg", ysize=700)
image player hurt = Transform("vespera/battle_hit.jpg", ysize=700)
image player hover = Transform("vespera/battle_idle.jpg", ysize=700)
image player idle = Transform("vespera/battle_idle.jpg", ysize=700)
image player idle_low = Transform("vespera/battle_hit.jpg", ysize=700)
image player idle_stunned = Transform("vespera/battle_hit.jpg", ysize=700)
image player idle_stunned_low = Transform("vespera/battle_hit.jpg", ysize=700)
image player idle_poisoned = Transform("vespera/battle_idle.jpg", ysize=700)
image player idle_poisoned_low = Transform("vespera/battle_hit.jpg", ysize=700)
image player idle_burned = Transform("vespera/battle_idle.jpg", ysize=700)
image player idle_burned_low = Transform("vespera/battle_hit.jpg", ysize=700)
image player idle_frozen = Transform("vespera/battle_idle.jpg", ysize=700)
image player idle_frozen_low = Transform("vespera/battle_hit.jpg", ysize=700)
image player idle_weak = Transform("vespera/battle_hit.jpg", ysize=700)
image player idle_weak_low = Transform("vespera/battle_hit.jpg", ysize=700)
image player idle_vulnerable = Transform("vespera/battle_hit.jpg", ysize=700)
image player idle_vulnerable_low = Transform("vespera/battle_hit.jpg", ysize=700)
image player idle_shielded = Transform("vespera/battle_idle.jpg", ysize=700)
image player idle_shielded_low = Transform("vespera/battle_idle.jpg", ysize=700)
