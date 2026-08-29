# LifeSim facade. One store object owns clock, hunger, stats, cash, pending travel.
#
#   default life_sim = LifeSim()
#
# apply_to_player(player) writes maxima at fight start only:
#   vitality  → player.health_max
#   stamina   → player.energy_max
#   strength  → player.attack_multiplier
#
# If current health > new max, clamp down.
# If health_max increased, do NOT auto-heal — leftover HP stays as-is.
# Current energy is not touched here; battle already does
# `player.energy = player.energy_max` at the start of each player turn
# after enemy_turn (game/scripts/battle/enemy_turn.rpy).
#
# ---------------------------------------------------------------------------
# THE ONE card.use CHANGE
# ---------------------------------------------------------------------------
# attack_multiplier already exists on RPGCharacter (default 1) but is unused.
# In game/scripts/data/card.rpy Card.use, after the weak status scale, multiply:
#
#     atk_value = attack["value"]
#     if player.has_status("weak"):
#         atk_value = max(1, int(atk_value * 0.75))
#     atk_value = max(1, int(atk_value * getattr(player, "attack_multiplier", 1)))
#
# That is the only battle code impact. Do not rewrite card.use here.
# ---------------------------------------------------------------------------
#
# Cash is a local float (start $20). Later this should share the game's
# `money` store (`default money = 0` in game/scripts/battle/win.rpy).

init python:

    class LifeSim:
        def __init__(self):
            self.clock = GameClock()
            self.stats = LifeStats()
            self.hunger = HungerNeed()
            self.cash = int(START_CASH)
            self.pending_minutes = 0
            self.location = START_LOCATION
            self.log = []

        @property
        def starving(self):
            return self.hunger.starving

        def display_time(self):
            return self.clock.display()

        @property
        def location_label(self):
            return NODE_LABELS.get(self.location, self.location)

        def hunger_display(self):
            return int(ls_round_half_up(self.hunger.value))

        def battle_snapshot(self):
            return {
                "health_max": self.stats.health_max,
                "energy_max": self.stats.energy_max,
                "attack_multiplier": self.stats.attack_multiplier,
            }

        def _advance_minutes(self, minutes, hunger_rate=1.0, hunger_delta=0):
            minutes = int(minutes)
            if minutes < 0:
                minutes = 0
            hunger_before = self.hunger.value
            applied = self.clock.advance(minutes)
            hours = applied / 60.0
            self.hunger.drain_hours(hours, rate=hunger_rate)
            if hunger_delta:
                self.hunger.add(hunger_delta)
            return {
                "minutes": applied,
                "hunger_before": hunger_before,
                "hunger_after": self.hunger.value,
            }

        def note_travel(self, points):
            """Stash pending minutes from path pixel length. Replaces any previous pending."""
            length = path_pixel_length(points)
            self.pending_minutes = travel_minutes_from_pixels(length)
            return self.pending_minutes

        def commit_travel(self, dest=None):
            """Advance clock + hunger by pending minutes, then clear pending."""
            if dest is not None:
                self.location = dest
            pending = int(self.pending_minutes or 0)
            self.pending_minutes = 0
            if pending <= 0:
                return {
                    "minutes": 0,
                    "hunger_before": self.hunger.value,
                    "hunger_after": self.hunger.value,
                }
            result = self._advance_minutes(pending)
            self._log(
                "Walked to {} · {}".format(
                    NODE_LABELS.get(self.location, self.location),
                    format_duration(result["minutes"]),
                )
            )
            self._log_hunger(result["hunger_before"], result["hunger_after"])
            return result

        def cancel_travel(self):
            """Clear pending without applying (teleport / aborted path)."""
            self.pending_minutes = 0

        def travel_to(self, dest):
            """
            Demo helper (no RF): shortest path from the current node, stash + commit.
            The real game should call note_travel / commit_travel from Follower.
            """
            dest = str(dest)
            if dest not in CITY_NODES:
                return {
                    "minutes": 0,
                    "hunger_before": self.hunger.value,
                    "hunger_after": self.hunger.value,
                }
            if dest == self.location:
                self.cancel_travel()
                return {
                    "minutes": 0,
                    "hunger_before": self.hunger.value,
                    "hunger_after": self.hunger.value,
                }
            points = shortest_path_points(self.location, dest)
            self.note_travel(points)
            return self.commit_travel(dest)

        def finish_activity(self, activity_id):
            """Look up duration (and optional hunger delta) then apply."""
            spec = ACTIVITIES.get(activity_id)
            if not spec:
                return {"ok": False, "reason": "unknown", "minutes": 0}
            hours = spec.get("hours", 0)
            minutes = int(ls_round_half_up(hours * 60))
            hunger_delta = spec.get("hunger_delta", 0)
            result = self._advance_minutes(minutes, hunger_delta=hunger_delta)
            label = spec.get("label", activity_id)
            self._log("{} · {}".format(label, format_duration(result["minutes"])))
            self._log_hunger(result["hunger_before"], result["hunger_after"])
            result["ok"] = True
            result["activity"] = activity_id
            return result

        def train(self, stat_name):
            """Gym: 2 hours, hunger -15 (on top of time drain), +1 to chosen stat."""
            if self.starving:
                return {"ok": False, "reason": "starving"}
            if stat_name not in ("vitality", "stamina", "strength"):
                return {"ok": False, "reason": "unknown_stat"}
            if not self.stats.can_train(stat_name):
                return {"ok": False, "reason": "capped"}
            self.stats.train(stat_name)
            result = self.finish_activity("train")
            result["stat"] = stat_name
            result["value"] = getattr(self.stats, stat_name)
            self._log("Trained {} → {}".format(stat_name, result["value"]))
            return result

        def eat(self):
            """Cafe: 1 hour, hunger +40, costs $5 from the local cash float."""
            if self.cash < EAT_COST:
                return {"ok": False, "reason": "broke"}
            self.cash -= EAT_COST
            result = self.finish_activity("eat")
            result["cash"] = self.cash
            self._log("Paid ${} · cash ${}".format(EAT_COST, self.cash))
            return result

        def sleep(self):
            """Home: jump to 08:00 next day. Hunger drains at HALF the normal rate."""
            hunger_before = self.hunger.value
            slept = self.clock.sleep_until_morning()
            hours = slept / 60.0
            self.hunger.drain_hours(hours, rate=HUNGER_SLEEP_RATE)
            self._log(
                "Slept · {} · woke {}".format(
                    format_duration(slept),
                    self.clock.display(),
                )
            )
            self._log_hunger(hunger_before, self.hunger.value)
            return {
                "ok": True,
                "minutes": slept,
                "hunger_before": hunger_before,
                "hunger_after": self.hunger.value,
            }

        def apply_to_player(self, player):
            """
            Write life-sim maxima onto the battle Player at fight start.

            If current health is above the new max, clamp it down.
            If health_max increased, do NOT auto-heal — leftover HP stays as-is.
            """
            snapshot = self.battle_snapshot()
            if player is None:
                return snapshot
            player.health_max = snapshot["health_max"]
            player.energy_max = snapshot["energy_max"]
            player.attack_multiplier = snapshot["attack_multiplier"]
            current_health = getattr(player, "health", snapshot["health_max"])
            if current_health > player.health_max:
                player.health = player.health_max
            return snapshot

        def start_fight(self, player=None):
            snapshot = self.apply_to_player(player)
            result = self.finish_activity("arena")
            result["snapshot"] = snapshot
            return result

        def reset(self):
            self.clock = GameClock()
            self.stats = LifeStats()
            self.hunger = HungerNeed()
            self.cash = int(START_CASH)
            self.pending_minutes = 0
            self.location = START_LOCATION
            self.log = []
            self._log(
                "New run · {} · hunger {} · ${}".format(
                    self.clock.display(),
                    int(self.hunger.value),
                    self.cash,
                )
            )
            return self

        def _log(self, line):
            self.log.append(line)

        def _log_hunger(self, before, after):
            b = int(ls_round_half_up(before))
            a = int(ls_round_half_up(after))
            if b != a:
                self.log.append("Hunger {} → {}".format(b, a))
            if self.starving:
                self.log.append("Starving — training blocked")


default life_sim = LifeSim()
