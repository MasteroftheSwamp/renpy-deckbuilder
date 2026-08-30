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

# Hale battle tags (engine shows "<image> <anim>")
image hale attack = Transform("vespera/hale_battle.jpg", ysize=720)
image hale heal = Transform("vespera/hale_stand.jpg", ysize=720)
image hale kick = Transform("vespera/hale_battle.jpg", ysize=720)
image hale punch = Transform("vespera/hale_battle.jpg", ysize=720)
image hale slash = Transform("vespera/hale_battle.jpg", ysize=720)
image hale raise_hand = Transform("vespera/hale_stand.jpg", ysize=720)
image hale drink = Transform("vespera/hale_stand.jpg", ysize=720)
image hale cast = Transform("vespera/hale_battle.jpg", ysize=720)
image hale hurt = Transform("vespera/hale_stand.jpg", ysize=720)
image hale hover = Transform("vespera/hale_battle.jpg", ysize=720)
image hale idle = Transform("vespera/hale_battle.jpg", ysize=720)
image hale idle_low = Transform("vespera/hale_battle.jpg", ysize=720)
image hale idle_stunned = Transform("vespera/hale_stand.jpg", ysize=720)
image hale idle_stunned_low = Transform("vespera/hale_stand.jpg", ysize=720)
image hale idle_poisoned = Transform("vespera/hale_battle.jpg", ysize=720)
image hale idle_poisoned_low = Transform("vespera/hale_battle.jpg", ysize=720)
image hale idle_burned = Transform("vespera/hale_battle.jpg", ysize=720)
image hale idle_burned_low = Transform("vespera/hale_battle.jpg", ysize=720)
image hale idle_frozen = Transform("vespera/hale_battle.jpg", ysize=720)
image hale idle_frozen_low = Transform("vespera/hale_battle.jpg", ysize=720)
image hale idle_weak = Transform("vespera/hale_stand.jpg", ysize=720)
image hale idle_weak_low = Transform("vespera/hale_stand.jpg", ysize=720)
image hale idle_vulnerable = Transform("vespera/hale_stand.jpg", ysize=720)
image hale idle_vulnerable_low = Transform("vespera/hale_stand.jpg", ysize=720)
image hale idle_shielded = Transform("vespera/hale_battle.jpg", ysize=720)
image hale idle_shielded_low = Transform("vespera/hale_battle.jpg", ysize=720)

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
