init python:
    from uuid import uuid4


    class RPGCharacter():
        DEFAULT_ANIM = {
            "attack": "attack",
            "heal": "raise_hand",
            "energy": "drink",
            "draw": "cast",
        }
        DEFAULT_SFX = {
            "attack": "sound/punch.ogg",
            "heal": "sound/potion.ogg",
            "energy": "sound/powerup.ogg",
        }

        # All image states that may be shown (used when hiding)
        ALL_STATES = (
            "idle", "idle_low",
            "idle_stunned", "idle_stunned_low",
            "idle_poisoned", "idle_poisoned_low",
            "idle_burned", "idle_burned_low",
            "idle_frozen", "idle_frozen_low",
            "idle_weak", "idle_weak_low",
            "idle_vulnerable", "idle_vulnerable_low",
            "idle_shielded", "idle_shielded_low",
            "hurt",
            "attack", "heal", "kick", "punch", "slash",
            "raise_hand", "drink", "cast", "hover",
        )


        def __init__(self, **kwargs) -> None:
            self.id = str(uuid4())
            self.name = kwargs.get("name", "")

            image = kwargs.get("image", self.name.lower())
            if image:
                self.image_name = image
                if image == "player":
                    hover_path = "images/player/BattleSprites/DarkDameBattle-Hover.png"
                else:
                    hover_path = f"images/enemies/{image} hover.png"
                width, height = renpy.image_size(hover_path)
                self.width = width
                self.height = height

            self.health = self.health_max = kwargs.get("health", 0)
            self.energy = self.energy_max = kwargs.get("energy", 0)

            self.attack = 0
            self.attack_min = kwargs.get("attack_min", 0)
            self.attack_max = kwargs.get("attack_max", 0)
            self.attack_multiplier = kwargs.get("attack_multiplier", 1)

            self.heal = 0
            self.heal_min = kwargs.get("heal_min", 0)
            self.heal_max = kwargs.get("heal_max", 0)

            self.actions = kwargs.get("actions", [])

            # Flexible status map: key -> {"duration": int, "stacks": int}
            self.statuses = {}

            self.home_xalign = 0.5
            self.home_yalign = 1.0


        # ------------------------------------------------------------------
        # Compatibility: old .stunned flag maps onto the status system
        # ------------------------------------------------------------------
        @property
        def stunned(self) -> bool:
            return self.has_status("stunned")

        @stunned.setter
        def stunned(self, value: bool) -> None:
            if value:
                self.add_status("stunned")
            else:
                self.remove_status("stunned")


        # ------------------------------------------------------------------
        # Status API
        # ------------------------------------------------------------------
        def add_status(self, key: str, duration=None, stacks=None) -> None:
            """
            Apply or refresh a status.
            """
            if key not in STATUS_DEFS:
                return
            defn = STATUS_DEFS[key]
            d = duration if duration is not None else defn.default_duration
            s = stacks if stacks is not None else defn.default_stacks

            if key in self.statuses:
                # Refresh duration to the higher value; add stacks
                self.statuses[key]["duration"] = max(self.statuses[key]["duration"], d)
                self.statuses[key]["stacks"] += s
            else:
                self.statuses[key] = {"duration": d, "stacks": s}

            self.refresh_sprite()


        def remove_status(self, key: str) -> None:
            if key in self.statuses:
                del self.statuses[key]
                self.refresh_sprite()


        def clear_statuses(self) -> None:
            self.statuses.clear()
            self.refresh_sprite()


        def has_status(self, key: str) -> bool:
            return key in self.statuses and self.statuses[key]["duration"] > 0


        def status_stacks(self, key: str) -> int:
            return self.statuses.get(key, {}).get("stacks", 0)


        def is_action_blocked(self) -> bool:
            for key in self.statuses:
                if STATUS_DEFS[key].blocks_action:
                    return True
            return False


        def tick_statuses(self, when="end_turn") -> list:
            """
            Process status effects that tick at the given moment.
            Returns a list of narration strings (e.g. poison damage messages).
            """
            messages = []
            expired = []

            for key, data in list(self.statuses.items()):
                defn = STATUS_DEFS.get(key)
                if not defn:
                    continue

                if defn.tick_when == when:
                    # Damage-over-time statuses (poison, burn)
                    if key in ("poisoned", "burned") and data["stacks"] > 0:
                        dmg = data["stacks"]
                        self.health = max(0, self.health - dmg)
                        messages.append(f"{self.name} took {dmg} {defn.name.lower()} damage.")
                        renpy.sound.queue("sound/punch.ogg", relative_volume=0.3)

                    # Decrement duration
                    data["duration"] -= 1
                    if data["duration"] <= 0:
                        expired.append(key)

            for key in expired:
                del self.statuses[key]
                messages.append(f"{self.name} is no longer {STATUS_DEFS[key].name.lower()}.")

            if expired or messages:
                self.refresh_sprite()

            return messages


        def primary_status_suffix(self):
            """
            Return the idle_suffix of the highest-priority active status, or None.
            """
            for key in STATUS_IDLE_PRIORITY:
                if self.has_status(key):
                    return STATUS_DEFS[key].idle_suffix
            return None


        def active_tint(self):
            """
            Tint of the highest-priority active status, or None.
            """
            for key in STATUS_IDLE_PRIORITY:
                if self.has_status(key):
                    return STATUS_DEFS[key].tint
            return None


        def status_icons_text(self) -> str:
            """
            Concatenated icon string for UI display above the sprite.
            """
            icons = []
            for key in STATUS_IDLE_PRIORITY:
                if self.has_status(key):
                    icons.append(STATUS_DEFS[key].icon)
            return " ".join(icons)


        # ------------------------------------------------------------------
        # Idle / image resolution
        # ------------------------------------------------------------------
        def is_low_hp(self) -> bool:
            if self.health_max <= 0:
                return False
            return (self.health / self.health_max) <= LOW_HP_RATIO


        def get_idle_state(self) -> str:
            """
            Compute the correct idle image state:
              idle | idle_low | idle_<status> | idle_<status>_low
            """
            suffix = self.primary_status_suffix()
            low = self.is_low_hp()

            if suffix and low:
                return f"idle_{suffix}_low"
            if suffix:
                return f"idle_{suffix}"
            if low:
                return "idle_low"
            return "idle"


        def image(self, state="") -> str:
            """
            Get image name.  Empty state → resolved idle (status + low-HP aware).
            Explicit states (attack, hurt, kick, …) are used as-is so telegraph
            and action poses stay clean.
            """
            if not state:
                # Telegraph pose while the player still has turns left
                if player.turns and self.action("attack", 0) > 0:
                    state = "attack"
                elif player.turns and self.action("heal", 0) > 0:
                    state = "heal"
                else:
                    state = self.get_idle_state()
            return f"{self.image_name} {state}"


        def refresh_sprite(self) -> None:
            """
            Re-show the character at home with the correct idle + optional tint.
            Safe to call even if the character is not currently on screen.
            """
            if not hasattr(self, "image_name"):
                return
            home_x = getattr(self, "home_xalign", 0.5)
            home_y = getattr(self, "home_yalign", 1.0)
            state = self.get_idle_state()
            tag = self.image(state)
            at_list = [position(home_x, home_y)]

            tint = self.active_tint()
            if tint:
                at_list.append(status_tint(tint))

            try:
                renpy.show(tag, at_list=at_list, layer=LAYER_ENEMIES)
            except Exception:
                pass


        def hide_all_states(self) -> None:
            for state in self.ALL_STATES:
                renpy.hide(f"{self.image_name} {state}", layer=LAYER_ENEMIES)


        # ------------------------------------------------------------------
        # Combat helpers
        # ------------------------------------------------------------------
        def action(self, key: str, value=None):
            return next(iter(self.actions), {}).get(key, value)


        def say(self) -> str:
            if self.is_action_blocked():
                blocked = [STATUS_DEFS[k].name for k in self.statuses if STATUS_DEFS[k].blocks_action]
                return f"{self.name} is {'/'.join(blocked)}!"
            return self.action("say", "").format(name=self.name)


        def hurt(self, value: int) -> None:
            if not value:
                return
            # Vulnerable amplifies incoming damage
            if self.has_status("vulnerable"):
                value = int(value * 1.5)
            # Shielded reduces it
            if self.has_status("shielded"):
                value = max(0, value - self.status_stacks("shielded"))
            self.health = max(0, self.health - value)


        def recover(self, value: int, overheal=False) -> None:
            if not value:
                return
            if not overheal and self.health + value >= self.health_max:
                self.health = self.health_max
            else:
                self.health += value
            self.refresh_sprite()


        def stun(self, stunned: bool) -> None:
            self.stunned = stunned


        # ------------------------------------------------------------------
        # Animations
        # ------------------------------------------------------------------
        def play_action(self, anim="attack", target_xalign=None, sfx=None, effect=None, duration=0.55):
            """
            Play a non-attack (or simple) battle animation, then return to proper idle.
            """
            home_x = getattr(self, "home_xalign", 0.5)
            home_y = getattr(self, "home_yalign", 1.0)
            tag = self.image(anim)
            at_list = []

            if target_xalign is not None:
                mid = home_x + (target_xalign - home_x) * 0.6
                at_list.append(lunge(home_x, mid, duration=duration, y=home_y))
            else:
                at_list.append(position(home_x, home_y))

            if effect == "glow":
                at_list.append(heal_glow)
            elif effect == "energy":
                at_list.append(energy_flash)
            elif effect == "hop":
                at_list.append(hop)

            renpy.show(tag, at_list=at_list, layer=LAYER_ENEMIES)
            if sfx:
                renpy.sound.queue(sfx, relative_volume=0.6)
            renpy.pause(duration)
            self.refresh_sprite()


        def play_attack(self, anim="attack", target=None, sfx="sound/punch.ogg", duration=0.55):
            """
            Full attack sequence with contact-timed hit reaction on the target.
            1. Lunge toward target
            2. On contact → target plays hit reaction
            3. Return home → refresh idle
            """
            home_x = getattr(self, "home_xalign", 0.5)
            home_y = getattr(self, "home_yalign", 1.0)
            target_x = getattr(target, "home_xalign", 0.8) if target else 0.8
            mid = home_x + (target_x - home_x) * 0.6
            contact = duration * 0.38
            ret = duration * 0.42

            # Approach
            renpy.show(
                self.image(anim),
                at_list=[lunge_approach(home_x, mid, contact, y=home_y)],
                layer=LAYER_ENEMIES,
            )
            if sfx:
                renpy.sound.queue(sfx, relative_volume=0.6)
            renpy.pause(contact)

            # Contact — hit reaction on target
            if target is not None:
                knock_dir = 1 if home_x < target_x else -1
                target.play_hit_reaction(knock_dir=knock_dir)

            # Return
            renpy.show(
                self.image(anim),
                at_list=[lunge_return(mid, home_x, ret, y=home_y)],
                layer=LAYER_ENEMIES,
            )
            renpy.pause(ret)
            self.refresh_sprite()


        def play_hit_reaction(self, knock_dir=1, duration=0.35):
            """
            Hurt pose + knockback + red flash + shake, then back to proper idle.
            """
            home_x = getattr(self, "home_xalign", 0.5)
            home_y = getattr(self, "home_yalign", 1.0)
            renpy.show(
                self.image("hurt"),
                at_list=[hit_reaction(home_x, knock_dir=knock_dir, duration=duration, y=home_y)],
                layer=LAYER_ENEMIES,
            )
            renpy.sound.queue("sound/punch.ogg", relative_volume=0.4)
            renpy.pause(duration)
            self.refresh_sprite()


        def play_special_attack(self, title="SPECIAL ATTACK", anim="attack", sfx="sound/powerup.ogg", colour="#ffcc00"):
            """
            JRPG-style special attack sequence using LAYER_FX (not screens),
            so it works reliably inside invoke_in_new_context:

              1. Dim battlefield
              2. Banner slides across with the attack name
              3. Full-screen character cut-in
              4. Impact flash

            Caller applies damage / hit reactions afterwards.
            """
            is_player = (self.image_name == "player")

            # 1. Dim
            renpy.show(
                "fx_dim",
                what=Solid("#000000"),
                at_list=[tf_special_dim],
                layer=LAYER_FX,
            )
            renpy.pause(0.15)

            # 2. Banner
            if sfx:
                renpy.sound.queue(sfx, relative_volume=0.8)

            banner = Fixed(
                Solid((0, 0, 0, 210), xysize=(920, 110)),
                Text(
                    title,
                    size=58,
                    color=colour,
                    bold=True,
                    textalign=0.5,
                    xalign=0.5,
                    yalign=0.5,
                    outlines=[(3, "#000000", 0, 0)],
                ),
                xysize=(920, 110),
            )
            renpy.show(
                "fx_banner",
                what=banner,
                at_list=[tf_special_banner],
                layer=LAYER_FX,
            )
            renpy.pause(1.05)
            renpy.hide("fx_banner", layer=LAYER_FX)

            # 3. Cut-in
            cutin_tf = tf_special_cutin_player if is_player else tf_special_cutin_enemy
            renpy.show(
                "fx_cutin",
                what=renpy.displayable(self.image(anim)),
                at_list=[cutin_tf],
                layer=LAYER_FX,
            )
            renpy.pause(0.95)
            renpy.hide("fx_cutin", layer=LAYER_FX)

            # 4. Impact flash
            renpy.show(
                "fx_impact",
                what=Solid("#ffffff"),
                at_list=[tf_special_impact],
                layer=LAYER_FX,
            )
            renpy.sound.queue("sound/punch.ogg", relative_volume=0.7)
            renpy.pause(0.25)
            renpy.hide("fx_impact", layer=LAYER_FX)

            renpy.hide("fx_dim", layer=LAYER_FX)
            renpy.pause(0.05)
