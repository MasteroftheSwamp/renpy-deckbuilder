## ROUTE CONTROLLER ##
init python:
################################################################################
## ROUTE LINES ##
################################################################################

    class RouteLines(renpy.Displayable): 

        def __init__(self, lines=None, width=2, **kwargs):
            super(RouteLines, self).__init__(**kwargs)
            self.lines = lines or []  # Initialize with no lines
            self.width = width  # Set the line width with a default of 2

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            canvas = render.canvas()

            if dev_mode:
                for line in self.lines:
                    points = [(p[0], p[1]) for p in line.get('points', [])]  # Offset points
                    line_color = "#E6FF00" #"#FFFFFF"  # All lines white
                    line_width = getattr(self, 'width', 2)
                    for i in range(len(points) - 1):
                        canvas.line("#000000", points[i], points[i + 1], width=line_width+10)
                        canvas.line(line_color, points[i], points[i + 1], width=line_width)

            renpy.redraw(self, 0)  # Redraw every frame
            return render

        def event(self, ev, x, y, st):
            return None
