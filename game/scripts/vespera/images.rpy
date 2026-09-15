# Vespera / Elena Voss — declared CGs, battle stills, Hale, story bgs.
# Files live under game/images/vespera/

# Legacy scale knob (bust PNGs are now native 420×420 squares).
define SIDE_BUST_YSIZE = 420

# Combat stills (Dreamkrate battle kit)
image vespera combat idle = Transform("vespera/battle/idle.png", ysize=920)
image vespera combat attack = Transform("vespera/battle/attack.png", ysize=920)
image vespera combat hit = Transform("vespera/battle/hurt.png", ysize=920)

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

# Hale battle tags — Dreamkrate kit under enemies/hale/ (700px tall).
# Engine still probes images/enemies/hale hover.png for layout size.
image hale attack = Image("enemies/hale/attack.png")
image hale heal = Image("enemies/hale/heal.png")
image hale kick = Image("enemies/hale/kick.png")
image hale punch = Image("enemies/hale/punch.png")
image hale slash = Image("enemies/hale/slash.png")
image hale raise_hand = Image("enemies/hale/raise_hand.png")
image hale drink = Image("enemies/hale/drink.png")
image hale cast = Image("enemies/hale/cast.png")
image hale hurt = Image("enemies/hale/hurt.png")
image hale hover = Image("enemies/hale/hover.png")
image hale idle = Image("enemies/hale/idle.png")
image hale idle_low = Image("enemies/hale/idle_low.png")
image hale idle_stunned = Image("enemies/hale/idle_stunned.png")
image hale idle_stunned_low = Image("enemies/hale/idle_stunned_low.png")
image hale idle_poisoned = Image("enemies/hale/idle_poisoned.png")
image hale idle_poisoned_low = Image("enemies/hale/idle_poisoned_low.png")
image hale idle_burned = Image("enemies/hale/idle_burned.png")
image hale idle_burned_low = Image("enemies/hale/idle_burned_low.png")
image hale idle_frozen = Image("enemies/hale/idle_frozen.png")
image hale idle_frozen_low = Image("enemies/hale/idle_frozen_low.png")
image hale idle_weak = Image("enemies/hale/idle_weak.png")
image hale idle_weak_low = Image("enemies/hale/idle_weak_low.png")
image hale idle_vulnerable = Image("enemies/hale/idle_vulnerable.png")
image hale idle_vulnerable_low = Image("enemies/hale/idle_vulnerable_low.png")
image hale idle_shielded = Image("enemies/hale/idle_shielded.png")
image hale idle_shielded_low = Image("enemies/hale/idle_shielded_low.png")

# Hale dialogue — abridged emotions (supporting cast). Busts = side images; full = centrals.
# Side busts scaled ysize=SIDE_BUST_YSIZE so they sit as faces beside the say box (tweak here, keep full-res PNGs).
# Usage later: dr_hale smug "…"  |  show hale smug
# Emotions: neutral, smug, clinical, angry, surprised, pleased, frustrated
image side hale = Image("hale/bust/neutral.png")
image side hale neutral = Image("hale/bust/neutral.png")
image side hale smug = Image("hale/bust/smug.png")
image side hale clinical = Image("hale/bust/clinical.png")
image side hale angry = Image("hale/bust/angry.png")
image side hale surprised = Image("hale/bust/surprised.png")
image side hale pleased = Image("hale/bust/pleased.png")
image side hale frustrated = Image("hale/bust/frustrated.png")

image hale neutral = Transform("hale/full/neutral.png", ysize=980)
image hale smug = Transform("hale/full/smug.png", ysize=980)
image hale clinical = Transform("hale/full/clinical.png", ysize=980)
image hale angry = Transform("hale/full/angry.png", ysize=980)
image hale surprised = Transform("hale/full/surprised.png", ysize=980)
image hale pleased = Transform("hale/full/pleased.png", ysize=980)
image hale frustrated = Transform("hale/full/frustrated.png", ysize=980)


# Amora dialogue — abridged emotions (supporting cast). Busts = side; full = centrals.
# Usage: amora smirk "…"  |  show amora smirk
# Emotions: neutral, smirk, sadistic, angry, amused, cold, surprised
image side amora = Image("amora/bust/neutral.png")
image side amora neutral = Image("amora/bust/neutral.png")
image side amora smirk = Image("amora/bust/smirk.png")
image side amora sadistic = Image("amora/bust/sadistic.png")
image side amora angry = Image("amora/bust/angry.png")
image side amora amused = Image("amora/bust/amused.png")
image side amora cold = Image("amora/bust/cold.png")
image side amora surprised = Image("amora/bust/surprised.png")

image amora neutral = Transform("amora/full/neutral.png", ysize=980)
image amora smirk = Transform("amora/full/smirk.png", ysize=980)
image amora sadistic = Transform("amora/full/sadistic.png", ysize=980)
image amora angry = Transform("amora/full/angry.png", ysize=980)
image amora amused = Transform("amora/full/amused.png", ysize=980)
image amora cold = Transform("amora/full/cold.png", ysize=980)
image amora surprised = Transform("amora/full/surprised.png", ysize=980)

# Amora battle tags — OpenArt kit under enemies/amora/ (700px tall).
# Engine probes images/enemies/amora hover.png for layout size.
image amora attack = Image("enemies/amora/attack.png")
image amora heal = Image("enemies/amora/heal.png")
image amora kick = Image("enemies/amora/kick.png")
image amora punch = Image("enemies/amora/punch.png")
image amora slash = Image("enemies/amora/slash.png")
image amora raise_hand = Image("enemies/amora/raise_hand.png")
image amora drink = Image("enemies/amora/drink.png")
image amora cast = Image("enemies/amora/cast.png")
image amora hurt = Image("enemies/amora/hurt.png")
image amora hover = Image("enemies/amora/hover.png")
image amora idle = Image("enemies/amora/idle.png")
image amora idle_low = Image("enemies/amora/idle_low.png")
image amora idle_stunned = Image("enemies/amora/idle_stunned.png")
image amora idle_stunned_low = Image("enemies/amora/idle_stunned_low.png")
image amora idle_poisoned = Image("enemies/amora/idle_poisoned.png")
image amora idle_poisoned_low = Image("enemies/amora/idle_poisoned_low.png")
image amora idle_burned = Image("enemies/amora/idle_burned.png")
image amora idle_burned_low = Image("enemies/amora/idle_burned_low.png")
image amora idle_frozen = Image("enemies/amora/idle_frozen.png")
image amora idle_frozen_low = Image("enemies/amora/idle_frozen_low.png")
image amora idle_weak = Image("enemies/amora/idle_weak.png")
image amora idle_weak_low = Image("enemies/amora/idle_weak_low.png")
image amora idle_vulnerable = Image("enemies/amora/idle_vulnerable.png")
image amora idle_vulnerable_low = Image("enemies/amora/idle_vulnerable_low.png")
image amora idle_shielded = Image("enemies/amora/idle_shielded.png")
image amora idle_shielded_low = Image("enemies/amora/idle_shielded_low.png")



# Story backgrounds
image bg rooftop night = Transform("vespera/bg_rooftop_night.jpg", xysize=(1920, 1080))
image bg lab = Transform("vespera/bg_lab.jpg", xysize=(1920, 1080))

# Hale + Amora chamber story stills (16:9 CGs)
image bg hale amora chamber 01 = Transform("story/hale_amora_chamber/01_establish.png", xysize=(1920, 1080))
image bg hale amora chamber 02 = Transform("story/hale_amora_chamber/02_hale_slam.png", xysize=(1920, 1080))
image bg hale amora chamber 03 = Transform("story/hale_amora_chamber/03_amora_amused.png", xysize=(1920, 1080))
image bg hale amora chamber 04 = Transform("story/hale_amora_chamber/04_hale_jab.png", xysize=(1920, 1080))
image bg hale amora chamber 05 = Transform("story/hale_amora_chamber/05_amora_lean.png", xysize=(1920, 1080))
image bg hale amora chamber 06 = Transform("story/hale_amora_chamber/06_amora_approaches.png", xysize=(1920, 1080))
image bg hale amora chamber 07 = Transform("story/hale_amora_chamber/07_amora_shoulders.png", xysize=(1920, 1080))
image bg hale amora chamber 08 = Transform("story/hale_amora_chamber/08_hale_turns.png", xysize=(1920, 1080))
image bg hale amora chamber 09 = Transform("story/hale_amora_chamber/09_amora_smile.png", xysize=(1920, 1080))
image bg hale amora chamber 10 = Transform("story/hale_amora_chamber/10_amora_plan.png", xysize=(1920, 1080))
image bg hale amora chamber 11 = Transform("story/hale_amora_chamber/11_hale_vicious_smile.png", xysize=(1920, 1080))


# Player battle tags — Dreamkrate Vespera battle kit (13 unique stills).
# Missing status/action poses alias the closest available art until painted.
image player attack = Transform("vespera/battle/attack.png", ysize=700)
image player heal = Transform("vespera/battle/hover.png", ysize=700)
image player kick = Transform("vespera/battle/kick.png", ysize=700)
image player punch = Transform("vespera/battle/punch.png", ysize=700)
image player slash = Transform("vespera/battle/attack.png", ysize=700)
image player raise_hand = Transform("vespera/battle/hover.png", ysize=700)
image player drink = Transform("vespera/battle/idle.png", ysize=700)
image player cast = Transform("vespera/battle/attack.png", ysize=700)
image player hurt = Transform("vespera/battle/hurt.png", ysize=700)
image player hover = Transform("vespera/battle/hover.png", ysize=700)
image player idle = Transform("vespera/battle/idle.png", ysize=700)
image player idle_low = Transform("vespera/battle/idle_low.png", ysize=700)
image player idle_stunned = Transform("vespera/battle/hurt.png", ysize=700)
image player idle_stunned_low = Transform("vespera/battle/idle_low.png", ysize=700)
image player idle_poisoned = Transform("vespera/battle/idle.png", ysize=700)
image player idle_poisoned_low = Transform("vespera/battle/idle_low.png", ysize=700)
image player idle_burned = Transform("vespera/battle/idle_burned.png", ysize=700)
image player idle_burned_low = Transform("vespera/battle/idle_low.png", ysize=700)
image player idle_frozen = Transform("vespera/battle/idle.png", ysize=700)
image player idle_frozen_low = Transform("vespera/battle/idle_low.png", ysize=700)
image player idle_weak = Transform("vespera/battle/idle_weak_low.png", ysize=700)
image player idle_weak_low = Transform("vespera/battle/idle_weak_low.png", ysize=700)
image player idle_vulnerable = Transform("vespera/battle/idle_vulnerable.png", ysize=700)
image player idle_vulnerable_low = Transform("vespera/battle/idle_vulnerable_low.png", ysize=700)
image player idle_shielded = Transform("vespera/battle/idle_shielded.png", ysize=700)
image player idle_shielded_low = Transform("vespera/battle/idle_shielded_low.png", ysize=700)
