# City-map hunger. Lives on the overworld, never inside combat.
# Range 0–100. Drain 4 per hour of advanced time (sleep uses half rate).
# At 0, training is blocked and the HUD shows starving.

init -10 python:

    class HungerNeed:
        def __init__(self, value=START_HUNGER):
            self.value = float(ls_clamp(value, HUNGER_MIN, HUNGER_MAX))

        @property
        def starving(self):
            return self.value <= 0

        def set(self, value):
            self.value = float(ls_clamp(value, HUNGER_MIN, HUNGER_MAX))

        def add(self, amount):
            self.set(self.value + amount)

        def drain_hours(self, hours, rate=1.0):
            if hours <= 0:
                return 0.0
            before = self.value
            self.add(-HUNGER_PER_HOUR * float(hours) * float(rate))
            return before - self.value
