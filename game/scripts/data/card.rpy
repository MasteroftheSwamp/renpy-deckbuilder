init python:
    from uuid import uuid4


    class Card:
        LABEL_DESCRIPTION_YPOS = 100
        LABEL_NAME_YPOS = 5
        WIDTH = 250
        HEIGHT = 350
        OFFSET = 80


        def __init__(self, **kwargs) -> None:
            self.id = str(uuid4())
            self.cost = kwargs.get("cost", 0)
            self.action = kwargs.get("action", {})
            self.value = kwargs.get("value", 0)

            # Optional per-card battle animation (kick, slash, raise_hand, drink, ...)
            # Falls back to a sensible default derived from the primary action in use().
            self.anim = kwargs.get("anim", None)

            # Special attack config (JRPG-style).
            # False/None = normal attack.
            # True = use card name + defaults.
            # dict = { "title", "anim", "sfx", "colour" }
            self.special = kwargs.get("special", None)

            self.image = f"cards/{kwargs.get('image', 'transparent')}.png"
            self.name = kwargs.get("name", "")


        def label_size(self, label: str) -> str:
            """
            Get label size.
            """
            size = 1.0
            length = len(label)

            if length < 5:
                size = 0.95
            elif length < 15:
                size = 0.9
            elif length < 25:
                size = 0.85
            elif length < 35:
                size = 0.8
            else:
                size = 0.75

            if renpy.variant("mobile") or renpy.variant("touch"):
                size -= 0.15

            return f"{{size=*{size}}}" if not size == 1.0 else ""


        def label_name(self) -> str:
            """
            Name label.
            """
            return self.label_size(self.name) + "{color=[colors.label]}{b}{k=-2}" + self.name


        def label_cost(self) -> str:
            """
            Cost label.
            """
            return self.label_size(str(self.cost)) + emojis.get(self.cost)


        def label_description(self) -> str:
            """
            Description label.
            """
            label = ""
            color = "{color=[colors.label]}"

            if self.special:
                label += "★ Special\n"

            for action, data in self.action.items():
                if not isinstance(data, dict):
                    continue
                value = data.get("value")
                if value is None and action not in ("status", "cleanse"):
                    continue
                if value is None:
                    continue

                label += action.capitalize()
                label += f" {value}"

                if data.get("times", 1) > 1:
                    label += f" ×{data.get('times')}"

                if data.get("stun"):
                    label += " Stun"
                if data.get("poison"):
                    label += " Poison"
                if data.get("all"):
                    label += " All"

                if action == "turns":
                    label += " once per battle"

                label += "\n"

            label = label.rstrip('\n')

            return self.label_size(label) + color + label


        @staticmethod
        def label_upgrade(action: str, value=1) -> str:
            """
            Upgrade label.
            """
            if action == "all":
                return f"Select a card to apply effects to {{b}}{{color=[colors.note]}}all{{/color}}{{/b}} enemies:"
            elif action == "cost":
                return f"Select a card to decrease {{b}}{{color=[colors.note]}}cost{{/color}}{{/b}} by {emojis.get(1)}:"
            elif action == "stun":
                return f"Select a card to {{b}}{{color=[colors.note]}}stun{{/color}}{{/b}} an enemy:"
            elif action == "times":
                return f"Select a card to increase action by 1 {{b}}{{color=[colors.note]}}time{{/color}}{{/b}}:"
            else:
                return f"Select a card to increase {{b}}{{color=[colors.note]}}{action}{{/color}}{{/b}} by {{b}}{value}{{/b}}:"


        def upgrade(self, action: str, value=1) -> None:
            """
            Upgrade card.
            """
            if action in ["all", "stun"]:
                self.action["attack"][action] = True
            elif action == "cost" and self.cost > 0:
                self.cost -= 1
            elif action == "times":
                action = self.action.get("attack") if self.action.get("attack") else self.action.get("heal")
                action["times"] = action.get("times", 1)
                action["times"] += 1
            else:
                if self.action.get(action):
                    self.action[action]["value"] += value
                else:
                    self.action[action] = {"value": value}


        def get_xpos(self) -> int:
            """
            Calculate x-position.
            """
            x = config.screen_width / 2
            x -= (self.WIDTH + self.OFFSET * (len(deck.hand) - 1)) / 2
            x += deck.hand.index(self) * self.OFFSET
            return int(x)


        def get_ypos(self) -> int:
            """
            Calculate y-position.
            """
            return config.screen_height - self.HEIGHT


        def get_pos(self):
            """
            Calculate xy-position.
            """
            return self.get_xpos(), self.get_ypos()


        def use(self, target) -> None:
            """
            Use card.
            Plays battle animations (with contact-timed hit reactions on attacks),
            applies damage/heal/status effects, then discards.
            """
            if player.energy < self.cost:
                renpy.notify(f"Not enough energy! (need {self.cost})")
                return

            player.energy -= self.cost
            is_enemy = target != player

            # Resolve animation
            anim = self.anim
            if not anim:
                if self.action.get("attack"):
                    anim = "attack"
                elif self.action.get("heal"):
                    anim = "raise_hand"
                elif self.action.get("energy"):
                    anim = "drink"
                elif self.action.get("draw"):
                    anim = "cast"
                else:
                    anim = "idle"

            energy = self.action.get("energy")
            draw = self.action.get("draw")
            heal = self.action.get("heal")
            attack = self.action.get("attack")
            # Optional status application: {"status": "poisoned", "duration": 3, "stacks": 2}
            # or shorthand on attack: attack.stun / attack.poison etc.
            status_spec = self.action.get("status")

            # --- Player animation ---
            if attack and is_enemy and self.special:
                # JRPG special: banner → cut-in → impact, then hit reactions below
                spec = self.special if isinstance(self.special, dict) else {}
                title = spec.get("title", self.name.upper() or "SPECIAL ATTACK")
                cutin_anim = spec.get("anim", anim or "attack")
                sfx = spec.get("sfx", "sound/powerup.ogg")
                colour = spec.get("colour", "#ffcc00")
                player.play_special_attack(
                    title=title,
                    anim=cutin_anim,
                    sfx=sfx,
                    colour=colour,
                )
            elif attack and is_enemy:
                if attack.get("all"):
                    living = enemies.alive()
                    first = living[0] if living else target
                    player.play_attack(anim=anim, target=first, sfx="sound/punch.ogg")
                else:
                    player.play_attack(anim=anim, target=target, sfx="sound/punch.ogg")
            elif heal:
                player.play_action(
                    anim=anim, sfx="sound/potion.ogg", effect="glow", duration=0.5,
                )
            elif energy:
                player.play_action(
                    anim=anim, sfx="sound/powerup.ogg", effect="energy", duration=0.4,
                )
            elif draw:
                player.play_action(
                    anim=anim, sfx="sound/draw.ogg", effect="hop", duration=0.35,
                )
            else:
                player.play_action(anim=anim, duration=0.3)

            # --- Apply effects ---
            if energy:
                player.energy += energy["value"]

            if draw:
                deck.draw_cards(draw["value"])

            if heal:
                for _ in range(heal.get("times", 1)):
                    target.recover(heal["value"])
                # Heal can also cleanse a status if specified
                if heal.get("cleanse"):
                    target.remove_status(heal["cleanse"])

            if attack:
                atk_value = attack["value"]
                if player.has_status("weak"):
                    atk_value = max(1, int(atk_value * 0.75))
                for _ in range(attack.get("times", 1)):
                    if is_enemy and attack.get("all"):
                        targets = enemies.alive()
                    else:
                        targets = [target]
                    for t in targets:
                        # Hit reaction:
                        # - Specials: always play (no lunge contact)
                        # - Normal single-target: already played during play_attack
                        # - Normal all-target: play on everyone except the first (already played)
                        needs_reaction = False
                        if is_enemy:
                            if self.special:
                                needs_reaction = True
                            elif attack.get("all") and t is not targets[0]:
                                needs_reaction = True
                        if needs_reaction:
                            knock_dir = 1 if player.home_xalign < t.home_xalign else -1
                            t.play_hit_reaction(knock_dir=knock_dir)

                        t.hurt(atk_value)

                        # Status application from attack flags
                        if attack.get("stun"):
                            t.add_status("stunned", duration=attack.get("stun_duration", 1))
                        if attack.get("poison"):
                            t.add_status(
                                "poisoned",
                                duration=attack.get("poison_duration", 3),
                                stacks=attack.get("poison_stacks", 1),
                            )
                        if attack.get("burn"):
                            t.add_status(
                                "burned",
                                duration=attack.get("burn_duration", 2),
                                stacks=attack.get("burn_stacks", 1),
                            )
                        if attack.get("freeze"):
                            t.add_status("frozen", duration=attack.get("freeze_duration", 1))
                        if attack.get("weak"):
                            t.add_status("weak", duration=attack.get("weak_duration", 2))
                        if attack.get("vulnerable"):
                            t.add_status("vulnerable", duration=attack.get("vulnerable_duration", 2))

                        t.refresh_sprite()

            # Explicit status block on the card (works on any target)
            if status_spec:
                key = status_spec.get("key") or status_spec.get("name")
                if key:
                    target.add_status(
                        key,
                        duration=status_spec.get("duration"),
                        stacks=status_spec.get("stacks"),
                    )

            # Cleanse
            cleanse = self.action.get("cleanse")
            if cleanse:
                if cleanse is True:
                    target.clear_statuses()
                else:
                    target.remove_status(cleanse)

            deck.discard_card(self)


        @staticmethod
        def generate(count=1) -> list:
            """
            Generate card(s).
            """
            cards = []

            for _ in range(count):
                card_type = renpy.random.choice(
                    ["attack"] +
                    ["draw"] +
                    ["energy"] * (1 if wins > 1 else 0) +
                    ["heal"] +
                    []
                )

                card = {
                    "action": {
                        card_type: {
                            "value": renpy.random.randint(wins, max(3, wins)),
                        },
                    },
                    "cost": renpy.random.randint(1, 1 if wins < 5 else 2),
                }

                if card_type == "attack":
                    card["name"] = "Attack"
                    card["anim"] = renpy.random.choice(["attack", "punch", "kick", "slash"])
                    if renpy.random.random() < 0.3:
                        card["action"]["attack"]["stun"] = True
                        card["cost"] += 1
                    elif renpy.random.random() < 0.1:
                        card["action"]["attack"]["all"] = True
                        card["cost"] += 1
                        card["anim"] = "cast"

                elif card_type == "draw":
                    card["name"] = "Draw"
                    card["anim"] = "cast"
                    card["action"]["draw"]["value"] = renpy.random.randint(2, 3) if wins < 5 else renpy.random.randint(3, 6)

                elif card_type == "energy":
                    card["name"] = "Energy"
                    card["anim"] = "drink"
                    card["action"]["energy"] = {"value": renpy.random.randint(2, 3)}
                    card["cost"] = renpy.random.randint(1, card["action"]["energy"]["value"] - 1)

                elif card_type == "heal":
                    card["name"] = "Heal"
                    card["anim"] = "raise_hand"
                    if renpy.random.random() < 0.5:
                        card["cost"] += 1

                if card_type != "draw" and renpy.random.random() < 0.2:
                    card["action"]["draw"] = {"value": renpy.random.randint(0, 2)}

                cards.append(Card(**card))

            return cards
