# ---------------------------------------------------------------------------
# RF library loader — rooms + chains as stable IDs for story bots / authors.
#
# Register a room once, then:  $ current_rf_level = "room_id"  /  jump rf_play
# Or:  $ rf_enter_chain("chain_id")
#
# Do NOT edit follower_controller.rpy to add content.
# ---------------------------------------------------------------------------

default current_rf_chain = None

init -1 python:
    # Populated by init blocks in level files (rooftop_a_levels, vespera_patrol, …)
    RF_ROOMS = {}
    RF_CHAINS = {}


init python:

    def rf_register_room(room_id, bg, route, start, points=None,
                         follower="rooftop_a_follower", rl="rooftop_a_rl"):
        """Register one walkable screen. route/points/follower/rl are store names."""
        RF_ROOMS[room_id] = {
            "bg": bg,
            "route": route,
            "start": tuple(start),
            "points": points,
            "follower": follower,
            "rl": rl,
        }
        # Keep legacy flat dict in sync when present
        rooftop = getattr(renpy.store, "RF_ROOFTOP_A", None)
        if isinstance(rooftop, dict):
            rooftop[room_id] = {
                "bg": bg,
                "route": route,
                "start": tuple(start),
            }
        return RF_ROOMS[room_id]

    def rf_register_chain(chain_id, entry, rooms, exits=None):
        """Chain = ordered/graph of room ids. Story bot jumps the chain entry."""
        RF_CHAINS[chain_id] = {
            "entry": entry,
            "rooms": list(rooms),
            "exits": exits or {},
        }
        return RF_CHAINS[chain_id]

    def rf_get_room(room_id):
        return RF_ROOMS.get(room_id)

    def rf_current_bg():
        info = RF_ROOMS.get(renpy.store.current_rf_level)
        if info:
            return info["bg"]
        # Legacy fallback
        rooftop = getattr(renpy.store, "RF_ROOFTOP_A", None) or {}
        info = rooftop.get(renpy.store.current_rf_level) or {}
        return info.get("bg", "maps/rooftop-a/map_rooftop-a_1.jpg")

    def rf_current_route():
        info = RF_ROOMS.get(renpy.store.current_rf_level)
        if info:
            return getattr(renpy.store, info["route"])
        rooftop = getattr(renpy.store, "RF_ROOFTOP_A", {})
        info = rooftop[renpy.store.current_rf_level]
        return getattr(renpy.store, info["route"])

    def rf_current_start():
        info = RF_ROOMS.get(renpy.store.current_rf_level)
        if info:
            return info["start"]
        rooftop = getattr(renpy.store, "RF_ROOFTOP_A", {})
        return rooftop[renpy.store.current_rf_level]["start"]

    def rf_load_room(room_id):
        """Load bg route + points onto the shared rooftop follower and editor."""
        info = RF_ROOMS.get(room_id)
        if not info:
            # Fall back to legacy RF_ROOFTOP_A-only ids
            rooftop = getattr(renpy.store, "RF_ROOFTOP_A", {})
            if room_id not in rooftop:
                renpy.notify("Unknown RF room: {}".format(room_id))
                return False
            info = {
                "bg": rooftop[room_id]["bg"],
                "route": rooftop[room_id]["route"],
                "start": rooftop[room_id]["start"],
                "points": None,
                "follower": "rooftop_a_follower",
                "rl": "rooftop_a_rl",
            }

        renpy.store.current_rf_level = room_id
        route = getattr(renpy.store, info["route"])
        start = info["start"]
        follower = getattr(renpy.store, info["follower"])
        rl = getattr(renpy.store, info["rl"])

        load_predefined_route(rl, route)

        points = []
        if info.get("points"):
            points = getattr(renpy.store, info["points"])
            for _pt in points:
                if not _pt.get("once") or _pt.get("active", True):
                    _pt["detected"] = False
            follower.load_interact_points(points)
        else:
            # Keep existing points only if already loaded; otherwise empty
            if not follower.follower.interact_points:
                follower.load_interact_points([])

        follower.set_teleport(start[0], start[1], follower.route.lines)
        follower.reset_follower()

        # Editor mirror
        load_predefined_route(renpy.store.interactive_line, route)
        renpy.store.test_follower.load_interact_points(
            follower.follower.interact_points
        )
        renpy.store.test_follower.set_teleport(
            start[0], start[1], renpy.store.test_follower.route.lines
        )
        renpy.store.test_follower.reset_follower()
        return True

    def rf_enter_chain(chain_id, room_id=None):
        """Set active chain and jump into a room (default: chain entry)."""
        chain = RF_CHAINS.get(chain_id)
        if not chain:
            renpy.notify("Unknown RF chain: {}".format(chain_id))
            return
        renpy.store.current_rf_chain = chain_id
        renpy.store.current_rf_level = room_id or chain["entry"]
        renpy.jump("rf_play")

    def rf_chain_exit(to_room_id):
        """Swap room inside the current chain (call from an interact label)."""
        renpy.store.current_rf_level = to_room_id
        renpy.jump("rf_play")
