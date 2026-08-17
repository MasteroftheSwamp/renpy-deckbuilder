default lock_plyr_cntrl = False ## DECIDES IF PLAYER CAN CLICK TO MAKE THE FOLLOWER MOVE
default dev_mode = False ## ALLOWS YOU TO SEE DEV STUFF
default edit_route_menu = False ## ALLOWS EDITING TOOLS FOR CREATING ROUTES
default poly_route_dev = False ## SHOWS GREATER DETAIL FOR THE ROUTE LINES
default debug_text_stuff = False ## ALLOWS YOU TO SEE SPECIAL TEXT FOR FOLLOWERS, CLOSEST POINT ON LINE

init python:
    import pygame
    import heapq  # For A* priority queue
    import math

    class InteractiveRouteDisplayable(renpy.Displayable):
        """
        A custom displayable to manage and edit lines:
        - Hover over lines/points to highlight them.
        - Click to select a line for editing.
        - Add/move points in edit mode.
        """

        def __init__(self, lines=None, width=2, **kwargs):
            super(InteractiveRouteDisplayable, self).__init__(**kwargs)
            self.lines = lines or []  # Initialize with no lines
            self.width = width  # Set the line width with a default of 2
            self.hovered_line = None  # The currently hovered line
            self.hovered_point = None  # The currently hovered point
            self.last_point = None  # The currently selected point (blue)
            self.selected_point = None  # The currently selected point (pink)
            self.editing_line = None  # The currently selected line for editing
            self.temp_point = None  # Temporary point added during line creation
            self.moving_point = None  # The currently dragged point
            self.moving_line = None # The Currently dragged line
            self.start_point = None # Starting point of the line
            self.start_selected_connected = False # See if the line is connected
            self.hovered_line_points = None  # Stores the two points of a hovered segment
            self.grid_mode = False # Holding shift enables this mode allowing player to lock line to a grid

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            canvas = render.canvas()
            disable_renpy_bind()

            if edit_route_menu:  # Edit mode enabled
                # Get connected lines for the hovered line (for when editing_line is None) and editing line
                hovered_connected_lines = self._get_connected_lines(self.hovered_line) if self.hovered_line else []
                connected_lines = self._get_connected_lines(self.editing_line) if self.editing_line else []

                for line in self.lines:
                    # Determine base line color
                    if self.editing_line and line in connected_lines:
                        line_color = "#00FF00"  # Green for connected lines in edit mode
                    elif not self.editing_line and line in hovered_connected_lines:
                        line_color = "#FFFF00"  # Yellow for all connected lines when hovered and no editing_line
                    else:
                        # Red for unconnected lines, 75% transparent when editing_line is selected
                        line_color = "#FF0000BF" if self.editing_line else "#FF0000"  # 75% transparent red when editing, opaque otherwise

                    # Unpack hovered_line_points for segment hover effect
                    if self.hovered_line_points:
                        hovered_start, hovered_end = self.hovered_line_points
                    else:
                        hovered_start, hovered_end = None, None

                    points = [(p[0], p[1]) for p in line.get('points', [])]
                    line_width = getattr(self, 'width', 2)

                    # Draw the line segments
                    for i in range(len(points) - 1):
                        segment_color = line_color  # Default to base color

                        # When editing_line exists, allow non-connected lines to have individual segment hover
                        if self.editing_line and line not in connected_lines:
                            orig_points = line.get('points', [])
                            if (orig_points[i] == hovered_start and orig_points[i + 1] == hovered_end):
                                if self.selected_point is not None:
                                    segment_color = "#FFFF00"  # Opaque yellow for hovered segment in non-connected lines when selected_point exists
                                else:
                                    segment_color = "#FF0000BF"  # Transparent red when selected_point is None
                        # Original behavior for hovered segment in editing_line
                        elif self.editing_line and line in connected_lines and self.hovered_line_points:
                            orig_points = line.get('points', [])
                            if (orig_points[i] == hovered_start and orig_points[i + 1] == hovered_end):
                                segment_color = "#FFFF00"  # Yellow for hovered segment in connected lines

                        canvas.line(segment_color, points[i], points[i + 1], width=line_width)

                    # Draw the points
                    for i, orig_point in enumerate(line.get('points', [])):
                        point = points[i]
                        # Default point color, 75% transparent for non-connected lines when editing_line is selected
                        true_color = "#FF0000BF" if self.editing_line and line not in connected_lines else "#FF0000"

                        # Determine point color
                        if len(points) == 1:
                            true_color = "#FF0000BF" if self.editing_line and line not in connected_lines else "#FF0000"  # Single points follow line transparency
                        elif orig_point == self.start_point:
                            true_color = "#FF0000" if orig_point != self.hovered_point else "#FFFF00"
                        elif orig_point == self.last_point:
                            true_color = "#FF0000" if orig_point != self.hovered_point else "#FFFF00"
                        elif orig_point == self.hovered_point:
                            # Handle hovering for points
                            if self.editing_line and line in connected_lines:
                                true_color = "#FFFF00"  # Yellow for hovered points in connected lines when editing_line is selected
                            elif self.editing_line and line not in connected_lines:
                                if self.selected_point is not None:
                                    true_color = "#FFFF00"  # Yellow for hovered points in non-connected lines when selected_point exists
                                else:
                                    true_color = "#FF0000BF"  # Transparent red when selected_point is None
                            elif not self.editing_line:
                                true_color = "#FFFF00"  # Yellow for hovered points when no editing_line
                            else:
                                true_color = "#FF0000"  # Red otherwise
                        elif self.editing_line and line in connected_lines:
                            true_color = "#FF0000"  # Red for points in connected lines in edit mode when not hovered
                        # else clause removed since default handles non-editing case

                        canvas.circle(true_color, point, 10)

                        # Overlay pink if it’s the selected point
                        if orig_point == self.selected_point:
                            if orig_point == self.hovered_point:
                                canvas.circle("#FFFF00", point, 10)  # Yellow when selected and hovered
                            else:
                                canvas.circle("#FF00FF", point, 10)  # Pink when selected but not hovered

                # Draw the temporary point
                if self.temp_point:
                    temp_x, temp_y = self.temp_point[0], self.temp_point[1]
                    canvas.circle("#FF0000", (temp_x, temp_y), 10)

                # Guideline from selected_point
                if (self.temp_point or (self.lines and len(self.lines) > 0 and self.lines[0]['points'])) and self.selected_point:
                    mouse_x, mouse_y = renpy.get_mouse_pos()
                    selected_x, selected_y = self.selected_point[0], self.selected_point[1]
                    if self.grid_mode:
                        mouse_x, mouse_y = self._get_snapped_mouse_pos(mouse_x, mouse_y, selected_x, selected_y)
                    canvas.line("#FFFFFF80", (selected_x, selected_y), (mouse_x, mouse_y), width=1)

                # Grid mode alignment lines
                if self.grid_mode:
                    mouse_x, mouse_y = renpy.get_mouse_pos()
                    threshold = 10
                    aligned_x, aligned_y = None, None
                    for line in self.lines:
                        for point in line['points']:
                            point_x, point_y = point[0], point[1]
                            if abs(point_x - mouse_x) <= threshold:
                                aligned_x = point_x
                            if abs(point_y - mouse_y) <= threshold:
                                aligned_y = point_y
                    if aligned_x is not None:
                        canvas.line("#FF00FF80", (aligned_x, 0), (aligned_x, height), width=1)
                    if aligned_y is not None:
                        canvas.line("#FF00FF80", (0, aligned_y), (width, aligned_y), width=1)

            else:  # Edit mode disabled
                if dev_mode:
                    for line in self.lines:
                        points = [(p[0], p[1]) for p in line.get('points', [])]
                        line_color = "#FFFFFF50"
                        line_width = getattr(self, 'width', 2)
                        for i in range(len(points) - 1):
                            canvas.line(line_color, points[i], points[i + 1], width=line_width)

            if poly_route_dev:
                for line in self.lines:
                    for orig_point in line.get('points', []):
                        x, y = orig_point[0], orig_point[1]
                        text = Text(f"({round(orig_point[0])}, {round(orig_point[1])})", size=14, color="#FFFFFF", outlines=[(0, "#000", 0, 0)])
                        tr = renpy.render(text, width, height, st, at)
                        render.blit(tr, (x - tr.width // 2, y - 20))

                if edit_route_menu:
                    mouse_pos = renpy.get_mouse_pos()
                    connected_polygons = [line['points'] for line in self.lines if line.get('connected', False)]
                    if connected_polygons:
                        outer_polygon = [tuple(p) for p in connected_polygons[0]]
                        holes = [[tuple(p) for p in hole] for hole in connected_polygons[1:]]
                        start = (follower.follower.x, follower.follower.y)  # Fixed typo from target_y to y for start
                        dest = (follower.follower.target_x, follower.follower.target_y)
                        nodes = {tuple(start), tuple(dest)}
                        for i, point in enumerate(outer_polygon):
                            if self._is_concave_vertex(outer_polygon, i):
                                nodes.add(tuple(point))
                        for hole in holes:
                            for point in hole:
                                nodes.add(tuple(point))
                        for node in nodes:
                            x, y = node[0], node[1]
                            canvas.circle("#FFFF00", (x, y), 8)

            renpy.redraw(self, 0)
            return render

        def event(self, ev, x, y, st):
            if not edit_route_menu:  # If edit mode is disabled, do nothing
                return None

            if ev.type == pygame.MOUSEMOTION:
                if self.editing_line:
                    # Get all connected lines
                    connected_lines = self._get_connected_lines(self.editing_line)
                    all_points = []
                    for line in self.lines:  # Check all lines, not just connected ones
                        all_points.extend(line['points'])
                    # Check for hovered point first
                    self.hovered_point = self._detect_hover_point(x, y, all_points)
                    # Only check for hovered line segment if no point is hovered
                    if not self.hovered_point:
                        self.hovered_line_points = self._detect_hover_line_segment(x, y)
                    else:
                        self.hovered_line_points = None
                else:
                    self.hovered_line, self.hovered_point = self._detect_hover(x, y)
                    if self.hovered_point:
                        self.hovered_line_points = None
                    else:
                        self.hovered_line_points = self._detect_hover_line_segment(x, y)

                if self.moving_point:
                    self._start_moving_point(self.moving_point, x, y)
                if self.moving_line:
                    self._start_moving_line_segment(self.moving_line, x, y)


            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:  # Left mouse button
                    if self.editing_line:
                        # Get all connected lines
                        connected_lines = self._get_connected_lines(self.editing_line)
                        all_points = set()
                        for line in connected_lines:
                            all_points.update(tuple(p) for p in line['points'])  # Convert each point to tuple
                        # Start moving a hovered point in edit mode or select/unselect it
                        if self.hovered_point and tuple(self.hovered_point) in all_points:
                            if self.hovered_point == self.selected_point:
                                # Unselect the point if it’s already selected
                                self.selected_point = None
                                self.moving_point = None  # Also stop moving it
                            else:
                                # Select and start moving the point if it’s not already selected
                                self.moving_point = self.hovered_point
                                self.selected_point = self.hovered_point  # Set hovered point as pink selected_point
                        elif self.hovered_line_points and tuple(self.hovered_line_points[0]) in all_points and tuple(self.hovered_line_points[1]) in all_points:
                            self.moving_line = self.hovered_line_points  # Activate line segment movement
                            self.line_drag_start = (x, y)  # Store drag start position
                    else:
                        # Select a line for editing and set up the connected group
                        if self.hovered_line:
                            self.editing_line = self.hovered_line
                            connected_lines = self._get_connected_lines(self.editing_line)
                            all_points = set()
                            for line in connected_lines:
                                all_points.update(tuple(p) for p in line['points'])  # Convert each point to tuple
                            if all_points:
                                # Convert tuples back to mutable lists for start_point and last_point
                                points_list = [list(p) for p in all_points]
                                self.start_point = points_list[0]  # First point in connected set
                                # Check if any line in the connected set forms a closed loop
                                is_polygon = any(line['points'][0] == line['points'][-1] for line in connected_lines if len(line['points']) > 2)
                                if is_polygon:
                                    self.start_selected_connected = True
                                    # Use second-to-last if enough points, else last
                                    self.last_point = points_list[-2] if len(points_list) > 2 else points_list[-1]
                                else:
                                    self.start_selected_connected = False  # Reset if not a polygon
                                    self.last_point = points_list[-1]  # Last point in connected set
                            else:
                                # Fallback if no points in connected lines (unlikely but safe)
                                self.start_point = self.editing_line['points'][0] if self.editing_line['points'] else None
                                self.last_point = self.editing_line['points'][-1] if self.editing_line['points'] else None
                                self.start_selected_connected = (self.start_point == self.last_point) and len(self.editing_line['points']) > 2

                elif ev.button == 3:  # Right mouse button
                    modifiers = pygame.key.get_mods()

                    # Handle inserting a new point on a hovered line segment
                    if self.hovered_line_points:  # If hovering over a line segment
                        point1, point2 = self.hovered_line_points
                        # Determine new point position based on Shift/grid mode
                        if modifiers & pygame.KMOD_LSHIFT:  # Shift held (grid mode)
                            # Place the new point exactly in the middle
                            mid_x = (point1[0] + point2[0]) / 2
                            mid_y = (point1[1] + point2[1]) / 2
                            new_point = [mid_x, mid_y]
                        else:  # Shift not held
                            # Place the new point at the mouse's hover position
                            closest_x, closest_y = self._closest_point_on_line(x, y, point1[0], point1[1], point2[0], point2[1])
                            new_point = [closest_x, closest_y]
                        # Insert the new point into the line, ensuring point1 and point2 are consecutive
                        for line in self.lines:
                            points = line['points']
                            if point1 in points and point2 in points:
                                index = points.index(point1)
                                if index + 1 < len(points) and points[index + 1] == point2:
                                    # Check if the line is connected and if selected_point exists
                                    if self.editing_line:
                                        connected_lines = self._get_connected_lines(self.editing_line)
                                        line_in_connected = line in connected_lines
                                        if not line_in_connected and self.selected_point is None:
                                            break  # Skip non-connected lines if no selected_point
                                    points.insert(index + 1, new_point)
                                    # If a point is selected, connect it to the new point
                                    if self.selected_point and self.selected_point != new_point:
                                        # Check if selected_point is from a connected line
                                        if self.editing_line:
                                            connected_lines = self._get_connected_lines(self.editing_line)
                                            selected_in_connected = any(self.selected_point in l['points'] for l in connected_lines)
                                            line_in_connected = line in connected_lines
                                            if selected_in_connected and not line_in_connected:
                                                # Connect selected_point from connected group to new_point in non-connected line
                                                editing_points = self.editing_line['points']
                                                is_endpoint = self.selected_point in (editing_points[0], editing_points[-1])
                                                if is_endpoint and self.selected_point in editing_points:
                                                    # Extend the current editing line
                                                    if self.selected_point == editing_points[0]:
                                                        editing_points.insert(0, new_point)
                                                    else:
                                                        editing_points.append(new_point)
                                                else:
                                                    # Create a new branch from selected_point to new_point
                                                    new_branch = {'points': [self.selected_point, new_point], 'color': "#FF0000", 'editing': False, 'connected': False}
                                                    self.lines.append(new_branch)
                                                    self.editing_line = new_branch
                                            elif line_in_connected:
                                                # Original behavior for connected lines
                                                editing_points = self.editing_line['points']
                                                is_endpoint = self.selected_point in (editing_points[0], editing_points[-1])
                                                if is_endpoint and self.selected_point in editing_points:
                                                    # Extend the current editing line
                                                    if self.selected_point == editing_points[0]:
                                                        editing_points.insert(0, new_point)
                                                    else:
                                                        editing_points.append(new_point)
                                                else:
                                                    # Create a new branch from selected_point to new_point
                                                    new_branch = {'points': [self.selected_point, new_point], 'color': "#FF0000", 'editing': False, 'connected': False}
                                                    self.lines.append(new_branch)
                                                    self.editing_line = new_branch  # Switch to editing the new branch
                                        # Update selected_point and last_point to the new point
                                        self.selected_point = new_point
                                        self.last_point = new_point
                                    # If no point is selected, just set the new point as selected (only for connected lines)
                                    elif not self.selected_point:
                                        if self.editing_line:
                                            connected_lines = self._get_connected_lines(self.editing_line)
                                            if line in connected_lines:
                                                self.selected_point = new_point
                                                self.last_point = new_point
                                        else:
                                            self.selected_point = new_point
                                            self.last_point = new_point
                                    break

                    # Remaining logic for Shift and other right-click behaviors
                    else:
                        if modifiers & pygame.KMOD_LSHIFT:
                            self.grid_mode = True

                        # Check for hovered point to connect
                        all_points = []
                        for line in self.lines:
                            all_points.extend(line['points'])
                        hovered_point = self._detect_hover_point(x, y, all_points)

                        if hovered_point and self.selected_point and hovered_point != self.selected_point:
                            # Connect selected_point to hovered_point
                            already_connected = False
                            for line in self.lines:
                                points = line['points']
                                for i in range(len(points) - 1):
                                    if (points[i] == self.selected_point and points[i + 1] == hovered_point) or \
                                       (points[i] == hovered_point and points[i + 1] == self.selected_point):
                                        already_connected = True
                                        break
                                if already_connected:
                                    break
                            if not already_connected:
                                new_branch = {'points': [self.selected_point, hovered_point], 'color': "#FF0000", 'editing': False, 'connected': False}
                                self.lines.append(new_branch)
                                self.editing_line = new_branch
                                self.last_point = hovered_point
                                self.selected_point = hovered_point
                                self.start_point = hovered_point
                        elif not self.editing_line:
                            if not self.temp_point:
                                self.temp_point = [x, y]
                                self.selected_point = self.temp_point
                                self.start_point = self.temp_point
                            else:
                                if self.grid_mode and self.selected_point:
                                    mouse_x, mouse_y = renpy.get_mouse_pos()
                                    selected_x, selected_y = self.selected_point[0], self.selected_point[1]
                                    snapped_x, snapped_y = self._get_snapped_mouse_pos(mouse_x, mouse_y, selected_x, selected_y)
                                    new_point = [snapped_x, snapped_y]
                                else:
                                    new_point = [x, y]
                                new_line = {'points': [self.selected_point, new_point], 'color': "#FF0000", 'editing': False, 'connected': False}
                                self.lines.append(new_line)
                                self.editing_line = new_line
                                self.last_point = new_point
                                self.selected_point = new_point
                                self.temp_point = None
                        else:
                            connected_lines = self._get_connected_lines(self.editing_line)
                            all_connected_points = []
                            for line in connected_lines:
                                all_connected_points.extend(line['points'])

                            hovered_connected_point = self._detect_hover_point(x, y, all_connected_points)

                            hovered_separate_point = None
                            for line in self.lines:
                                if line not in connected_lines:
                                    hovered = self._detect_hover_point(x, y, line['points'])
                                    if hovered:
                                        hovered_separate_point = hovered
                                        break

                            # Check if hovering over any point or segment in self.lines
                            any_hovered_point = hovered_point
                            hovered_segment = self._detect_hover_line_segment(x, y)

                            if hovered_connected_point and hovered_connected_point == self.start_point and len(self.editing_line['points']) > 1:
                                self.editing_line['points'].append(self.start_point)
                                self.start_selected_connected = True
                                self.editing_line['connected'] = True
                            elif hovered_separate_point and hovered_separate_point != self.selected_point and self.selected_point is not None:
                                new_branch = {'points': [self.selected_point, hovered_separate_point], 'color': "#FF0000", 'editing': False, 'connected': False}
                                self.lines.append(new_branch)
                                self.editing_line = new_branch
                                self.last_point = hovered_separate_point
                                self.selected_point = hovered_separate_point
                                self.start_point = self.selected_point
                            elif hovered_segment and not any_hovered_point and self.selected_point:
                                # Insert a new point on the hovered segment and connect it to the selected point
                                point1, point2 = hovered_segment
                                closest_x, closest_y = self._closest_point_on_line(x, y, point1[0], point1[1], point2[0], point2[1])
                                new_point = [closest_x, closest_y]
                                for line in self.lines:
                                    if point1 in line['points'] and point2 in line['points']:
                                        points = line['points']
                                        index = points.index(point1)
                                        if index + 1 < len(points) and points[index + 1] == point2:
                                            points.insert(index + 1, new_point)
                                            # Connect the selected_point to the new_point
                                            if self.selected_point != new_point:
                                                # Check if selected_point is an endpoint of the editing line
                                                editing_points = self.editing_line['points']
                                                is_endpoint = self.selected_point == editing_points[0] or self.selected_point == editing_points[-1]
                                                if is_endpoint:
                                                    # Extend the current line
                                                    if self.selected_point == editing_points[0]:
                                                        editing_points.insert(0, new_point)
                                                    else:
                                                        editing_points.append(new_point)
                                                else:
                                                    # Create a new branch
                                                    new_branch = {'points': [self.selected_point, new_point], 'color': "#FF0000", 'editing': False, 'connected': False}
                                                    self.lines.append(new_branch)
                                                    self.editing_line = new_branch
                                            self.selected_point = new_point
                                            self.last_point = new_point
                                            break
                            elif not any_hovered_point and self.selected_point:
                                if self.grid_mode:
                                    mouse_x, mouse_y = renpy.get_mouse_pos()
                                    selected_x, selected_y = self.selected_point[0], self.selected_point[1]
                                    snapped_x, snapped_y = self._get_snapped_mouse_pos(mouse_x, mouse_y, selected_x, selected_y)
                                    new_point = [snapped_x, snapped_y]
                                else:
                                    new_point = [x, y]
                                points = self.editing_line['points']
                                is_endpoint = self.selected_point == points[0] or self.selected_point == points[-1]
                                if is_endpoint:
                                    if self.selected_point in points:
                                        index = points.index(self.selected_point)
                                        if index == 0:
                                            points.insert(0, new_point)
                                        else:
                                            points.append(new_point)
                                        self.last_point = new_point
                                        self.selected_point = new_point
                                else:
                                    new_branch = {'points': [self.selected_point, new_point], 'color': "#FF0000", 'editing': False, 'connected': False}
                                    self.lines.append(new_branch)
                                    self.editing_line = new_branch
                                    self.last_point = new_point
                                    self.selected_point = new_point
                                    self.start_point = self.selected_point

            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    # Stop moving the point
                    self.moving_line = None
                    self.moving_point = None

            elif ev.type == pygame.KEYUP:
                if ev.key == pygame.K_LSHIFT:  # Reset grid_mode when Shift is released
                    self.grid_mode = False

            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LSHIFT:  # Reset grid_mode when Shift is released
                    self.grid_mode = True

                elif ev.key == pygame.K_RETURN:  # Enter key to exit edit mode
                    self.editing_line = None
                    self.last_point = None
                    self.start_point = None
                    self.hovered_line = None
                    self.hovered_point = None
                    self.temp_point = None
                    self.moving_point = None
                    self.start_selected_connected = False
                    self.hovered_line_points = None
                    self.moving_line = None
                    self.selected_point = None
                    # Handle orphan points (already redundant with temp_point = None above, but kept for clarity):
                    if self.temp_point and not any(self.temp_point in line['points'] for line in self.lines):
                        self.temp_point = None
                    # Remove incomplete or single-point lines:
                    self.lines = [line for line in self.lines if len(line['points']) > 1]

                elif ev.key == pygame.K_DELETE:  # DELETE key pressed
                    if self.editing_line:  # Only proceed if an editing line is selected
                        connected_lines = self._get_connected_lines(self.editing_line)
                        if self.hovered_point:  # If a point is hovered
                            line = self._get_line_containing_point(self.hovered_point)
                            if line and line in connected_lines:  # Only delete if the line is connected
                                points = line['points']
                                if self.hovered_point in points:
                                    index = points.index(self.hovered_point)
                                    is_endpoint = index == 0 or index == len(points) - 1
                                    was_polygon = line['connected'] and len(points) > 2 and points[0] == points[-1]

                                    if not is_endpoint and len(points) > 2:  # Split the line if not an endpoint
                                        # Create two new lines
                                        first_segment = points[:index]  # Up to but not including the deleted point
                                        second_segment = points[index + 1:]  # After the deleted point
                                        self.lines.remove(line)  # Remove the original line

                                        # Add new lines with connected = False
                                        if first_segment:  # Only add if there are points
                                            new_line1 = {'points': first_segment, 'color': "#FF0000", 'editing': False, 'connected': False}
                                            self.lines.append(new_line1)
                                        if second_segment:  # Only add if there are points
                                            new_line2 = {'points': second_segment, 'color': "#FF0000", 'editing': False, 'connected': False}
                                            self.lines.append(new_line2)

                                        # Update editing_line to one of the new segments (if it was the deleted line)
                                        if line == self.editing_line:
                                            self.editing_line = new_line1 if first_segment else new_line2 if second_segment else None

                                        # Update start_point, last_point, and selected_point
                                        if self.hovered_point == self.start_point:
                                            self.start_point = first_segment[0] if first_segment else None
                                        if self.hovered_point == self.last_point or self.hovered_point == self.selected_point:
                                            self.last_point = second_segment[-1] if second_segment else first_segment[-1] if first_segment else None
                                            self.selected_point = self.last_point
                                    else:  # Endpoint deletion
                                        points.remove(self.hovered_point)  # Remove the point
                                        if points:
                                            # Update pointers
                                            if self.hovered_point == self.start_point:
                                                self.start_point = points[0]
                                            if self.hovered_point == self.last_point or self.hovered_point == self.selected_point:
                                                self.last_point = points[-1]
                                                self.selected_point = self.last_point
                                            # If it was a polygon, it’s no longer connected
                                            if was_polygon:
                                                line['connected'] = False
                                        else:
                                            # Remove the line if no points remain
                                            self.lines.remove(line)
                                            if line == self.editing_line:
                                                self.editing_line = None
                                                self.start_point = None
                                                self.last_point = None
                                                self.selected_point = None

                                    # Reset selected_point to None after deletion to avoid bugs
                                    self.selected_point = None

            return None
        ##=====================================================================#
        ## DEV CREATION TOOLS ##################################################
        ##=====================================================================#
        def _get_connected_lines(self, root_line):
            """Returns a list of all lines connected to the root_line through shared points."""
            if root_line is None:
                return []  # Return empty list if root_line is None
            connected_lines = [root_line]
            points_to_check = set(tuple(p) for p in root_line['points'])  # Points as tuples for hashing

            while points_to_check:
                current_point = points_to_check.pop()
                for line in self.lines:
                    if line not in connected_lines:
                        line_points = set(tuple(p) for p in line['points'])
                        if current_point in line_points:
                            connected_lines.append(line)
                            points_to_check.update(line_points - {current_point})

            return connected_lines

        def _get_snapped_mouse_pos(self, mouse_x, mouse_y, start_x, start_y):
            """Returns mouse position snapped to 90-degree angles or aligned with points when grid_mode is True."""
            import math
            dx = mouse_x - start_x
            dy = mouse_y - start_y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance == 0:
                return mouse_x, mouse_y  # Avoid division by zero

            # Check for pink line alignment first when grid_mode is active
            if self.grid_mode:
                threshold = 10
                aligned_x, aligned_y = None, None
                for line in self.lines:
                    for point in line['points']:
                        point_x, point_y = point[0], point[1]
                        if abs(point_x - mouse_x) <= threshold:  # Vertical alignment
                            aligned_x = point_x
                        if abs(point_y - mouse_y) <= threshold:  # Horizontal alignment
                            aligned_y = point_y
                # Snap to intersection if both alignments exist
                if aligned_x is not None and aligned_y is not None:
                    return aligned_x, aligned_y
                # Snap to single alignment if only one exists
                elif aligned_x is not None:
                    return aligned_x, mouse_y
                elif aligned_y is not None:
                    return mouse_x, aligned_y

            # Fallback to 90-degree snapping if no alignment
            angle = math.degrees(math.atan2(dy, dx))
            snapped_angle = round(angle / 45) * 45  # Snap to nearest 90 degrees
            snapped_rad = math.radians(snapped_angle)
            snapped_x = start_x + distance * math.cos(snapped_rad)
            snapped_y = start_y + distance * math.sin(snapped_rad)
            return snapped_x, snapped_y

        def _detect_hover_line_segment(self, x, y):
            """Detects if the follower is hovering over a line segment (between two points), only if no point is hovered."""
            if self.hovered_point:  # If a point is already hovered, don’t hover a line segment
                return None
            x = x
            y = y
            for line in self.lines:
                for i in range(len(line['points']) - 1):
                    ax, ay = line['points'][i]
                    bx, by = line['points'][i + 1]
                    closest_x, closest_y = self._closest_point_on_line(x, y, ax, ay, bx, by)
                    distance = ((x - closest_x) ** 2 + (y - closest_y) ** 2) ** 0.5
                    if distance <= 5:  # Hover threshold
                        return (line['points'][i], line['points'][i + 1])  # Return the two points forming the segment
            return None

        def _start_moving_line_segment(self, points, x, y):
            """Move both points of a hovered line segment and update all identical points across all lines, without collapsing."""
            dx = x - self.line_drag_start[0]
            dy = y - self.line_drag_start[1]

            # Identify all instances of point1 and point2 across all lines
            point1, point2 = points
            affected_points1 = []
            affected_points2 = []
            for line in self.lines:
                for p in line['points']:
                    if p == point1:
                        affected_points1.append(p)
                    elif p == point2:
                        affected_points2.append(p)

            # Check for overlap with other distinct points
            min_distance = 20  # Minimum distance to prevent collapse
            new_x1, new_y1 = point1[0] + dx, point1[1] + dy
            new_x2, new_y2 = point2[0] + dx, point2[1] + dy
            for line in self.lines:
                for other_point in line['points']:
                    if other_point not in affected_points1 and other_point not in affected_points2:
                        dist1 = ((other_point[0] - new_x1) ** 2 + (other_point[1] - new_y1) ** 2) ** 0.5
                        dist2 = ((other_point[0] - new_x2) ** 2 + (other_point[1] - new_y2) ** 2) ** 0.5
                        if dist1 < min_distance or dist2 < min_distance:
                            return  # Don’t move if too close to another distinct point

            # Move all instances of point1
            old_x1, old_y1 = point1[0], point1[1]
            for p in affected_points1:
                p[0] = old_x1 + dx
                p[1] = old_y1 + dy

            # Move all instances of point2
            old_x2, old_y2 = point2[0], point2[1]
            for p in affected_points2:
                p[0] = old_x2 + dx
                p[1] = old_y2 + dy

            # Sync start/end points for any connected lines
            for line in self.lines:
                if line.get('connected', False) and len(line['points']) > 2:
                    line_points = line['points']
                    if point1 == line_points[0] or point2 == line_points[0]:  # Start point moved
                        line_points[-1][0] = line_points[0][0]  # Sync end to start
                        line_points[-1][1] = line_points[0][1]
                    elif point1 == line_points[-1] or point2 == line_points[-1]:  # End point moved
                        line_points[0][0] = line_points[-1][0]  # Sync start to end
                        line_points[0][1] = line_points[-1][1]

            self.line_drag_start = (x, y)

        def is_point_in_polygon(point, polygon):
            x, y = point
            x = x
            y = y
            inside = False
            n = len(polygon)

            for i in range(n):
                x1, y1 = polygon[i]
                x2, y2 = polygon[(i + 1) % n]

                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                    inside = not inside

            return inside

        def _is_point_inside_polygon(self, point, polygon):
            """
            Uses the Ray-Casting Algorithm to determine if a point is inside a polygon.

            Args:
                point (tuple): The (x, y) coordinates of the mouse.
                polygon (list): A list of (x, y) tuples forming a closed shape.

            Returns:
                bool: True if the point is inside the polygon, False otherwise.
            """
            x, y = point
            x = x
            y = y
            inside = False
            n = len(polygon)

            if n < 3:  # Not a valid polygon
                return False

            x0, y0 = polygon[0]
            for i in range(n + 1):
                x1, y1 = polygon[i % n]  # Loop back to the first point
                if ((y0 > y) != (y1 > y)) and (x < (x1 - x0) * (y - y0) / (y1 - y0) + x0):
                    inside = not inside
                x0, y0 = x1, y1

            return inside

        def _get_line_containing_point(self, point):
            for line in self.lines:
                if point in line['points']:
                    return line
            return None

        def _detect_hover(self, x, y):
            x = x
            y = y
            """Detect if the follower is hovering over a line or a point, prioritizing points."""
            hovered_line = None
            hovered_point = None

            # First, check for points across all lines
            for line in self.lines:
                for point in line['points']:
                    if abs(point[0] - x) <= 10 and abs(point[1] - y) <= 10:
                        hovered_point = point
                        hovered_line = line
                        break
                if hovered_point:  # If a point is found, stop checking
                    break

            # Only check for line hover if no point is hovered
            if hovered_point is None:
                for line in self.lines:
                    for i in range(len(line['points']) - 1):
                        ax, ay = line['points'][i]
                        bx, by = line['points'][i + 1]
                        closest_x, closest_y = self._closest_point_on_line(x, y, ax, ay, bx, by)
                        distance = ((x - closest_x) ** 2 + (y - closest_y) ** 2) ** 0.5
                        if distance <= 5:  # Hover threshold
                            hovered_line = line
                            break

            return hovered_line, hovered_point

        def _detect_hover_point(self, x, y, points):
            x = x
            y = y
            """Detect if the follower is hovering over a point in the given points list."""
            for point in points:
                if abs(point[0] - x) <= 10 and abs(point[1] - y) <= 10:
                    return point
            return None

        def _closest_point_on_line(self, px, py, ax, ay, bx, by):
            """Find the closest point to (px, py) on the line segment (ax, ay) -> (bx, by)."""
            apx, apy = px - ax, py - ay
            abx, aby = bx - ax, by - ay
            ab_len = (abx**2 + aby**2)**0.5

            if ab_len == 0:
                return ax, ay  # Zero-length segment

            abx_norm, aby_norm = abx / ab_len, aby / ab_len
            proj_length = max(0, min(apx * abx_norm + apy * aby_norm, ab_len))
            closest_x = ax + abx_norm * proj_length
            closest_y = ay + aby_norm * proj_length
            return closest_x, closest_y


        def _add_point_to_line(self, line, point):
            """Add a new point to a line."""
            if len(line['points']) < 2:
                return
            line['points'].append(point)

        def _start_moving_point(self, point, x, y):
            """Move a hovered point and update all identical points across all lines, syncing start/end if connected, without collapsing."""
            # Find all instances of this exact point across all lines
            affected_points = []
            for line in self.lines:
                for p in line['points']:
                    if p == point:  # Check if it's the same point object (identity match)
                        affected_points.append(p)

            # Check for overlap with other distinct points in all lines
            min_distance = 20  # Minimum distance to prevent collapse
            for line in self.lines:
                for other_point in line['points']:
                    if other_point not in affected_points:
                        dist = ((other_point[0] - x) ** 2 + (other_point[1] - y) ** 2) ** 0.5
                        if dist < min_distance:
                            return  # Don’t move if too close to another distinct point

            # Update all affected points’ coordinates
            old_x, old_y = point[0], point[1]
            for p in affected_points:
                p[0] = x
                p[1] = y

            # Sync start/end points for connected lines (e.g., polygons)
            for line in self.lines:
                if line.get('connected', False) and len(line['points']) > 2:
                    points = line['points']
                    if point == points[0]:  # Dragging the start point
                        points[-1][0] = x  # Sync the end point
                        points[-1][1] = y
                    elif point == points[-1]:  # Dragging the end point
                        points[0][0] = x  # Sync the start point
                        points[0][1] = y
        ##=====================================================================#
        ## DEV CREATION TOOLS ##################################################
        ##=====================================================================#

################################################################################
## ROUTE TOOLS ##
################################################################################

    import os
    import copy

    def save_route(route):
        global selected_route
        # Check if there are no points to save
        if not route.lines or all(not line["points"] for line in route.lines):
            renpy.notify("No points to save.")
            return

        # Check if currently in edit mode
        if getattr(route, "editing_line", None) is not None:
            renpy.notify("End Edit Mode - Press Enter.")
            return

        # Define the folder and file naming pattern
        folder_path = os.path.join(renpy.config.basedir, "game", "RF", "saved route")
        os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

        # Determine the next available file name
        file_number = 1
        route_id = "route"
        while True:
            file_name = f"{route_id}_route_{file_number:03}.txt"
            file_path = os.path.join(folder_path, file_name)
            if not os.path.exists(file_path):
                break
            file_number += 1

        # Generate variable name based on route_id
        var_name = f"{route_id}_route"

        # Collect all lines with their points
        all_lines = [
            {
                "points": line["points"],
                "color": line["color"],
                "editing": line["editing"],
                "connected": line["connected"]
            }
            for line in route.lines
        ]

        # Write the lines to the file with default variable declaration
        with open(file_path, "w") as file:
            file.write(f"default {var_name} = [\n")
            for i, line in enumerate(all_lines):
                # Convert the line dictionary to a string with proper formatting
                points_str = "[" + ", ".join(f"[{x}, {y}]" for x, y in line["points"]) + "]"
                line_str = f"    {{'points': {points_str}, 'color': '{line['color']}', 'editing': {str(line['editing']).capitalize()}, 'connected': {str(line['connected']).capitalize()}}}"
                if i < len(all_lines) - 1:
                    line_str += ","  # Add comma for all but the last line
                file.write(f"{line_str}\n")
            file.write("]")

        # Notify the user that the route was saved
        renpy.notify("Route Saved! - saved route")

    def save_interact_points(follower_displayable):
        """
        Saves all interact points of the follower into a file in the 'RF/saved points' folder,
        using the exact name 'follower' to match the default variable.

        Args:
            follower_displayable (FollowerDisplayable): The displayable object containing the follower with interact points.
        """
        follower = follower_displayable.follower
        if not follower.interact_points:
            renpy.notify("No interact points to save.")
            return

        # Define the folder and file naming pattern
        folder_path = os.path.join(renpy.config.basedir, "game", "RF", "saved points")
        os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn’t exist

        # Use the exact name "follower" to match 'default follower'
        follower_name = "follower"
        file_number = 1
        while True:
            file_name = f"{follower_name}_interact_points_{file_number:03}.txt"
            file_path = os.path.join(folder_path, file_name)
            if not os.path.exists(file_path):
                break
            file_number += 1

        # Variable name for the file
        var_name = follower_name  # This will be "follower"

        # Write the interact points to the file
        with open(file_path, "w") as file:
            file.write(f"default {var_name}interact_points = [\n")
            for i, point_data in enumerate(follower.interact_points):
                point_str = f"({point_data['point'][0]}, {point_data['point'][1]})"
                active_str = str(point_data.get('active', True)).capitalize()  # Default to True if 'active' missing
                detected_str = str(point_data.get('detected', False)).capitalize()  # Default to False if 'detected' missing
                line_str = f"    {{'name': '{point_data['name']}', 'point': {point_str}, 'label': '{point_data['label']}', 'active': {active_str}, 'detected': {detected_str}}}"
                if i < len(follower.interact_points) - 1:
                    line_str += ","  # Add comma for all but the last point
                file.write(f"{line_str}\n")
            file.write("]")

        renpy.notify(f"Interact points saved! - Check RF/saved points")

    def clear_current_route(route):
        route.lines = []
        route.editing_line = None
        route.selected_point = None
        route.temp_point = None

        route.hovered_line = None
        route.hovered_point = None
        route.selected_point = None
        route.last_point = None
        route.editing_line = None
        route.temp_point = None
        route.moving_point = None
        route.start_point = None
        route.start_selected_connected = False
        route.hovered_line_points = None
        route.moving_line = None
        renpy.notify("route Cleared!")

    def clear_interact_points(f):
        """Clears all interaction points."""
        f.interact_point_counter = 0
        f.interact_points = []

    def toggle_edit_mode(route):
        global edit_route_menu

        if edit_route_menu:
            # Exit edit mode
            edit_route_menu = False
            # Clear the editing line and selected point
            route.editing_line = None
            route.selected_point = None
            route.temp_point = None

            if route.editing_line:
                route.editing_line = None  # Exit edit mode
                route.selected_point = None  # Clear the selected point
                route.start_point = None  # Clear the selected point

                route.hovered_line = None
                route.hovered_point = None
                route.selected_point = None
                route.last_point = None
                route.editing_line = None
                route.temp_point = None
                route.moving_point = None
                route.start_point = None
                route.hovered_line_points = None
                route.moving_line = None
                route.start_selected_connected = False

            # Handle orphan points:
            if route.temp_point and not any(route.temp_point in line['points'] for line in route.lines):
                route.temp_point = None  # Remove the single temp point if no line exists

            # Remove incomplete or single-point lines:
            route.lines = [line for line in route.lines if len(line['points']) > 1]

            renpy.notify("Edit mode disabled. Exiting edit mode.")
        else:
            # Enable edit mode
            edit_route_menu = True
            renpy.notify("Edit mode enabled.")

    def toggle_poly_route_mode():
        global poly_route_dev

        if poly_route_dev:
            poly_route_dev = False
        else:
            poly_route_dev = True

################################################################################
################################################################################
