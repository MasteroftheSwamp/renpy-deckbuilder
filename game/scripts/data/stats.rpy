# ---------------------------------------------------------------------------
# Designer-facing stats — vitality / stamina / strength → battle numbers.
#
#   vitality  1–10 → health_max = 10 + vitality * 5          → default 15
#   stamina   1–10 → energy_max = 2 + stamina                → default 3
#   strength  1–10 → attack_multiplier = 1.0 + (str-1)*0.10  → default 1.0
#
# Written onto Player only at fight start via apply_player_stats /
# life_sim.apply_to_player (see game/scripts/battle/battle.rpy).
#
# Hunger is NOT a battle stat. It lives in game/scripts/life_sim/needs.rpy
# and shows on the city map HUD only.
#
# Constants STAT_MIN / STAT_MAX / HEALTH_BASE / HEALTH_PER_VITALITY /
# ENERGY_BASE / ENERGY_PER_STAMINA / ATTACK_PER_STRENGTH come from
# game/scripts/life_sim/clock.rpy (init -20). Do not duplicate the numbers.
#
# attack_multiplier is on RPGCharacter. Card.use still needs this multiply
# after the weak status scale (quote only — do not rewrite card.use here):
#
#     atk_value = attack["value"]
#     if player.has_status("weak"):
#         atk_value = max(1, int(atk_value * 0.75))
#     atk_value = max(1, int(atk_value * getattr(player, "attack_multiplier", 1)))
#
# Trainable 1–10. Training +1, cap 10. HUD Stats tab + life_sim_demo.
# ---------------------------------------------------------------------------

init -15 python:

    def health_max_from_vitality(vitality):
        return HEALTH_BASE + int(vitality) * HEALTH_PER_VITALITY

    def energy_max_from_stamina(stamina):
        return ENERGY_BASE + int(stamina) * ENERGY_PER_STAMINA

    def attack_multiplier_from_strength(strength):
        return 1.0 + (int(strength) - 1) * ATTACK_PER_STRENGTH


    class LifeStats:
        def __init__(self, vitality=STAT_MIN, stamina=STAT_MIN, strength=STAT_MIN):
            self.vitality = int(ls_clamp(vitality, STAT_MIN, STAT_MAX))
            self.stamina = int(ls_clamp(stamina, STAT_MIN, STAT_MAX))
            self.strength = int(ls_clamp(strength, STAT_MIN, STAT_MAX))

        @property
        def health_max(self):
            return health_max_from_vitality(self.vitality)

        @property
        def energy_max(self):
            return energy_max_from_stamina(self.stamina)

        @property
        def attack_multiplier(self):
            return attack_multiplier_from_strength(self.strength)

        def can_train(self, stat_name):
            value = getattr(self, stat_name, None)
            if value is None:
                return False
            return value < STAT_MAX

        def train(self, stat_name):
            """+1 to a named stat, cap STAT_MAX. Returns True if it increased."""
            if not self.can_train(stat_name):
                return False
            setattr(self, stat_name, getattr(self, stat_name) + 1)
            return True


    def apply_player_stats(player, stats):
        """
        Write vitality/stamina/strength onto Player at fight start.

        If current health is above the new max, clamp it down.
        If health_max increased, do NOT auto-heal — leftover HP stays as-is.
        Current energy is not touched here; battle already refills
        player.energy = player.energy_max at the start of each player turn.
        """
        health_max = stats.health_max
        energy_max = stats.energy_max
        attack_multiplier = stats.attack_multiplier
        snapshot = {
            "health_max": health_max,
            "energy_max": energy_max,
            "attack_multiplier": attack_multiplier,
        }
        if player is None:
            return snapshot
        player.health_max = health_max
        player.energy_max = energy_max
        player.attack_multiplier = attack_multiplier
        current_health = getattr(player, "health", health_max)
        if current_health > player.health_max:
            player.health = player.health_max
        return snapshot
