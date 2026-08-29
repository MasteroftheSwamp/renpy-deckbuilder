# RF travel helpers + activity durations.
#
# Do NOT monkeypatch Follower in this prototype. When you port, hook
# game/RF/follower_controller.rpy yourself:
#
#   1. Follower.set_destination  (success path, after
#      `self.path = self.route_points[:]` and `self.path_active = True`)
#      AND the matching success assignment in Follower.set_button_destination:
#          life_sim.note_travel(self.route_points)
#      Stash pending minutes from the path pixel length at click time.
#      If the player clicks a new destination mid-walk, note_travel REPLACES
#      the pending amount — do not double-charge.
#
#   2. Follower.update  (when the last path node is popped):
#          if not self.path:
#              self.destination = None
#              self.path_active = False
#              self.moving = False
#              life_sim.commit_travel()   # BEFORE reach_action()
#              if self.label_active:
#                  self.reach_action()
#
#   3. Follower.set_teleport:
#          life_sim.cancel_travel()      # clear pending, do not apply
#
#   4. Scenario labels (alley): at the end of the scene, BEFORE jumping
#      back to the city:
#          $ life_sim.finish_activity("alley")
#      Walking there is extra travel time on top of this fixed duration.
#
# Inside init-python Follower methods, use renpy.store.life_sim if the
# bare name is not in scope.

init -10 python:

    NODE_LABELS = {
        "home": "Home",
        "gym": "Gym",
        "cafe": "Cafe",
        "alley": "Alley",
        "arena": "Arena",
    }

    # Demo-only schematic graph (the real city uses RF route_points).
    # Same coordinates as life_sim.py / prototype/index.html.
    CITY_NODES = {
        "home": (100.0, 280.0),
        "gym": (300.0, 90.0),
        "cafe": (380.0, 300.0),
        "alley": (640.0, 420.0),
        "arena": (860.0, 150.0),
    }

    CITY_EDGES = (
        ("home", "gym"),
        ("home", "cafe"),
        ("gym", "cafe"),
        ("gym", "arena"),
        ("cafe", "alley"),
        ("cafe", "arena"),
        ("alley", "arena"),
    )

    # Timed activities looked up by finish_activity(id).
    # "sleep" is special-cased on LifeSim (jump to 08:00 next day).
    ACTIVITIES = {
        "alley": {
            "hours": ALLEY_HOURS,
            "label": "Alley scenario",
        },
        "train": {
            "hours": TRAIN_HOURS,
            "hunger_delta": -TRAIN_HUNGER,
            "label": "Gym training",
        },
        "eat": {
            "hours": EAT_HOURS,
            "hunger_delta": EAT_HUNGER,
            "cost": EAT_COST,
            "label": "Cafe meal",
        },
        "arena": {
            "hours": ARENA_HOURS,
            "label": "Arena bout",
        },
    }


    def path_pixel_length(points):
        """Sum hypot() between consecutive (x, y) points. Empty / single → 0."""
        if not points or len(points) < 2:
            return 0.0
        total = 0.0
        for i in range(1, len(points)):
            x1, y1 = points[i - 1][0], points[i - 1][1]
            x2, y2 = points[i][0], points[i][1]
            total += math.hypot(x2 - x1, y2 - y1)
        return total


    def travel_minutes_from_pixels(pixel_length):
        """
        minutes = max(15, round_to_15(pixel_length / PIXELS_PER_MINUTE))

        PIXELS_PER_MINUTE = PIXELS_PER_HOUR / 60 ≈ 13.3, so a ~800 px walk
        is about 1 hour. Rounded to 15-minute steps. Zero-length → 0.
        """
        if pixel_length is None or pixel_length <= 0:
            return 0
        raw = float(pixel_length) / PIXELS_PER_MINUTE
        stepped = ls_round_half_up(raw / TRAVEL_STEP_MINUTES) * TRAVEL_STEP_MINUTES
        return max(MIN_TRAVEL_MINUTES, int(stepped))


    def city_neighbors():
        graph = {name: [] for name in CITY_NODES}
        for a, b in CITY_EDGES:
            ax, ay = CITY_NODES[a]
            bx, by = CITY_NODES[b]
            dist = math.hypot(bx - ax, by - ay)
            graph[a].append((b, dist))
            graph[b].append((a, dist))
        return graph


    def shortest_path_nodes(start, dest):
        if start == dest:
            return [start]
        if start not in CITY_NODES or dest not in CITY_NODES:
            return [start]
        graph = city_neighbors()
        inf = float("inf")
        dist = {name: inf for name in CITY_NODES}
        prev = {name: None for name in CITY_NODES}
        dist[start] = 0.0
        remaining = set(CITY_NODES)
        while remaining:
            current = min(remaining, key=lambda n: dist[n])
            remaining.remove(current)
            if current == dest:
                break
            if dist[current] == inf:
                break
            for neighbor, weight in graph[current]:
                candidate = dist[current] + weight
                if candidate < dist[neighbor]:
                    dist[neighbor] = candidate
                    prev[neighbor] = current
        if dist[dest] == inf:
            return [start]
        nodes = [dest]
        cursor = dest
        while cursor != start:
            cursor = prev[cursor]
            if cursor is None:
                return [start]
            nodes.append(cursor)
        nodes.reverse()
        return nodes


    def shortest_path_points(start, dest):
        return [CITY_NODES[name] for name in shortest_path_nodes(start, dest)]
