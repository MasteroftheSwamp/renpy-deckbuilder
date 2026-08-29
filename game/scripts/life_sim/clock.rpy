# Discrete life-sim clock. Time does not tick on the map.
# It jumps when travel commits (Follower arrives) or an activity finishes.
#
# Drop this folder into game/scripts/life_sim/ of the real project.

init -20 python:
    import math

    # ------------------------------------------------------------------
    # Constants (keep identical to life_sim.py and prototype/index.html)
    # ------------------------------------------------------------------
    PIXELS_PER_HOUR = 800
    TRAVEL_STEP_MINUTES = 15
    MIN_TRAVEL_MINUTES = 15
    HUNGER_PER_HOUR = 4
    HUNGER_SLEEP_RATE = 0.5
    TRAIN_HOURS = 2
    TRAIN_HUNGER = 15
    EAT_HOURS = 1
    EAT_HUNGER = 40
    EAT_COST = 5
    ALLEY_HOURS = 3
    ARENA_HOURS = 2
    SLEEP_WAKE_HOUR = 8
    STAT_MIN = 1
    STAT_MAX = 10
    HEALTH_BASE = 10
    HEALTH_PER_VITALITY = 5
    ENERGY_BASE = 2
    ENERGY_PER_STAMINA = 1
    ATTACK_PER_STRENGTH = 0.10
    START_HUNGER = 80
    START_CASH = 20
    START_MINUTES = 8 * 60

    PIXELS_PER_MINUTE = PIXELS_PER_HOUR / 60.0
    MINUTES_PER_DAY = 24 * 60
    HUNGER_MIN = 0
    HUNGER_MAX = 100
    START_DAY = 1
    START_LOCATION = "home"

    def ls_clamp(value, lo, hi):
        if value < lo:
            return lo
        if value > hi:
            return hi
        return value

    def ls_round_half_up(value):
        """Positive half-up rounding (matches JS Math.round)."""
        return int(math.floor(value + 0.5))

    def format_clock(day, minutes_from_midnight):
        minutes_from_midnight = int(minutes_from_midnight) % MINUTES_PER_DAY
        hours, mins = divmod(minutes_from_midnight, 60)
        return "Day {} · {:02d}:{:02d}".format(int(day), hours, mins)

    def format_duration(minutes):
        minutes = int(ls_round_half_up(max(0, minutes)))
        hours, mins = divmod(minutes, 60)
        if hours and mins:
            return "{}h {}m".format(hours, mins)
        if hours:
            return "{}h".format(hours)
        return "{}m".format(mins)


    class GameClock:
        """day (int, start 1) + minutes_from_midnight (int, start 08:00)."""

        def __init__(self, day=START_DAY, minutes_from_midnight=START_MINUTES):
            self.day = int(day)
            self.minutes_from_midnight = int(minutes_from_midnight)
            self._normalize()

        def _normalize(self):
            extra_days, minutes = divmod(int(self.minutes_from_midnight), MINUTES_PER_DAY)
            if minutes < 0:
                extra_days -= 1
                minutes += MINUTES_PER_DAY
            self.minutes_from_midnight = minutes
            self.day += extra_days

        def advance(self, minutes):
            minutes = int(minutes)
            if minutes <= 0:
                return 0
            self.minutes_from_midnight += minutes
            self._normalize()
            return minutes

        def minutes_until_next_morning(self):
            """Always jump to 08:00 *next* day (day + 1)."""
            return (MINUTES_PER_DAY - self.minutes_from_midnight) + (SLEEP_WAKE_HOUR * 60)

        def sleep_until_morning(self):
            slept = self.minutes_until_next_morning()
            self.day += 1
            self.minutes_from_midnight = SLEEP_WAKE_HOUR * 60
            return slept

        def display(self):
            return format_clock(self.day, self.minutes_from_midnight)
