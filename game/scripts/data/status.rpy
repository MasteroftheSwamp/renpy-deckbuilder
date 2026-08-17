init -1 python:
    class StatusDef:
        """
        Definition for a single status type.
        Add new statuses here — the rest of the system picks them up automatically.
        """
        def __init__(
            self,
            key,
            name,
            icon="•",
            tint=None,
            idle_suffix=None,
            blocks_action=False,
            tick_when=None,
            default_duration=1,
            default_stacks=1,
        ):
            self.key = key
            self.name = name
            self.icon = icon
            self.tint = tint                  # hex colour applied while active
            self.idle_suffix = idle_suffix    # used to build idle_<suffix> / idle_<suffix>_low
            self.blocks_action = blocks_action
            self.tick_when = tick_when        # "end_turn" | "start_turn" | None
            self.default_duration = default_duration
            self.default_stacks = default_stacks


    # Registry — extend this dict to add burn, freeze, weak, vulnerable, shield, etc.
    STATUS_DEFS = {
        "stunned": StatusDef(
            key="stunned",
            name="Stunned",
            icon="💫",
            tint="#c0c080",
            idle_suffix="stunned",
            blocks_action=True,
            tick_when="end_turn",
            default_duration=1,
        ),
        "poisoned": StatusDef(
            key="poisoned",
            name="Poisoned",
            icon="☠️",
            tint="#66cc66",
            idle_suffix="poisoned",
            blocks_action=False,
            tick_when="end_turn",
            default_duration=3,
            default_stacks=1,
        ),
        "burned": StatusDef(
            key="burned",
            name="Burned",
            icon="🔥",
            tint="#ff8844",
            idle_suffix="burned",
            blocks_action=False,
            tick_when="end_turn",
            default_duration=2,
            default_stacks=1,
        ),
        "frozen": StatusDef(
            key="frozen",
            name="Frozen",
            icon="❄️",
            tint="#88ccff",
            idle_suffix="frozen",
            blocks_action=True,
            tick_when="end_turn",
            default_duration=1,
        ),
        "weak": StatusDef(
            key="weak",
            name="Weak",
            icon="📉",
            tint="#cc88cc",
            idle_suffix="weak",
            blocks_action=False,
            tick_when="end_turn",
            default_duration=2,
        ),
        "vulnerable": StatusDef(
            key="vulnerable",
            name="Vulnerable",
            icon="💥",
            tint="#ff6666",
            idle_suffix="vulnerable",
            blocks_action=False,
            tick_when="end_turn",
            default_duration=2,
        ),
        "shielded": StatusDef(
            key="shielded",
            name="Shielded",
            icon="🛡️",
            tint="#88aaff",
            idle_suffix="shielded",
            blocks_action=False,
            tick_when="end_turn",
            default_duration=2,
        ),
    }

    # Priority when multiple statuses affect idle (first match wins)
    STATUS_IDLE_PRIORITY = ["stunned", "frozen", "poisoned", "burned", "weak", "vulnerable", "shielded"]

    # Health ratio at or below which idle_low is used
    LOW_HP_RATIO = 0.30
