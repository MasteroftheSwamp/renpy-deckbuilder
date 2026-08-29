"""Route Follower posture layer — pure Python, no Ren'Py.

Two layers on a follower:
  1. locomotion  — idle / stand / walk  (still driven by detect_movement)
  2. posture     — normal | crouch | injured | handcuffed  (exclusive)

Image-key resolution, in order:
  {posture}_{locomotion}_{dir_suffix}   e.g. crouch_walk_h, injured_stand_d
  {posture}_{locomotion}                e.g. handcuffed_idle  (mode 1 / free)
  existing locomotion key               e.g. walk_h / stand_d / idle  (fallback)

If a prefixed key exists in img_id, use that art and do NOT apply fallback
visual modifiers. Fallback modifiers exist so postures are readable without
new frames.

This module is imported by tests and (when on sys.path) by follower_states.rpy.
Drop follower_states.py into game/ as well if you want the rpy to import it;
the rpy also vendors the same functions so it is a one-file install.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Optional


POSTURES = ("normal", "crouch", "injured", "handcuffed")

POSTURE_ALIASES = {
    "normal": "normal",
    "idle": "normal",  # idle posture == standing-normal, not locomotion idle
    "crouch": "crouch",
    "injured": "injured",
    "handcuffed": "handcuffed",
    "cuffed": "handcuffed",
}

SPEED_MULT = {
    "normal": 1.0,
    "crouch": 0.45,
    "injured": 0.6,
    "handcuffed": 0.5,
}

# Fallback Transform knobs (used only when prefixed art is missing).
CROUCH_YZOOM = 0.62
INJURED_ROTATE = -4.0
INJURED_TINT = "#c46a4a"
INJURED_SATURATION = 0.45
HANDCUFFED_SHOULDER_XOFFSET = 6
HANDCUFFED_SHOULDER_YOFFSET = 2
HANDCUFFED_CUFF_SIZE = (16, 6)

# Longest-first so "handcuffed_walk_h" strips cleanly.
_POSTURE_PREFIXES = ("handcuffed_", "injured_", "crouch_", "normal_")

_DIR_TURN = {
    "left": ("h", -1.0),
    "right": ("h", 1.0),
    "up": ("u", 1.0),
    "down": ("d", 1.0),
    "up-left": ("uh", -1.0),
    "down-left": ("dh", -1.0),
    "up-right": ("uh", 1.0),
    "down-right": ("dh", 1.0),
}

_DIR_NO_TURN = {
    "left": ("hl", 1.0),
    "right": ("hr", 1.0),
    "up": ("u", 1.0),
    "down": ("d", 1.0),
    "up-left": ("uhl", 1.0),
    "down-left": ("dhl", 1.0),
    "up-right": ("uhr", 1.0),
    "down-right": ("dhr", 1.0),
}

_MODE_4_DIRS = ("left", "right", "up", "down")


class PostureError(ValueError):
    """Unknown or invalid posture name."""


def normalize_posture(name: Any) -> str:
    """Map aliases to a canonical exclusive posture. Raises PostureError if unknown."""
    if name is None:
        raise PostureError("posture is required")
    key = str(name).strip().lower()
    if key not in POSTURE_ALIASES:
        raise PostureError("unknown posture: %r (expected normal/crouch/injured/handcuffed)" % (name,))
    return POSTURE_ALIASES[key]


def speed_mult(posture: Any) -> float:
    return SPEED_MULT[normalize_posture(posture)]


def apply_speed(base_speed: float, posture: Any) -> float:
    return float(base_speed) * speed_mult(posture)


def capture_base_speed(current_speed: float, stored_base: Optional[float] = None) -> float:
    """Store Follower.speed once (install / first set_posture). Never overwrite."""
    if stored_base is None:
        return float(current_speed)
    return float(stored_base)


def strip_posture_prefix(state: Optional[str]) -> str:
    """walk_h / crouch_walk_h / handcuffed_idle → locomotion key (walk_h / idle)."""
    raw = state or ""
    for prefix in _POSTURE_PREFIXES:
        if raw.startswith(prefix):
            return raw[len(prefix):]
    return raw


def split_locomotion_state(state: Optional[str]) -> tuple:
    """Return (locomotion, dir_suffix).

    walk_h → ('walk', 'h')
    stand_dhl → ('stand', 'dhl')
    idle → ('idle', None)
    walk → ('walk', None)
    """
    raw = strip_posture_prefix(state)
    if not raw:
        return "stand", None
    if raw in ("idle", "stand", "walk"):
        return raw, None
    loco, _sep, suffix = raw.partition("_")
    if not _sep:
        return raw, None
    return loco, suffix


def locomotion_state_for_follower(
    act: str = "stand",
    direction: str = "down",
    turn: bool = True,
    directional_mode: str = "4",
) -> tuple:
    """Mirror Follower.set_follower's dir/act → (state_key, xzoom).

    Returns (None, xzoom) when the direction is invalid for that mode
    (original set_follower returns early in that case).
    locomotion maps stand→stand, walk→walk, idle→idle (mode 1 / free).
    """
    mode = str(directional_mode)
    if mode in ("1", "free"):
        return "idle", 1.0

    if mode == "4" and direction not in _MODE_4_DIRS:
        return None, 1.0

    table = _DIR_TURN if turn else _DIR_NO_TURN
    if direction not in table:
        return None, 1.0

    suffix, xzoom = table[direction]
    loco = "walk" if act == "walk" else "stand"
    return "%s_%s" % (loco, suffix), xzoom


def candidate_keys(posture: Any, locomotion_state: str) -> list:
    """Prefixed keys first, then the existing locomotion key."""
    posture = normalize_posture(posture)
    loco_state = strip_posture_prefix(locomotion_state)
    locomotion, dir_suffix = split_locomotion_state(loco_state)

    tried = []
    if dir_suffix:
        tried.append("%s_%s_%s" % (posture, locomotion, dir_suffix))
    tried.append("%s_%s" % (posture, locomotion))
    if loco_state and loco_state not in tried:
        tried.append(loco_state)
    return tried


class ResolvedKey:
    """Result of resolve_image_key."""

    __slots__ = (
        "key",
        "locomotion",
        "dir_suffix",
        "posture",
        "used_art",
        "use_fallback_modifiers",
        "tried",
        "speed_mult",
    )

    def __init__(
        self,
        key: str,
        locomotion: str,
        dir_suffix: Optional[str],
        posture: str,
        used_art: bool,
        use_fallback_modifiers: bool,
        tried: list,
    ):
        self.key = key
        self.locomotion = locomotion
        self.dir_suffix = dir_suffix
        self.posture = posture
        self.used_art = used_art
        self.use_fallback_modifiers = use_fallback_modifiers
        self.tried = list(tried)
        self.speed_mult = SPEED_MULT[posture]

    def as_dict(self) -> dict:
        return {
            "key": self.key,
            "locomotion": self.locomotion,
            "dir_suffix": self.dir_suffix,
            "posture": self.posture,
            "used_art": self.used_art,
            "use_fallback_modifiers": self.use_fallback_modifiers,
            "tried": list(self.tried),
            "speed_mult": self.speed_mult,
        }


def resolve_image_key(
    posture: Any,
    locomotion_state: str,
    img_id: Optional[Mapping] = None,
) -> ResolvedKey:
    """Pick the img_id key for this posture + locomotion state.

    locomotion_state is whatever set_follower already computed
    (walk_h, stand_d, idle, walk_hl, ...). A prefixed state is stripped
    so resolution is stable across frames.
    """
    posture = normalize_posture(posture)
    img_id = img_id or {}
    loco_state = strip_posture_prefix(locomotion_state)
    locomotion, dir_suffix = split_locomotion_state(loco_state)
    tried = candidate_keys(posture, loco_state)

    chosen = None
    for key in tried:
        if key in img_id:
            chosen = key
            break
    if chosen is None:
        chosen = loco_state or "idle"

    used_art = chosen != loco_state
    # Prefixed art → no fallback modifiers. Existing walk/stand/idle + non-normal
    # posture → apply the stand-in Transform (yzoom / lean / cuffs).
    use_fallback = (not used_art) and posture != "normal"

    return ResolvedKey(
        key=chosen,
        locomotion=locomotion,
        dir_suffix=dir_suffix,
        posture=posture,
        used_art=used_art,
        use_fallback_modifiers=use_fallback,
        tried=tried,
    )


def fallback_transform(posture: Any) -> dict:
    """Visual modifier dict applied when prefixed art is missing.

    normal:     no extra transform (speed_mult 1.0)
    crouch:     yzoom 0.62, plant feet, speed_mult 0.45
    injured:    rotate ~-4, desat / red-brown tint, speed_mult 0.6
    handcuffed: shoulders-back offset + wrists stand-in, speed_mult 0.5
    """
    p = normalize_posture(posture)
    if p == "normal":
        return {"speed_mult": 1.0}
    if p == "crouch":
        return {
            "yzoom": CROUCH_YZOOM,
            "plant_feet": True,
            "yanchor": 1.0,
            "speed_mult": SPEED_MULT["crouch"],
        }
    if p == "injured":
        return {
            "rotate": INJURED_ROTATE,
            "tint": INJURED_TINT,
            "desaturate": True,
            "saturation": INJURED_SATURATION,
            "speed_mult": SPEED_MULT["injured"],
        }
    # handcuffed — real art should show wrists cuffed behind the back.
    return {
        "shoulder_offset": True,
        "xoffset": HANDCUFFED_SHOULDER_XOFFSET,
        "yoffset": HANDCUFFED_SHOULDER_YOFFSET,
        "cuffs_overlay": True,
        "cuff_size": HANDCUFFED_CUFF_SIZE,
        "speed_mult": SPEED_MULT["handcuffed"],
    }


def apply_posture_to_state(
    posture: Any,
    act: str,
    direction: str,
    turn: bool,
    directional_mode: str,
    img_id: Optional[Mapping] = None,
) -> Optional[dict]:
    """Full resolve: dir/act → locomotion key → prefixed / fallback.

    Returns None when direction is invalid for the mode (original
    set_follower would return without updating).
    """
    loco_key, xzoom = locomotion_state_for_follower(act, direction, turn, directional_mode)
    if loco_key is None:
        return None
    resolved = resolve_image_key(posture, loco_key, img_id)
    out = resolved.as_dict()
    out["xzoom"] = xzoom
    out["locomotion_key"] = loco_key
    out["fallback"] = fallback_transform(posture) if resolved.use_fallback_modifiers else None
    return out


class PostureMachine:
    """Exclusive posture state + speed. Used by tests and as the rpy model."""

    def __init__(self, posture: str = "normal", base_speed: Optional[float] = None, speed: Optional[float] = None):
        self.posture = "normal"
        self.base_speed = None
        if speed is not None:
            self.base_speed = capture_base_speed(speed, None)
        if base_speed is not None:
            self.base_speed = float(base_speed)
        if posture and normalize_posture(posture) != "normal":
            self.set_posture(posture)

    def ensure_base_speed(self, current_speed: Optional[float] = None) -> float:
        if self.base_speed is None:
            if current_speed is None:
                raise PostureError("base_speed is not set")
            self.base_speed = capture_base_speed(current_speed, None)
        return self.base_speed

    def set_posture(self, name: Any) -> str:
        """Exclusive: the new posture replaces crouch/injured/handcuffed."""
        self.posture = normalize_posture(name)
        return self.posture

    def toggle_crouch(self) -> str:
        """If crouch → normal, else → crouch (clears injured/cuffed)."""
        if self.posture == "crouch":
            return self.set_posture("normal")
        return self.set_posture("crouch")

    def get_posture(self) -> str:
        return self.posture

    def is_crouching(self) -> bool:
        return self.posture == "crouch"

    def is_injured(self) -> bool:
        return self.posture == "injured"

    def is_handcuffed(self) -> bool:
        return self.posture == "handcuffed"

    def current_speed(self, current_speed: Optional[float] = None) -> float:
        base = self.ensure_base_speed(current_speed)
        return apply_speed(base, self.posture)
