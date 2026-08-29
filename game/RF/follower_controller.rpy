## FOLLOWER CODE ##
init python:
    import pygame
    import heapq  # For A* priority queue
    import math

    class Follower:
        def __init__(self, x=0, y=0, turn=True, free_movement=True, directional_mode="4", speed=200, route=None, img_id=None):
            self.rect = pygame.Rect(x, y, 25, 25) ## Square that represents follower position
            self.old_rect = self.rect.copy() ## Square that represents follower position
            self.x = x ## Follower X Position
            self.y = y ## Follower Y Position
            self.speed = speed ## Follower SPeed
            self.width = 25 ## Width of square
            self.target_x = x ## Hovered X Position
            self.target_y = y ## Hovered Y Position

            self.path = []  ## Set Path for follower to follow
            self.saved_path = []  ## Set Path for follower to follow

            self.destination = None ## End destination
            self.saved_destination = None ## End destination

            self.route_points = []  ## Keep this for rendering in FollowerDisplayable
            self.saved_route_points = []  ## Keep this for rendering in FollowerDisplayable

            self.route = route ## The line it follows
            self.graph = {}  # Graph restricted to polygon edges
            self.last_position = (x, y) ## Last position followed
            self.path_active = False ## Sees if a path is currently active

            self.img_id = img_id ## Image ID
            self.dir = "down" ## folower direction
            self.act = "stand" ## follower action
            self.state = "stand_d" ## follower state
            self.moving = False ## sees if follower is currently moving
            self.state_changed = False ## sees if followers state has currently changed
            self.just_clicked = False ## sees if follower has just clicked on a point
            self.child = None ## the follower image

            self.angle = 0 ## Follower angle // only works with self.directional_mode == "free"

            self.turn = turn ## Only for horizontal turn, (If you want entity to be auto flipped)
            self.directional_mode = directional_mode ## "1" This is for 1 image direction or state does not change it, "4" This is for 4 directional angled images, "8" This is for 8 directional angled images, "free" Makes image rotate when moving along

            self.free_movement = free_movement ## (If True then follower will be able to move in any closest point near mouse when clicked - Else place_point function must be used to move follower)

            ## ** WANRING ** I added an auto label active as False if lock_plyr_cntrl == False, so that the label is constantly jumped to when player reaches its destination ## To view how to alter this go to the dev_start_info read me
            self.label_active = False ## used with set_button_destination function // if False when follower reaches destination, label will not be jumped to //  If True self.label_jump will be jumped to // NOT the same as self.interact_points, this is purely destination basded, aka where the player clicked
            self.label_jump = "start" ## used with set_button_destination function // the label that the follower will jump to
            self.label_button_clicked = False ## used with set_button_destination function // If imagebutton is clicked this is set true

            self.interact_points = []  ## Points on the route that will jump label
            self.cur_interact_point = None ## Currently activated interact point
            self.interact_point_counter = 0  ## To auto-increment point names`

            self.set_follower()

        ########################################################################
        ## FUNCTIONS ON REACHING DESTINATION
        ########################################################################
        ## BUTTON INTERACT POINTS ##
        def set_reach(self,labl): ## used with set_button_destination function // CHANGES THE REACH ACTION
            """ CHANGES THE LABEL WHEN THE PLAYER REACHES THE DESTINATION """
            self.label_jump = labl

        def reach_action(self): ## used with set_button_destination function // THE ACTIONS THAT PLAY WHEN DESTINATION IS REACHED
            renpy.jump(self.label_jump)

        ## INTERACT POINTS ##
        def jump_interact_point(self):
            """ JUMPS TO THE LABEL WHEN INTERACT POINT IS TOUCHED BY THE FOLLOWER """
            if self.cur_interact_point:
                renpy.jump(self.cur_interact_point["label"])

        def togg_interact_point(self,name,togg):
            """ TOGGLES IF SPECIFIC INTERACT POINT IS ACTIVE """
            for i in self.interact_points:
                if i['name'] == name:
                    i['active'] = togg

        def set_interact_point(self,name,labl):
            """ CHANGES INTERACT POINT LABEL """
            for i in self.interact_points:
                if i['name'] == name:
                    i['label'] = labl

        def remove_interact_point(self,name):
            """ REMOVES INTERACT POINT IN THE INTERACT POINT LIST """
            for i in self.interact_points:
                if i['name'] == name:
                    self.interact_points.remove(self)

        def load_interact_points(self,int_pts):
            """ LOADS PRE DEFINED INTERACT POINT LIST """
            self.interact_points = int_pts

        ########################################################################
        ########################################################################
        def reset_follower(self):
            """ RESET FOLLOWER IMAGE// USED WHEN SWAPPING IMG IDS """
            if self.directional_mode == "1" or self.directional_mode == "free":
                self.state = "idle"
                self.child = Transform((self.img_id)[self.state]['image'], xzoom=1.0)
            elif self.directional_mode == "4":
                self.child = Transform((self.img_id)[self.state]['image'], xzoom=1.0)
            elif self.directional_mode == "8":
                self.child = Transform((self.img_id)[self.state]['image'], xzoom=1.0)

        def change_follower_dir(self,dir=None):
            """ SETS FOLLOWER DIRECTION THEN SETS THE IMAGE """
            if dir != None:
                self.dir = dir
                self.set_follower()

        def change_follower_act(self,act=None):
            """ SETS FOLLOWER ACTION // GET THE IMAGE STATES FROM THE IMAGE LIBRARY """
            if act != None:
                self.state = act
                self.child = Transform((self.img_id)[self.state]['image'], xzoom=1.0)

        def set_follower(self):
            """ SETS FOLLOWER IMAGE TO THE DIRECTION THE PLAYER IS FACING OR THE STATE /ACTION THEY ARE DOING """
            if self.directional_mode == "1" or self.directional_mode == "free":
                self.state = "idle"
                self.child = Transform((self.img_id)[self.state]['image'], xzoom=1.0)

            elif self.directional_mode == "4":
                # Construct the new state based on current dir and act
                if self.dir == 'left':
                    if self.turn:
                        new_state = "stand_h" if self.act == "stand" else "walk_h"
                        xzoom = -1.0
                    else:
                        new_state = "stand_hl" if self.act == "stand" else "walk_hl"
                        xzoom = 1.0
                elif self.dir == 'right':
                    if self.turn:
                        new_state = "stand_h" if self.act == "stand" else "walk_h"
                        xzoom = 1.0
                    else:
                        new_state = "stand_hr" if self.act == "stand" else "walk_hr"
                        xzoom = 1.0
                elif self.dir == 'up':
                    new_state = "stand_u" if self.act == "stand" else "walk_u"
                    xzoom = 1.0
                elif self.dir == 'down':
                    new_state = "stand_d" if self.act == "stand" else "walk_d"
                    xzoom = 1.0
                else:
                    return  # Invalid direction, no update

                # Update state and image if state has changed or we force it
                if self.state != new_state or self.state_changed:
                    self.state = new_state
                    self.child = Transform((self.img_id)[self.state]['image'], xzoom=xzoom)
                    self.state_changed = False  # Reset after update

            elif self.directional_mode == "8":
                # Construct the new state based on current dir and act
                if self.dir == 'left':
                    if self.turn:
                        new_state = "stand_h" if self.act == "stand" else "walk_h"
                        xzoom = -1.0
                    else:
                        new_state = "stand_hl" if self.act == "stand" else "walk_hl"
                        xzoom = 1.0
                elif self.dir == 'up-left':
                    if self.turn:
                        new_state = "stand_uh" if self.act == "stand" else "walk_uh"
                        xzoom = -1.0
                    else:
                        new_state = "stand_uhl" if self.act == "stand" else "walk_uhl"
                        xzoom = 1.0
                elif self.dir == 'down-left':
                    if self.turn:
                        new_state = "stand_dh" if self.act == "stand" else "walk_dh"
                        xzoom = -1.0
                    else:
                        new_state = "stand_dhl" if self.act == "stand" else "walk_dhl"
                        xzoom = 1.0
                elif self.dir == 'right':
                    if self.turn:
                        new_state = "stand_h" if self.act == "stand" else "walk_h"
                        xzoom = 1.0
                    else:
                        new_state = "stand_hr" if self.act == "stand" else "walk_hr"
                        xzoom = 1.0
                elif self.dir == 'up-right':
                    if self.turn:
                        new_state = "stand_uh" if self.act == "stand" else "walk_uh"
                        xzoom = 1.0
                    else:
                        new_state = "stand_uhr" if self.act == "stand" else "walk_uhr"
                        xzoom = 1.0
                elif self.dir == 'down-right':
                    if self.turn:
                        new_state = "stand_dh" if self.act == "stand" else "walk_dh"
                        xzoom = 1.0
                    else:
                        new_state = "stand_dhr" if self.act == "stand" else "walk_dhr"
                        xzoom = 1.0
                elif self.dir == 'up':
                    new_state = "stand_u" if self.act == "stand" else "walk_u"
                    xzoom = 1.0
                elif self.dir == 'down':
                    new_state = "stand_d" if self.act == "stand" else "walk_d"
                    xzoom = 1.0
                else:
                    return  # Invalid direction, no update

                # Update state and image if state has changed or we force it
                if self.state != new_state or self.state_changed:
                    self.state = new_state
                    self.child = Transform((self.img_id)[self.state]['image'], xzoom=xzoom)
                    self.state_changed = False  # Reset after update

        def detect_movement(self):
            """ DETECTS IF THE FOLLOWER IS MOVING """
            if self.directional_mode == "1" or self.directional_mode == "free":
                self.set_follower()
                current_pos = (self.x, self.y)
                if current_pos != self.last_position:
                    self.moving = True
                else:
                    if self.path_active == False:
                        self.moving = False
                    else:
                        self.moving = True
                # Update last_position for next frame
                self.last_position = (self.x, self.y)
            else:
                # Check if position changed since last frame
                current_pos = (self.x, self.y)
                if current_pos != self.last_position:
                    self.moving = True
                else:
                    if self.path_active == False:
                        self.moving = False
                    else:
                        self.moving = True
                # Update last_position for next frame
                self.last_position = (self.x, self.y)

                # Update action state
                new_act = "walk" if self.moving else "stand"
                if self.act != new_act:
                    self.act = new_act
                    self.state_changed = True  # Flag state change when action changes

                # Call set_follower to update image if state_changed is True
                if self.state_changed:
                    self.set_follower()

        def detect_direction(self):
            """ DETECTS MOVEMENT DIRECTION """
            if not self.path or len(self.path) < 1:
                return  # No path, no direction update

            # Only skip if just_clicked and no significant movement yet
            if self.just_clicked and (self.x, self.y) == self.last_position:
                return  # Prevents initial flicker right after click

            next_point = self.path[0]
            dx = next_point[0] - self.x
            dy = next_point[1] - self.y
            abs_dx = abs(dx)
            abs_dy = abs(dy)

            if self.directional_mode == "4":
                # Removed dist > 5 threshold to allow smaller movements to update direction
                new_dir = self.dir
                if abs_dx > abs_dy:  # Horizontal movement dominates
                    new_dir = "right" if dx > 0 else "left"
                else:  # Vertical movement dominates
                    new_dir = "down" if dy > 0 else "up"

                if self.dir != new_dir:
                    self.dir = new_dir
                    self.state_changed = True
            elif self.directional_mode == "8":
                # Calculate the angle of movement in radians
                if dx == 0 and dy == 0:
                    return  # No movement, no direction change
                angle = math.atan2(dy, dx)  # atan2 returns angle in radians (-pi to pi)
                angle_deg = math.degrees(angle)  # Convert to degrees (-180 to 180)

                # Normalize angle to 0-360 range for easier comparison
                if angle_deg < 0:
                    angle_deg += 360

                # Define 8-directional ranges (each ~45 degrees)
                # 0° = right, 90° = down, 180° = left, 270° = up
                new_dir = self.dir
                if 22.5 <= angle_deg < 67.5:
                    new_dir = "down-right"
                elif 67.5 <= angle_deg < 112.5:
                    new_dir = "down"
                elif 112.5 <= angle_deg < 157.5:
                    new_dir = "down-left"
                elif 157.5 <= angle_deg < 202.5:
                    new_dir = "left"
                elif 202.5 <= angle_deg < 247.5:
                    new_dir = "up-left"
                elif 247.5 <= angle_deg < 292.5:
                    new_dir = "up"
                elif 292.5 <= angle_deg < 337.5:
                    new_dir = "up-right"
                else:  # 337.5 <= angle_deg < 22.5
                    new_dir = "right"

                if self.dir != new_dir:
                    self.dir = new_dir
                    self.state_changed = True

        def detect_movement_angle(self):
            """ CALCULATE THE ANGLE THE FOLLOWER IS MOVING // USED IN self.directional_mode = 'free' """
            if not self.path or len(self.path) < 1:
                return None  # No movement or path to calculate angle from

            # Get the next point in the path
            next_point = self.path[0]
            dx = next_point[0] - self.x  # Change in x
            dy = next_point[1] - self.y  # Change in y

            # If there’s no movement, keep the current angle
            if dx == 0 and dy == 0:
                return self.angle

            # Calculate angle in radians using atan2 (handles all quadrants correctly)
            angle_rad = math.atan2(dy, dx)
            # Convert to degrees (0° = right, 90° = down, 180° = left, 270° = up)
            angle_deg = math.degrees(angle_rad)

            # Normalize to 0-360 range (optional, depending on your needs)
            if angle_deg < 0:
                angle_deg += 360

            return angle_deg

        def stop_follower(self):
            """ STOPS FOLLOWER IN THEIR TRACKS """
            # Clear path and destination
            self.path = []  # Clear the current path
            self.route_points = []  # Clear the route points for rendering
            self.destination = None  # Remove the destination
            self.path_active = False  # Indicate no active path

            self.saved_path = []  # Clear the current path
            self.saved_route_points = []  # Clear the route points for rendering
            self.saved_destination = None  # Remove the destination

            # Reset movement state
            self.moving = False  # Stop movement flag
            self.act = "stand"  # Set action to standing
            self.state_changed = True  # Flag state change to update image
            self.just_clicked = False  # Reset click debounce flag

            # Reset interaction-related attributes
            self.cur_interact_point = None  # Clear current interaction point

            # Update the follower’s image to reflect standing state
            self.set_follower()  # Update the image based on current direction

        def pause_follower(self):
            """ PAUSES FOLLOWER ON STANDBY TO CONTINUE """
            # Save current path and destination
            self.saved_path = self.path[:]  # Copy the current path
            self.saved_route_points = self.route_points[:]  # Copy the route points for rendering
            self.saved_destination = self.destination  # Save the destination

            # Clear active path and destination
            self.path = []  # Clear the current path
            self.route_points = []  # Clear the route points for rendering
            self.destination = None  # Remove the destination
            self.path_active = False  # Indicate no active path

            # Reset movement state
            self.moving = False  # Stop movement flag
            self.act = "stand"  # Set action to standing
            self.state_changed = True  # Flag state change to update image
            self.just_clicked = False  # Reset click debounce flag

            # Reset interaction-related attributes
            self.cur_interact_point = None  # Clear current interaction point

            # Update the follower’s image to reflect standing state
            self.set_follower()  # Update the image based on current direction

        def play_follower(self):
            """ RESUMES THE FOLLOWERS PATH IT WAS HEADED """
            # Restore saved path and destination
            if not self.saved_path or not self.saved_destination:
                if dev_mode:
                    renpy.notify("No saved path to resume!")
                return

            self.path = self.saved_path[:]  # Restore the saved path
            self.route_points = self.saved_route_points[:]  # Restore the route points for rendering
            self.destination = self.saved_destination  # Restore the destination

            # Clear saved variables
            self.saved_path = []  # Clear the saved path
            self.saved_route_points = []  # Clear the saved route points
            self.saved_destination = None  # Clear the saved destination

            # Resume movement
            self.path_active = True  # Indicate an active path
            self.just_clicked = True  # Set to debounce initial direction change
            self.moving = True  # Start movement flag (will be adjusted by detect_movement)
            self.act = "walk"  # Set action to walking (assumes movement starts)
            self.state_changed = True  # Flag state change to update image

            # Reset interaction-related attributes
            self.cur_interact_point = None  # Clear current interaction point

            # Update the follower’s image to reflect movement state
            self.set_follower()  # Update the image based on current direction

        def _closest_point_on_line(self, px, py, ax, ay, bx, by):
            """ DECIDES WHATS THE CLOSEST POINT ON THE LINE THATS CLOSE TO THE MOUSE """
            apx, apy = px - ax, py - ay
            abx, aby = bx - ax, by - ay
            ab_len = (abx**2 + aby**2)**0.5
            if ab_len == 0:
                return ax, ay
            abx_norm, aby_norm = abx / ab_len, aby / ab_len
            proj_length = max(0, min(apx * abx_norm + apy * aby_norm, ab_len))
            return ax + abx_norm * proj_length, ay + aby_norm * proj_length

        def snap_to_nearest_segment(self, x, y, lines):
            """ SNAP A POINT TO THE NEAREST POINT ON ANY LINE SEGMENT """
            min_dist = float('inf')
            best_point = (x, y)
            for line in lines:
                points = line['points']
                if len(points) < 2:
                    continue
                n = len(points) if line.get('connected', False) else len(points) - 1
                for i in range(n):
                    ax, ay = points[i]
                    bx, by = points[(i + 1) % len(points)] if line.get('connected', False) and i == n - 1 else points[i + 1]
                    cx, cy = self._closest_point_on_line(x, y, ax, ay, bx, by)
                    dist = math.hypot(cx - x, cy - y)
                    if dist < min_dist:
                        min_dist = dist
                        best_point = (cx, cy)
            return best_point

        def update_target_position(self, mouse_pos, lines):
            """ UPDATES THE POSITION OF THE TARGETED POSITION ON THE LINE """
            mx, my = mouse_pos
            connected_polygons = [line['points'] for line in lines]
            if not connected_polygons:
                self.target_x, self.target_y = mx, my
                return
            # Snap to nearest segment across all lines
            snapped_pos = self.snap_to_nearest_segment(mx, my, lines)
            self.target_x, self.target_y = snapped_pos

        def set_teleport(self, x, y, lines):
            """ TELEPORT THE FOLLOWER TO THE CLOSEST POINT ON THE LINES // type in the x and y coordinates to place player on the line"""
            self.x = x
            self.y = y
            snapped_start = self.snap_to_nearest_segment(self.x, self.y, lines)
            self.x, self.y = snapped_start
            self.destination = None
            self.path_active = False
            self.just_clicked = False
            self.path = []

        def set_destination(self, dest_x, dest_y, lines):
            """SETS PATH/DESTINATION TO POINT// target point that the follower will follow """
            # Clear saved variables
            self.saved_path = []  # Clear the saved path
            self.saved_route_points = []  # Clear the saved route points
            self.saved_destination = None  # Clear the saved destination

            self.label_button_clicked = False
            self.last_position = (self.x, self.y)
            self.update_target_position((dest_x, dest_y), lines)
            self.destination = (self.target_x, self.target_y)

            # Check if there are any valid lines to follow
            connected_polygons = [line['points'] for line in lines]
            if not connected_polygons:
                if dev_mode:
                    renpy.notify("Follower Error: No Line Found")
                self.path = []  # Clear path to prevent movement
                self.route_points = []  # Clear route points
                self.path_active = False  # Disable movement
                self.destination = None  # Reset destination
                return

            # Snap start position to nearest segment
            snapped_start = self.snap_to_nearest_segment(self.x, self.y, lines)
            self.x, self.y = snapped_start  # Snap follower to nearest segment

            # Calculate path across all segments
            self.route_points = self.calculate_path(snapped_start[0], snapped_start[1], self.target_x, self.target_y, lines)
            if not self.route_points or len(self.route_points) < 2:  # Check if path is invalid
                if dev_mode:
                    renpy.notify("Follower Error: No Valid Path Found")
                self.path = []  # Clear path to prevent movement
                self.route_points = []  # Clear route points
                self.path_active = False  # Disable movement
                self.destination = None  # Reset destination
                return

            self.path = self.route_points[:]  # Copy for movement
            self.path_active = True
            self.just_clicked = True  # Set flag to debounce direction

        def set_button_destination(self, dest_x, dest_y, lines):
            """SETS PATH/DESTINATION TO POINT THROUGH A BUTTON// target point that the follower will follow """
            # Clear saved variables
            self.saved_path = []  # Clear the saved path
            self.saved_route_points = []  # Clear the saved route points
            self.saved_destination = None  # Clear the saved destination

            self.label_button_clicked = True
            self.last_position = (self.x, self.y)
            self.update_target_position((dest_x, dest_y), lines)
            self.destination = (self.target_x, self.target_y)

            # Check if there are any valid lines to follow
            connected_polygons = [line['points'] for line in lines]
            if not connected_polygons:
                if dev_mode:
                    renpy.notify("Follower Error: No Line Found")
                self.path = []  # Clear path to prevent movement
                self.route_points = []  # Clear route points
                self.path_active = False  # Disable movement
                self.destination = None  # Reset destination
                return

            # Snap start position to nearest segment
            snapped_start = self.snap_to_nearest_segment(self.x, self.y, lines)
            self.x, self.y = snapped_start  # Snap follower to nearest segment

            # Calculate path across all segments
            self.route_points = self.calculate_path(snapped_start[0], snapped_start[1], self.target_x, self.target_y, lines)
            if not self.route_points or len(self.route_points) < 2:  # Check if path is invalid
                if dev_mode:
                    renpy.notify("Follower Error: No Valid Path Found")
                self.path = []  # Clear path to prevent movement
                self.route_points = []  # Clear route points
                self.path_active = False  # Disable movement
                self.destination = None  # Reset destination
                return

            self.path = self.route_points[:]  # Copy for movement
            self.path_active = True
            self.just_clicked = True  # Set flag to debounce direction

        def build_graph(self, lines, start, dest):
            """Build a graph where all points in lines are nodes, connected only along their line segments."""
            graph = {}
            # Process each line segment
            for line in lines:
                points = line['points']
                if len(points) < 2:  # Skip lines with fewer than 2 points
                    continue
                # Add all points as nodes, connecting to adjacent points in this line
                for i in range(len(points)):
                    current = tuple(points[i])  # Use tuple for hashable node
                    if current not in graph:
                        graph[current] = []
                    # Connect to previous point (if it exists)
                    if i > 0:
                        prev = tuple(points[i - 1])
                        dist = math.hypot(current[0] - prev[0], current[1] - prev[1])
                        if (prev, dist) not in graph[current]:
                            graph[current].append((prev, dist))
                        if prev not in graph:
                            graph[prev] = []
                        if (current, dist) not in graph[prev]:  # Bidirectional
                            graph[prev].append((current, dist))
                    # Connect to next point (if it exists and not last in non-connected, or wrap for connected)
                    if i < len(points) - 1:
                        next_node = tuple(points[i + 1])
                        dist = math.hypot(next_node[0] - current[0], next_node[1] - current[1])
                        if (next_node, dist) not in graph[current]:
                            graph[current].append((next_node, dist))
                        if next_node not in graph:
                            graph[next_node] = []
                        if (current, dist) not in graph[next_node]:  # Bidirectional
                            graph[next_node].append((current, dist))
                    # For connected (closed) lines, connect last to first
                    if line.get('connected', False) and i == len(points) - 1 and len(points) > 2:
                        first = tuple(points[0])
                        dist = math.hypot(current[0] - first[0], current[1] - first[1])
                        if (first, dist) not in graph[current]:
                            graph[current].append((first, dist))
                        if first not in graph:
                            graph[first] = []
                        if (current, dist) not in graph[first]:
                            graph[first].append((current, dist))

            # Add start and dest to the graph, connecting to nearest edge endpoints
            start = tuple(start)
            dest = tuple(dest)
            start_edge = None
            dest_edge = None

            # Find edges for start and dest across all lines
            for line_idx, line in enumerate(lines):
                points = line['points']
                if len(points) < 2:
                    continue
                n = len(points) if line.get('connected', False) else len(points) - 1
                for i in range(n):
                    ax, ay = points[i]
                    bx, by = points[(i + 1) % len(points)] if line.get('connected', False) and i == n - 1 else points[i + 1]
                    cx_s, cy_s = self._closest_point_on_line(start[0], start[1], ax, ay, bx, by)
                    cx_d, cy_d = self._closest_point_on_line(dest[0], dest[1], ax, ay, bx, by)
                    dist_s = math.hypot(cx_s - start[0], cy_s - start[1])
                    dist_d = math.hypot(cx_d - dest[0], cy_d - dest[1])
                    if dist_s < 1e-5:  # Start is on this segment
                        start_edge = (line_idx, i)
                    if dist_d < 1e-5:  # Dest is on this segment
                        dest_edge = (line_idx, i)

            # If start and dest are on the same edge, connect them directly
            if start_edge and dest_edge and start_edge == dest_edge:
                if start not in graph:
                    graph[start] = []
                if dest not in graph:
                    graph[dest] = []
                dist = math.hypot(dest[0] - start[0], dest[1] - start[1])
                graph[start].append((dest, dist))
                graph[dest].append((start, dist))
            else:
                # Connect start to edge endpoints
                if start not in graph:
                    graph[start] = []
                    if start_edge:
                        line_idx, edge_idx = start_edge
                        points = lines[line_idx]['points']
                        ax, ay = points[edge_idx]
                        bx, by = points[(edge_idx + 1) % len(points)] if lines[line_idx].get('connected', False) and edge_idx == len(points) - 2 else points[edge_idx + 1]
                        dist_a = math.hypot(ax - start[0], ay - start[1])
                        dist_b = math.hypot(bx - start[0], by - start[1])
                        graph[start].append((tuple([ax, ay]), dist_a))
                        graph[start].append((tuple([bx, by]), dist_b))
                        if tuple([ax, ay]) not in graph:
                            graph[tuple([ax, ay])] = []
                        if tuple([bx, by]) not in graph:
                            graph[tuple([bx, by])] = []
                        graph[tuple([ax, ay])].append((start, dist_a))
                        graph[tuple([bx, by])].append((start, dist_b))

                # Connect dest to edge endpoints
                if dest not in graph and dest != start:
                    graph[dest] = []
                    if dest_edge:
                        line_idx, edge_idx = dest_edge
                        points = lines[line_idx]['points']
                        ax, ay = points[edge_idx]
                        bx, by = points[(edge_idx + 1) % len(points)] if lines[line_idx].get('connected', False) and edge_idx == len(points) - 2 else points[edge_idx + 1]
                        dist_a = math.hypot(ax - dest[0], ay - dest[1])
                        dist_b = math.hypot(bx - dest[0], by - dest[1])
                        graph[dest].append((tuple([ax, ay]), dist_a))
                        graph[dest].append((tuple([bx, by]), dist_b))
                        if tuple([ax, ay]) not in graph:
                            graph[tuple([ax, ay])] = []
                        if tuple([bx, by]) not in graph:
                            graph[tuple([bx, by])] = []
                        graph[tuple([ax, ay])].append((dest, dist_a))
                        graph[tuple([bx, by])].append((dest, dist_b))

            self.graph = graph  # Update instance graph
            return graph

        def calculate_path(self, start_x, start_y, dest_x, dest_y, lines):
            """ Calculates the path that the player will follow """
            if not lines:
                return [(dest_x, dest_y)]
            start = (start_x, start_y)
            dest = (dest_x, dest_y)
            self.graph = self.build_graph(lines, start, dest)
            return self.a_star(start, dest)

        def a_star(self, start, goal):
            """ A* Pathfinding function """
            start = tuple(start)
            goal = tuple(goal)
            if start not in self.graph or goal not in self.graph:
                return [(self.x, self.y)]
            frontier = [(0, start)]
            came_from = {start: None}
            cost_so_far = {start: 0}
            while frontier:
                _, current = heapq.heappop(frontier)
                if current == goal:
                    break
                for next_node, cost in self.graph.get(current, []):
                    new_cost = cost_so_far[current] + cost
                    if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                        cost_so_far[next_node] = new_cost
                        h_cost = math.hypot(goal[0] - next_node[0], goal[1] - next_node[1])
                        priority = new_cost + h_cost
                        heapq.heappush(frontier, (priority, next_node))
                        came_from[next_node] = current
            path = []
            current = goal
            while current is not None:
                path.append(current)
                current = came_from.get(current)
                if current == start:
                    path.append(start)
                    break
            return [(p[0], p[1]) for p in path[::-1]]

        ## INTERACT POINTS FUNCTIONS ##

        def detect_interact_point(self):
            """Detects if the follower has passed or touched an active interact point, regardless of direction."""
            if not self.interact_points or not self.path or not self.moving:
                return

            current_pos = (self.x, self.y)
            prev_pos = self.last_position
            move_dist = math.hypot(self.x - prev_pos[0], self.y - prev_pos[1])
            if move_dist == 0:
                return

            # Default 10 keeps rooftop tight. City pins set point["radius"]
            # or follower.interact_radius for a bigger trigger.
            for point_data in self.interact_points:
                if not point_data.get('active', True):  # Skip if not active
                    continue
                detection_radius = float(
                    point_data.get("radius")
                    or getattr(self, "interact_radius", None)
                    or 10
                )
                point_pos = point_data["point"]
                point_x, point_y = point_pos

                # Check distance from current position to point
                dist_to_point = math.hypot(self.x - point_x, self.y - point_y)
                is_touching = dist_to_point <= detection_radius or self._segment_circle_intersect(prev_pos, current_pos, point_pos, detection_radius)

                if is_touching:
                    if not point_data.get('detected', False):  # Only trigger if not already detected
                        point_data['detected'] = True  # Mark as detected
                        self.cur_interact_point = point_data
                        self.jump_interact_point()
                        break  # Exit after first detection
                    # If already detected and still touching, do nothing
                else:
                    # Reset detected flag only when not touching at all
                    point_data['detected'] = False

        def _segment_circle_intersect(self, p1, p2, center, radius):
            """Check if a line segment (p1 to p2) intersects a circle (center, radius)."""
            x1, y1 = p1
            x2, y2 = p2
            cx, cy = center

            # Vector from p1 to p2
            dx = x2 - x1
            dy = y2 - y1

            # Vector from p1 to circle center
            fx = cx - x1
            fy = cy - y1

            # Length of the segment squared
            seg_len_sq = dx * dx + dy * dy
            if seg_len_sq == 0:
                return math.hypot(fx, fy) <= radius  # p1 = p2, just check distance

            # Project circle center onto segment (t is the projection parameter, clamped to [0, 1])
            t = max(0, min(1, (fx * dx + fy * dy) / seg_len_sq))

            # Closest point on segment to circle center
            closest_x = x1 + t * dx
            closest_y = y1 + t * dy

            # Distance from closest point to circle center
            dist_to_center = math.hypot(closest_x - cx, closest_y - cy)

            return dist_to_center <= radius

        def find_segment_for_point(self, point):
            """Finds the line segment that an interact point lies on."""
            px, py = point
            for line in self.route.lines:
                points = line['points']
                n = len(points) if line.get('connected', False) else len(points) - 1
                for i in range(n):
                    ax, ay = points[i]
                    bx, by = points[(i + 1) % len(points)] if line.get('connected', False) and i == n - 1 else points[i + 1]
                    closest_x, closest_y = self._closest_point_on_line(px, py, ax, ay, bx, by)
                    dist = math.hypot(closest_x - px, closest_y - py)
                    if dist < 1e-5:  # Point is effectively on this segment
                        return ((ax, ay), (bx, by))
            return None

        def project_point_to_segment(self, point, segment):
            """Projects a point onto a line segment and returns the closest point."""
            px, py = point
            (ax, ay), (bx, by) = segment
            return self._closest_point_on_line(px, py, ax, ay, bx, by)

        def drop_interact_point(self, x, y):
            """Drops an interaction point at the nearest point on the line in dev mode."""
            if dev_mode:  # Only allow in dev mode
                # Snap the clicked position to the nearest point on the line
                snapped_pos = self.snap_to_nearest_segment(x, y, self.route.lines)
                snapped_x, snapped_y = snapped_pos
                self.interact_point_counter = len(self.interact_points)+1
                point_name = f"point_{self.interact_point_counter}"
                new_point = {"name": point_name, "point": (snapped_x, snapped_y), "label": "start", "active": True, "detected": False}
                self.interact_points.append(new_point)

        def rando_drop_interact_point(self):
            """Drops a random interaction point on a line segment in dev mode, prefers spacing but allows overlap if needed."""
            if not dev_mode:  # Only allow in dev mode
                return
            if not self.route.lines:
                renpy.notify("No lines available to drop a point on!")
                return

            import random

            min_spacing = 50
            max_attempts = 5

            for attempt in range(max_attempts):
                line = random.choice(self.route.lines)
                points = line['points']
                if len(points) < 2:
                    continue
                segment_start_idx = random.randint(0, len(points) - 2)
                x1, y1 = points[segment_start_idx]
                x2, y2 = points[segment_start_idx + 1]
                t = random.uniform(0, 1)
                snapped_x = x1 + t * (x2 - x1)
                snapped_y = y1 + t * (y2 - y1)
                new_point_pos = (snapped_x, snapped_y)

                too_close = False
                for existing_point in self.interact_points:
                    ex_x, ex_y = existing_point["point"]
                    distance = math.hypot(snapped_x - ex_x, snapped_y - ex_y)
                    if distance < min_spacing:
                        too_close = True
                        break

                if not too_close:
                    self.interact_point_counter = len(self.interact_points) + 1
                    point_name = f"point_{self.interact_point_counter}"
                    new_point = {"name": point_name, "point": new_point_pos, "label": "start", "active": True, "detected": False}  # Added 'active'
                    self.interact_points.append(new_point)
                    renpy.notify(f"Added {point_name} at ({snapped_x:.1f}, {snapped_y:.1f})")
                    return

            # Fallback placement
            line = random.choice(self.route.lines)
            points = line['points']
            if len(points) >= 2:
                segment_start_idx = random.randint(0, len(points) - 2)
                x1, y1 = points[segment_start_idx]
                x2, y2 = points[segment_start_idx + 1]
                t = random.uniform(0, 1)
                snapped_x = x1 + t * (x2 - x1)
                snapped_y = y1 + t * (y2 - y1)
                new_point_pos = (snapped_x, snapped_y)

                self.interact_point_counter = len(self.interact_points) + 1
                point_name = f"point_{self.interact_point_counter}"
                new_point = {"name": point_name, "point": new_point_pos, "label": "start", "active": True, "detected": False}  # Added 'active'
                self.interact_points.append(new_point)
                #renpy.notify(f"Added {point_name} at ({snapped_x:.1f}, {snapped_y:.1f}) - Placed closer due to limited space")

        ## INTERACT POINTS FUNCTIONS ##

        def update(self, dt, route):
            mouse_pos = renpy.get_mouse_pos()
            self.update_target_position(mouse_pos, self.route.lines)

            if self.path:
                next_point = self.path[0]
                dx = next_point[0] - self.x
                dy = next_point[1] - self.y
                dist = math.hypot(dx, dy)
                if dist < self.speed * dt:
                    self.x, self.y = next_point
                    self.path.pop(0)
                    if not self.path:
                        self.destination = None
                        self.path_active = False
                        self.moving = False
                        if self.label_active:
                            self.reach_action()
                else:
                    angle = math.atan2(dy, dx)
                    step = self.speed * dt
                    self.x += math.cos(angle) * step
                    self.y += math.sin(angle) * step
                    # Snap to nearest segment across all lines
                    connected_polygons = [line['points'] for line in route.lines]
                    if connected_polygons:
                        snapped_pos = self.snap_to_nearest_segment(self.x, self.y, route.lines)
                        self.x, self.y = snapped_pos  # Snap back to nearest edge

                if self.directional_mode == "free":
                    self.moving = True
                    new_angle = self.detect_movement_angle()
                    if new_angle is not None:
                        self.angle = new_angle

            self.detect_interact_point()  # Add this line
            self.rect.center = (round(self.x), round(self.y))
            self.detect_direction()
            self.detect_movement()

            if self.just_clicked and (self.x, self.y) != self.last_position:
                self.just_clicked = False

    class FollowerDisplayable(renpy.Displayable):
        def __init__(self, follower):
            super().__init__()
            super().__setattr__("follower", follower)
            super().__setattr__("old_st", None)

        def __getattr__(self, name):
            if name not in ("follower","old_st") and hasattr(self.follower, name):
                return getattr(self.follower, name)

        def __setattr__(self, name, value):
            if name in ("follower", "old_st") or not hasattr(self, "follower"):
                super().__setattr__(name, value)
            elif hasattr(self.follower, name):
                setattr(self.follower, name, value)
            else:
                super().__setattr__(name, value)

        def render(self, width, height, st, at):
            if dev_mode:
                disable_renpy_bind()
            if self.directional_mode == "free":
                # Apply rotation based on self.angle
                rotated_child = Transform(self.child, rotate=self.angle)
                cr = renpy.render(rotated_child, width, height, st, at)
            else:
                # No rotation for other modes
                cr = renpy.render(renpy.displayable(self.child), width, height, st, at)

            if self.label_button_clicked == False:
                self.label_active = False
            else:
                self.label_active = True

            cw, ch = cr.get_size()
            rv = renpy.Render(width, height)
            canvas = rv.canvas()

            if self.old_st is None:
                self.old_st = st
            dtime = st - self.old_st
            self.old_st = st

            self.update(dtime, self.route)

            collision_box = Solid("#FF0000")
            collision_box_render = renpy.render(collision_box, self.rect.width, self.rect.height, st, at)
            if dev_mode:
                rv.blit(collision_box_render, self.rect.topleft)

            follower_mid_x = self.rect.x + self.rect.width / 2
            follower_mid_y = self.rect.y + self.rect.height / 2
            follower_mid = (follower_mid_x, follower_mid_y)

            last_pos = (self.last_position[0], self.last_position[1])
            if dev_mode:
                canvas.circle("#800080", last_pos, 8)

            target_pos = (self.target_x, self.target_y)
            if dev_mode:
                canvas.circle("#FF0000", target_pos, 10)

            if self.directional_mode == "free":
                if dev_mode:
                    # Draw movement direction line based on self.angle
                    if self.path:  # Only draw if moving (has a path)
                        angle_rad = math.radians(self.angle)  # Convert angle to radians
                        line_length = 100  # Match your other project’s length
                        dir_x = math.cos(angle_rad)  # X component of direction
                        dir_y = math.sin(angle_rad)  # Y component of direction
                        start_pos = (follower_mid_x, follower_mid_y)  # Center of follower
                        end_pos = (start_pos[0] + dir_x * line_length, start_pos[1] + dir_y * line_length)  # Endpoint
                        if dev_mode:  # Show only in dev mode, like your other debug visuals
                            canvas.line("#00FFFF", start_pos, end_pos, width=2)  # Cyan line, width 2 for visibility

            if self.graph:
                for node1, edges in self.graph.items():
                    x1, y1 = node1[0], node1[1]
                    for node2, _ in edges:
                        x2, y2 = node2[0], node2[1]
                        is_route_edge = False
                        if self.follower.path_active and self.route_points:
                            for i in range(len(self.route_points) - 1):
                                if (self.route_points[i] == (x1, y1) and self.route_points[i + 1] == (x2, y2)) or \
                                   (self.route_points[i] == (x2, y2) and self.route_points[i + 1] == (x1, y1)):
                                    is_route_edge = True
                                    break
                        color = "#FF0000" if is_route_edge else "#0000FF"  # Red for route, blue for all edges
                        if poly_route_dev:
                            canvas.line(color, (x1, y1), (x2, y2), width=2 if is_route_edge else 1)

            if dev_mode:
                for point_data in self.interact_points:
                    point_pos = point_data["point"]
                    canvas.circle("#2A00FF", point_pos, 8)  # Orange circles for interact points
                    text_obj = Text(point_data["name"], size=12, color="#FFFFFF", outlines=[(2, "#000", 0, 0)])
                    text_render = renpy.render(text_obj, width, height, st, at)
                    rv.blit(text_render, (point_pos[0] - text_render.width // 2, point_pos[1] - 20))

            if self.destination:
                if dev_mode:
                    canvas.circle("#00FF00", self.destination, 10)

            if debug_text_stuff:
                debug_texts = [
                    f"x: {self.x}",
                    f"y: {self.y}",
                    f"dir: {self.dir}",
                    f"state: {self.state}",
                    f"act: {self.act}",
                    f"movement: {self.moving}",
                    f"target_x: {target_pos[0]}",
                    f"target_y: {target_pos[1]}",
                ]
                y_offset = 20
                for debug_text in debug_texts:
                    text_obj = Text(debug_text, size=14, color="#FFFFFF", outlines=[(2, "#000", 0, 0)])
                    text_render = renpy.render(text_obj, width, height, st, at)
                    rv.blit(text_render, (50, y_offset))
                    y_offset += 20

            # Positioning and rotation logic
            x_position = self.x - (cw // 2)
            y_position = self.y - (ch // 2) if self.directional_mode == "free" else self.y - ch

            if self.directional_mode == "free":
                rv.blit(cr, (x_position + self.img_id[self.state]['xoff'], y_position + self.img_id[self.state]['yoff']))
            else:
                # Non-free mode: use static positioning
                rv.blit(cr, (x_position + self.img_id[self.state]['xoff'], y_position + self.img_id[self.state]['yoff']))

            renpy.redraw(self, 0)
            return rv

        def event(self, ev, x, y, st):
            if (ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3 and
                pygame.key.get_mods() & pygame.KMOD_LCTRL and dev_mode):
                self.drop_interact_point(x, y)

            if lock_plyr_cntrl == False:
                if self.free_movement == True:
                    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                        self.set_destination(x, y, self.route.lines)
                renpy.redraw(self, 0)
                return
            else:
                return None
