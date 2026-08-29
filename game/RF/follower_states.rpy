################################################################################
## Route Follower — POSTURE state machine (drop-in)
##
## Copy this file into game/RF/  (or game/scripts/).
## Optionally also copy follower_states.py into game/ so this wrap can import
## the same resolver the unit tests use. If the .py is missing, the functions
## below are vendored so this file still works on its own.
##
## After launch:
##     rooftop_a_follower.set_posture("crouch")
##     rooftop_a_follower.set_posture("injured")
##     rooftop_a_follower.set_posture("handcuffed")
##     rooftop_a_follower.toggle_crouch()
##
## Stealth can later call set_posture("crouch").
##
## Does NOT rewrite follower_controller.rpy. Wraps Follower.__init__,
## Follower.set_follower, and Follower.detect_movement at init 1.
## change_follower_act (angry/happy/sad) is left alone; the next
## detect_movement → set_follower restores posture + locomotion.
################################################################################

init 1 python:
    ############################################################################
    ## Shared resolver (import follower_states if present, else vendor)
    ############################################################################
    import sys
    import os

    for _rfs_dir in (
        renpy.config.gamedir,
        os.path.join(renpy.config.gamedir, "RF"),
        os.path.join(renpy.config.gamedir, ".."),
    ):
        if _rfs_dir and _rfs_dir not in sys.path:
            sys.path.insert(0, _rfs_dir)

    try:
        import follower_states as _rfs
    except ImportError:
        _rfs = None

    if _rfs is None:
        # --- vendored copy of follower_states.py (keep in sync) ---------------
        class _Rfs:
            POSTURES = ("normal", "crouch", "injured", "handcuffed")
            POSTURE_ALIASES = {
                "normal": "normal",
                "idle": "normal",
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
            CROUCH_YZOOM = 0.62
            INJURED_ROTATE = -4.0
            INJURED_TINT = "#c46a4a"
            INJURED_SATURATION = 0.45
            HANDCUFFED_SHOULDER_XOFFSET = 6
            HANDCUFFED_SHOULDER_YOFFSET = 2
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
                pass

            @staticmethod
            def normalize_posture(name):
                if name is None:
                    raise _Rfs.PostureError("posture is required")
                key = str(name).strip().lower()
                if key not in _Rfs.POSTURE_ALIASES:
                    raise _Rfs.PostureError("unknown posture: %r" % (name,))
                return _Rfs.POSTURE_ALIASES[key]

            @staticmethod
            def speed_mult(posture):
                return _Rfs.SPEED_MULT[_Rfs.normalize_posture(posture)]

            @staticmethod
            def apply_speed(base_speed, posture):
                return float(base_speed) * _Rfs.speed_mult(posture)

            @staticmethod
            def capture_base_speed(current_speed, stored_base=None):
                if stored_base is None:
                    return float(current_speed)
                return float(stored_base)

            @staticmethod
            def strip_posture_prefix(state):
                raw = state or ""
                for prefix in _Rfs._POSTURE_PREFIXES:
                    if raw.startswith(prefix):
                        return raw[len(prefix):]
                return raw

            @staticmethod
            def split_locomotion_state(state):
                raw = _Rfs.strip_posture_prefix(state)
                if not raw:
                    return "stand", None
                if raw in ("idle", "stand", "walk"):
                    return raw, None
                loco, sep, suffix = raw.partition("_")
                if not sep:
                    return raw, None
                return loco, suffix

            @staticmethod
            def locomotion_state_for_follower(act="stand", direction="down", turn=True, directional_mode="4"):
                mode = str(directional_mode)
                if mode in ("1", "free"):
                    return "idle", 1.0
                if mode == "4" and direction not in _Rfs._MODE_4_DIRS:
                    return None, 1.0
                table = _Rfs._DIR_TURN if turn else _Rfs._DIR_NO_TURN
                if direction not in table:
                    return None, 1.0
                suffix, xzoom = table[direction]
                loco = "walk" if act == "walk" else "stand"
                return "%s_%s" % (loco, suffix), xzoom

            @staticmethod
            def candidate_keys(posture, locomotion_state):
                posture = _Rfs.normalize_posture(posture)
                loco_state = _Rfs.strip_posture_prefix(locomotion_state)
                locomotion, dir_suffix = _Rfs.split_locomotion_state(loco_state)
                tried = []
                if dir_suffix:
                    tried.append("%s_%s_%s" % (posture, locomotion, dir_suffix))
                tried.append("%s_%s" % (posture, locomotion))
                if loco_state and loco_state not in tried:
                    tried.append(loco_state)
                return tried

            @staticmethod
            def resolve_image_key(posture, locomotion_state, img_id=None):
                posture = _Rfs.normalize_posture(posture)
                img_id = img_id or {}
                loco_state = _Rfs.strip_posture_prefix(locomotion_state)
                locomotion, dir_suffix = _Rfs.split_locomotion_state(loco_state)
                tried = _Rfs.candidate_keys(posture, loco_state)
                chosen = None
                for key in tried:
                    if key in img_id:
                        chosen = key
                        break
                if chosen is None:
                    chosen = loco_state or "idle"
                used_art = chosen != loco_state
                use_fallback = (not used_art) and posture != "normal"

                class _RK:
                    pass
                r = _RK()
                r.key = chosen
                r.locomotion = locomotion
                r.dir_suffix = dir_suffix
                r.posture = posture
                r.used_art = used_art
                r.use_fallback_modifiers = use_fallback
                r.tried = tried
                r.speed_mult = _Rfs.SPEED_MULT[posture]
                return r

            @staticmethod
            def fallback_transform(posture):
                p = _Rfs.normalize_posture(posture)
                if p == "normal":
                    return {"speed_mult": 1.0}
                if p == "crouch":
                    return {"yzoom": 0.62, "plant_feet": True, "yanchor": 1.0, "speed_mult": 0.45}
                if p == "injured":
                    return {"rotate": -4.0, "tint": "#c46a4a", "desaturate": True, "saturation": 0.45, "speed_mult": 0.6}
                return {
                    "shoulder_offset": True,
                    "xoffset": 6,
                    "yoffset": 2,
                    "cuffs_overlay": True,
                    "speed_mult": 0.5,
                }

        _rfs = _Rfs
        # --- end vendored copy ------------------------------------------------

    store._rf_posture_mod = _rfs


    ############################################################################
    ## Transform builder — fallback visuals WITHOUT new art
    ############################################################################
    def _rf_make_child(image, xzoom, posture, use_fallback):
        """Build the follower child Transform.

        If prefixed art exists (use_fallback False), only apply facing xzoom.
        If falling back to walk/stand/idle, apply posture stand-ins:
          crouch     — yzoom 0.62, feet planted (yanchor 1.0)
          injured    — lean ~-4°, desat / red-brown tint
          handcuffed — shoulders back + tiny cuff rect behind the torso
                       (real art should show wrists cuffed behind the back)
        """
        if (not use_fallback) or posture == "normal":
            return Transform(image, xzoom=xzoom)

        if posture == "crouch":
            return Transform(
                image,
                xzoom=xzoom,
                yzoom=0.62,
                yanchor=1.0,
                xanchor=0.5,
                anchor=(0.5, 1.0),
                transform_anchor=True,
            )

        if posture == "injured":
            kw = dict(
                xzoom=xzoom,
                rotate=-4,
                anchor=(0.5, 1.0),
                transform_anchor=True,
            )
            try:
                kw["matrixcolor"] = SaturationMatrix(0.45) * TintMatrix("#c46a4a")
            except Exception:
                pass
            return Transform(image, **kw)

        if posture == "handcuffed":
            # Shoulders-back offset. Tiny dark bar = wrists stand-in.
            # Real art should show wrists cuffed behind the back.
            sign = 1.0 if xzoom >= 0 else -1.0
            body = Transform(image, xzoom=xzoom, xoffset=int(6 * sign), yoffset=2)
            try:
                cuff = Transform(Solid("#1c1814"), xysize=(16, 6))
                # Body first so fit_first uses sprite size; cuff drawn on top
                # at the small of the back (reads as cuffs behind the torso).
                return Fixed(
                    body,
                    Transform(cuff, xalign=0.5, yalign=0.48, xoffset=int(-10 * sign)),
                    fit_first=True,
                )
            except Exception:
                return body

        return Transform(image, xzoom=xzoom)


    def _rf_ensure_posture_attrs(self):
        if not hasattr(self, "posture") or self.posture is None:
            self.posture = "normal"
        if not hasattr(self, "base_speed"):
            self.base_speed = None
        if getattr(self, "base_speed", None) is None:
            try:
                self.base_speed = _rfs.capture_base_speed(self.speed, None)
            except Exception:
                self.base_speed = float(getattr(self, "speed", 0) or 0)


    def _rf_apply_posture_speed(self):
        """follower.speed = base_speed * speed_mult. Idempotent."""
        _rf_ensure_posture_attrs(self)
        try:
            posture = _rfs.normalize_posture(getattr(self, "posture", "normal"))
        except Exception:
            posture = "normal"
            self.posture = "normal"
        self.speed = _rfs.apply_speed(self.base_speed, posture)


    def _rf_apply_posture_visuals(self):
        """Override child/state after original set_follower computed dir/act.

        KEEP original dir/act. Only change how the image key is built and
        how Transform is applied.
        """
        _rf_ensure_posture_attrs(self)
        img_id = getattr(self, "img_id", None) or {}
        if not img_id:
            return

        try:
            posture = _rfs.normalize_posture(getattr(self, "posture", "normal"))
        except Exception:
            posture = "normal"

        loco_key, xzoom = _rfs.locomotion_state_for_follower(
            getattr(self, "act", "stand"),
            getattr(self, "dir", "down"),
            getattr(self, "turn", True),
            getattr(self, "directional_mode", "4"),
        )
        if loco_key is None:
            return  # invalid dir — original set_follower returned early

        resolved = _rfs.resolve_image_key(posture, loco_key, img_id)
        key = resolved.key
        if key not in img_id:
            return

        self.state = key
        image = img_id[key]["image"]
        self.child = _rf_make_child(image, xzoom, posture, resolved.use_fallback_modifiers)


    ############################################################################
    ## Follower API  (proxied onto FollowerDisplayable via __getattr__)
    ############################################################################
    def _rf_follower_set_posture(self, name):
        _rf_ensure_posture_attrs(self)
        self.posture = _rfs.normalize_posture(name)
        _rf_apply_posture_speed(self)
        self.state_changed = True
        self.set_follower()
        return self.posture

    def _rf_follower_toggle_crouch(self):
        _rf_ensure_posture_attrs(self)
        if getattr(self, "posture", "normal") == "crouch":
            return self.set_posture("normal")
        return self.set_posture("crouch")

    def _rf_follower_get_posture(self):
        _rf_ensure_posture_attrs(self)
        return self.posture

    def _rf_follower_is_crouching(self):
        return self.get_posture() == "crouch"

    def _rf_follower_is_injured(self):
        return self.get_posture() == "injured"

    def _rf_follower_is_handcuffed(self):
        return self.get_posture() == "handcuffed"


    ############################################################################
    ## Wrap Follower  (init 1 — class already exists from follower_controller)
    ############################################################################
    def _rf_install_posture_layer():
        F = globals().get("Follower")
        if F is None:
            F = getattr(renpy.store, "Follower", None)
        if F is None:
            return False
        if getattr(F, "_rf_posture_wrapped", False):
            return True

        _orig_init = F.__init__
        _orig_set_follower = F.set_follower
        _orig_detect_movement = F.detect_movement
        _orig_reset = getattr(F, "reset_follower", None)

        def _wrapped_init(self, *args, **kwargs):
            # Set posture BEFORE original __init__ so the first set_follower
            # (called at the end of Follower.__init__) sees it.
            self.posture = "normal"
            self.base_speed = None
            _orig_init(self, *args, **kwargs)
            if getattr(self, "base_speed", None) is None:
                self.base_speed = _rfs.capture_base_speed(self.speed, None)
            _rf_apply_posture_speed(self)

        def _wrapped_set_follower(self):
            # Original logic for dir/act → walk_h / stand_d / idle + xzoom.
            _orig_set_follower(self)
            # Then resolve prefixed keys / fallback Transforms.
            _rf_apply_posture_visuals(self)

        def _wrapped_detect_movement(self):
            _orig_detect_movement(self)
            # Re-apply so pause/play cannot stick a wrong speed.
            _rf_apply_posture_speed(self)

        def _wrapped_reset_follower(self):
            if _orig_reset is not None:
                _orig_reset(self)
            self.state_changed = True
            _rf_apply_posture_visuals(self)
            _rf_apply_posture_speed(self)

        F.__init__ = _wrapped_init
        F.set_follower = _wrapped_set_follower
        F.detect_movement = _wrapped_detect_movement
        if _orig_reset is not None:
            F.reset_follower = _wrapped_reset_follower

        F.set_posture = _rf_follower_set_posture
        F.toggle_crouch = _rf_follower_toggle_crouch
        F.get_posture = _rf_follower_get_posture
        F.is_crouching = _rf_follower_is_crouching
        F.is_injured = _rf_follower_is_injured
        F.is_handcuffed = _rf_follower_is_handcuffed
        F._rf_posture_wrapped = True
        return True

    store._rf_posture_ok = _rf_install_posture_layer()


init 2 python:
    # Retry one priority later if Follower was also declared at init 1.
    if not getattr(renpy.store, "_rf_posture_ok", False):
        store._rf_posture_ok = _rf_install_posture_layer()
