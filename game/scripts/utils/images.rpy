# ---------------------------------------------------------------------------
# Helper: every character gets the same set of state names.
# All non-hover states currently share the base art as placeholders.
# Drop real frames (or Animation() / ATL) into the matching paths when ready.
# ---------------------------------------------------------------------------

# ---- Boy ----
image boy attack = Image("enemies/boy.png")
image boy heal = Image("enemies/boy.png")
image boy kick = Image("enemies/boy.png")
image boy punch = Image("enemies/boy.png")
image boy slash = Image("enemies/boy.png")
image boy raise_hand = Image("enemies/boy.png")
image boy drink = Image("enemies/boy.png")
image boy cast = Image("enemies/boy.png")
image boy hurt = Image("enemies/boy.png")
image boy hover = Image("enemies/boy hover.png")
image boy idle = Image("enemies/boy.png")
image boy idle_low = Image("enemies/boy.png")
image boy idle_stunned = Image("enemies/boy.png")
image boy idle_stunned_low = Image("enemies/boy.png")
image boy idle_poisoned = Image("enemies/boy.png")
image boy idle_poisoned_low = Image("enemies/boy.png")
image boy idle_burned = Image("enemies/boy.png")
image boy idle_burned_low = Image("enemies/boy.png")
image boy idle_frozen = Image("enemies/boy.png")
image boy idle_frozen_low = Image("enemies/boy.png")
image boy idle_weak = Image("enemies/boy.png")
image boy idle_weak_low = Image("enemies/boy.png")
image boy idle_vulnerable = Image("enemies/boy.png")
image boy idle_vulnerable_low = Image("enemies/boy.png")
image boy idle_shielded = Image("enemies/boy.png")
image boy idle_shielded_low = Image("enemies/boy.png")


# ---- Girl ----
image girl attack = Image("enemies/girl.png")
image girl heal = Image("enemies/girl.png")
image girl kick = Image("enemies/girl.png")
image girl punch = Image("enemies/girl.png")
image girl slash = Image("enemies/girl.png")
image girl raise_hand = Image("enemies/girl.png")
image girl drink = Image("enemies/girl.png")
image girl cast = Image("enemies/girl.png")
image girl hurt = Image("enemies/girl.png")
image girl hover = Image("enemies/girl hover.png")
image girl idle = Image("enemies/girl.png")
image girl idle_low = Image("enemies/girl.png")
image girl idle_stunned = Image("enemies/girl.png")
image girl idle_stunned_low = Image("enemies/girl.png")
image girl idle_poisoned = Image("enemies/girl.png")
image girl idle_poisoned_low = Image("enemies/girl.png")
image girl idle_burned = Image("enemies/girl.png")
image girl idle_burned_low = Image("enemies/girl.png")
image girl idle_frozen = Image("enemies/girl.png")
image girl idle_frozen_low = Image("enemies/girl.png")
image girl idle_weak = Image("enemies/girl.png")
image girl idle_weak_low = Image("enemies/girl.png")
image girl idle_vulnerable = Image("enemies/girl.png")
image girl idle_vulnerable_low = Image("enemies/girl.png")
image girl idle_shielded = Image("enemies/girl.png")
image girl idle_shielded_low = Image("enemies/girl.png")


# ---- Player (DarkDame battle sprites) ----
# Art: game/images/player/BattleSprites/
# Tags stay "player <state>" so battle logic is unchanged.

image player attack = Image("player/BattleSprites/DarkDameBattle-Attack.png")
image player heal = Image("player/BattleSprites/DarkDameBattle-Heal.png")
image player kick = Image("player/BattleSprites/DarkDameBattle-Kick.png")
image player punch = Image("player/BattleSprites/DarkDameBattle-Punch.png")
image player slash = Image("player/BattleSprites/DarkDameBattle-Slash.png")
image player raise_hand = Image("player/BattleSprites/DarkDameBattle-Heal-Raise_Hand.png")
image player drink = Image("player/BattleSprites/DarkDameBattle-Drink.png")
image player cast = Image("player/BattleSprites/DarkDameBattle-Cast.png")
image player hurt = Image("player/BattleSprites/DarkDameBattle-Hurt.png")
image player hover = Image("player/BattleSprites/DarkDameBattle-Hover.png")
image player idle = Image("player/BattleSprites/DarkDameBattle-Idle.png")
image player idle_low = Image("player/BattleSprites/DarkDameBattle-Idle_Low.png")
image player idle_stunned = Image("player/BattleSprites/DarkDameBattle-Idle_Stunned.png")
image player idle_stunned_low = Image("player/BattleSprites/DarkDameBattle-Idle_Stunned_Low.png")
image player idle_poisoned = Image("player/BattleSprites/DarkDameBattle-Idle_Poisoned.png")
image player idle_poisoned_low = Image("player/BattleSprites/DarkDameBattle-Idle_Poisoned_Low.png")
# No burned art yet — fall back to poisoned
image player idle_burned = Image("player/BattleSprites/DarkDameBattle-Idle_Poisoned.png")
image player idle_burned_low = Image("player/BattleSprites/DarkDameBattle-Idle_Poisoned_Low.png")
image player idle_frozen = Image("player/BattleSprites/DarkDameBattle-Idle_Frozen.png")
image player idle_frozen_low = Image("player/BattleSprites/DarkDameBattle-Idle_Frozen_Low.png")
image player idle_weak = Image("player/BattleSprites/DarkDameBattle-Idle_Weak.png")
image player idle_weak_low = Image("player/BattleSprites/DarkDameBattle-Idle_Weak_Low.png")
image player idle_vulnerable = Image("player/BattleSprites/DarkDameBattle-Idle_Vulnerable.png")
image player idle_vulnerable_low = Image("player/BattleSprites/DarkDameBattle-Idle_Vulnerable_Low.png")
image player idle_shielded = Image("player/BattleSprites/DarkDameBattle-Idle_Shielded.png")
image player idle_shielded_low = Image("player/BattleSprites/DarkDameBattle-Idle_Shielded_low.png")


# ---------------------------------------------------------------------------
# Battle / story backgrounds (no spaces in paths; fill 1920x1080)
# ---------------------------------------------------------------------------
image bg plain = Transform(Image("bg/plain.jpg"), xysize=(1920, 1080))
image bg defeat = Transform(Image("bg/defeat.jpg"), xysize=(1920, 1080))
image bg jail = Transform(Image("bg/jail.jpg"), xysize=(1920, 1080))

# Busts used as side images next to the dialogue box (must be declared at init)
image side opponent = Image("enemies/opponent bust.png")
image side opponent_boy = Image("enemies/boy.png")
image side opponent_girl = Image("enemies/girl.png")
