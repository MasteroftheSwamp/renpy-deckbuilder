# Overworld / route-finder integration helpers

default arena_entrance_used = False

# Arena interact point position (on the example route, near the central junction)
define ARENA_ENTRANCE_POINT = (1002.0, 472.0)
# Visual stop-sign placement (top-left offset of the image on screen)
define ARENA_STOP_XOFFSET = 777
define ARENA_STOP_YOFFSET = 275


init python:
    def reset_arena_entrance():
        """
        Clear the one-shot flag and allow the arena entrance point
        to trigger again the next time the map is loaded.
        """
        renpy.store.arena_entrance_used = False
        try:
            for p in renpy.store.example_interact_points:
                if p.get("name") == "arena_entrance":
                    p["detected"] = False
                    p["active"] = True
        except Exception:
            pass


    def mark_arena_entrance_used():
        """Mark entrance as used and deactivate the interact point."""
        renpy.store.arena_entrance_used = True
        try:
            renpy.store.follower.togg_interact_point("arena_entrance", False)
            for p in renpy.store.example_interact_points:
                if p.get("name") == "arena_entrance":
                    p["detected"] = True
                    p["active"] = False
        except Exception:
            pass
