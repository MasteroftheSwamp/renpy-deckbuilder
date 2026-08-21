default enemies = Enemies()


init python:
    class Enemies:
        YALIGN = 1.0


        def __init__(self) -> None:
            self.enemies = []
            self.count = 0


        def generate(self, enemies: list) -> None:
            """
            Generate enemies.
            """
            self.enemies = []
            self.count = len(enemies)

            for enemy in enemies:
                self.enemies.append(RPGCharacter(**enemy))


        def show(self) -> None:
            """
            Show enemies.
            """
            for index, enemy in enumerate(self.enemies):
                xalign_position = self.xalign_position(enemy)
                enemy.home_xalign = xalign_position
                renpy.show_screen(f"enemy_stats{index}", enemy, xalign_position)
                enemy.refresh_sprite()

            renpy.with_statement(dissolve)


        def hide(self, enemy: RPGCharacter) -> None:
            """
            Hide enemy.
            """
            enemy.hide_all_states()
            try:
                renpy.hide_screen(f"enemy_stats{enemies.index(enemy)}")
            except Exception:
                pass
            renpy.transition(dissolve, layer=LAYER_ENEMIES)


        def get(self, enemy_id: str) -> RPGCharacter:
            """
            Get enemy by id.
            """
            return find(self.enemies, {"id": enemy_id})


        def index(self, enemy: RPGCharacter) -> int:
            """
            Get enemy index.
            """
            return self.enemies.index(enemy)


        def alive(self) -> list:
            """
            Get alive enemies.
            """
            return list(filter(lambda enemy: enemy.health > 0, self.enemies))


        def dead(self) -> bool:
            """
            Whether enemies are dead.
            """
            return not bool(len(self.alive()))


        def xalign_position(self, enemy: RPGCharacter) -> float:
            """
            Get enemy xalign position (right side of the screen so they face the player).
            """
            count = self.count
            index = self.enemies.index(enemy)

            if count == 1:
                xalign_position = 0.8

            elif count == 2:
                if index == 0:
                    xalign_position = 0.65
                elif index == 1:
                    xalign_position = 0.9

            elif count == 3:
                if index == 0:
                    xalign_position = 0.55
                elif index == 1:
                    xalign_position = 0.75
                elif index == 2:
                    xalign_position = 0.95

            elif count == 4:
                if index == 0:
                    xalign_position = 0.5
                elif index == 1:
                    xalign_position = 0.65
                elif index == 2:
                    xalign_position = 0.8
                elif index == 3:
                    xalign_position = 0.95

            elif count == 5:
                if index == 0:
                    xalign_position = 0.45
                elif index == 1:
                    xalign_position = 0.6
                elif index == 2:
                    xalign_position = 0.75
                elif index == 3:
                    xalign_position = 0.85
                elif index == 4:
                    xalign_position = 1.0

            return xalign_position


        def turn(self) -> None:
            """
            Enemy turn.
            """
            for enemy in self.alive():
                has_actions = bool(enemy.actions)

                # Action-blocking statuses (stunned, frozen, ...)
                if enemy.is_action_blocked():
                    narrator(enemy.say())
                    if has_actions:
                        enemy.actions.append(enemy.actions.pop(0))
                    enemy.refresh_sprite()
                    continue

                # Generate a random action when none are scripted
                if not has_actions:
                    if enemy.health < enemy.health_max and renpy.random.random() < 0.5:
                        heal = renpy.random.randint(enemy.heal_min, enemy.heal_max)
                        enemy.actions.append({
                            "say": f"{enemy.name} healed {heal} health.",
                            "heal": heal,
                            "anim": "raise_hand",
                        })
                    else:
                        attack = round(
                            renpy.random.randint(enemy.attack_min, enemy.attack_max)
                            * enemy.attack_multiplier
                        )
                        # Weak status reduces outgoing damage
                        if enemy.has_status("weak"):
                            attack = max(1, int(attack * 0.75))
                        enemy.actions.append({
                            "say": f"{enemy.name} dealt {attack} damage to you.",
                            "attack": attack,
                            "anim": "punch",
                        })

                narrator(enemy.say())
                action = enemy.actions.pop(0)

                anim = action.get("anim") or ("raise_hand" if action.get("heal") else "attack")
                attack = action.get("attack")
                heal = action.get("heal")

                if attack:
                    if enemy.has_status("weak"):
                        attack = max(1, int(attack * 0.75))
                    enemy.play_attack(
                        anim=anim,
                        target=player,
                        sfx="sound/punch.ogg",
                    )
                    renpy.with_statement(vpunch)
                    player.hurt(attack)

                    if player.health <= 0:
                        renpy.jump("lose")

                elif heal:
                    enemy.play_action(
                        anim=anim,
                        sfx="sound/potion.ogg",
                        effect="glow",
                        duration=0.5,
                    )
                    enemy.recover(heal)
                    if action.get("cleanse"):
                        enemy.remove_status(action["cleanse"])

                else:
                    if anim and anim != "idle":
                        enemy.play_action(anim=anim, duration=0.4)
                    else:
                        renpy.pause(0.3)

                self._apply_action_status(action, player)
                player.refresh_sprite()

                if has_actions:
                    enemy.actions.append(action)

                enemy.refresh_sprite()

            self.end_turn()


        def _apply_action_status(self, action, target) -> None:
            """Apply status effects from an enemy action onto target (usually the player)."""
            for spec in action.get("statuses") or []:
                key = spec.get("key") or spec.get("name")
                if key:
                    target.add_status(
                        key,
                        duration=spec.get("duration"),
                        stacks=spec.get("stacks"),
                    )

            status = action.get("status")
            if isinstance(status, str):
                target.add_status(
                    status,
                    duration=action.get("status_duration"),
                    stacks=action.get("status_stacks"),
                )
            elif isinstance(status, dict):
                key = status.get("key") or status.get("name")
                if key:
                    target.add_status(
                        key,
                        duration=status.get("duration"),
                        stacks=status.get("stacks"),
                    )

            if action.get("stun") or action.get("stunned"):
                target.add_status("stunned", duration=action.get("stun_duration", 1))
            if action.get("poison") or action.get("poisoned"):
                target.add_status(
                    "poisoned",
                    duration=action.get("poison_duration", 3),
                    stacks=action.get("poison_stacks", 1),
                )
            if action.get("burn") or action.get("burned"):
                target.add_status(
                    "burned",
                    duration=action.get("burn_duration", 2),
                    stacks=action.get("burn_stacks", 1),
                )
            if action.get("freeze") or action.get("frozen"):
                target.add_status("frozen", duration=action.get("freeze_duration", 1))
            if action.get("weak"):
                target.add_status("weak", duration=action.get("weak_duration", 2))
            if action.get("vulnerable"):
                target.add_status("vulnerable", duration=action.get("vulnerable_duration", 2))


        def end_turn(self) -> None:
            """
            Tick end-of-turn statuses on every living enemy (poison DoT, duration, etc.).
            """
            for enemy in self.alive():
                messages = enemy.tick_statuses("end_turn")
                for msg in messages:
                    narrator(msg)
                if enemy.health <= 0:
                    self.hide(enemy)
