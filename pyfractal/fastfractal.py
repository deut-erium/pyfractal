"""Module for drawing fractals fastly by operations on points directly"""
from math import cos, sin
from .curve import Curve


class FastFractal():
    """
    FastFractal class to generate a list of points denoting points of line
    fractals on the canvas
    """

    def __init__(
            self,
            parent,
            rules=None,
            start_point=(
                100,
                100),
            base_length=10):
        """
        Initialize the canvas
        parent is the parent class (GUI class) to hold functionalities
        """
        self.rules = rules if rules else []
        self.start_point = start_point
        self.base_length = base_length
        self.parent = parent
        self.recursion_depth = 1
        self.curve = Curve(self)

    def set_startpoint(self, point):
        """
        set the startpoint of curve to point
        """
        self.start_point = point

    def set_rules(self, rules):
        """
        Change the rules to a new set of rules
        """
        self.rules = rules

    def set_base_length(self, base_length):
        """
        Change base_length (length of the base fractal curve)
        to the new provided value
        """
        self.base_length = base_length

    def set_parent(self, parent):
        """
        Set the parent of the class to the provided parent
        """
        self.parent = parent

    def set_recursion_depth(self, recursion_depth):
        """
        Set the recursion depth of the class to provided recursion_depth
        """
        self.recursion_depth = recursion_depth

    def reflection(self, line, point):
        """
        find the reflection in line ax + by + c = 0 represented as (a,b,c)
        of point represented as (p,q)
        determined by the formula x = (p(a^2-b^2)-2b(aq+c))/(a^2 + b^2)
        y = -(q(a^2 - b^2)+ 2a(bp+c))/(a^2 + b^2)
        """
        a, b, c = line
        p, q = point
        a2_plus_b2 = a**2 + b**2  # a square plus b square
        a2_minus_b2 = a**2 - b**2  # a square minus b square
        x = (p * a2_minus_b2 - 2 * b * (a * q + c)) / a2_plus_b2
        y = -(q * a2_minus_b2 + 2 * a * (b * p + c)) / a2_plus_b2
        return x, y

    def flip(self, p1, p2, curve):
        """
        Flip the curve denoted by list of points (x,y) around the line
        formed by the line joining points p1 (x1,y1) and p2 (x2,y2)

        determine line in form ax + by + c = 0
        """
        x1, y1 = p1
        x2, y2 = p2
        a = x2 - x1
        b = y1 - y2
        c = x1 * y2 - x2 * y1
        line = (a, b, c)
        return [self.reflection(line, point) for point in curve]

    def rotate_scale(self, center, theta, scale, curve):
        """
        Rotate the curve (list of points (x,y)) by theta around the
        center (cx,cy) and scale the curve by a factor of scale

        x -> c_x + (x-c_x)*cos(theta)*scale - (y-c_y)*sin(theta)*scale
        y -> c_y + (x-c_x)*sin(theta)*scale + (y-c_y)*cos(theta)*scale
        for each (x,y) tuple in curve
        """
        c_x, c_y = center
        return [(c_x +
                 (i -
                  c_x) *
                 scale *
                 cos(theta) -
                 (j -
                  c_y) *
                 scale *
                 sin(theta), c_y +
                 (i -
                  c_x) *
                 scale *
                 sin(theta) +
                 (j -
                  c_y) *
                 scale *
                 cos(theta)) for i, j in curve]

    def translate(self, center, curve):
        """
        translate the curve to the provided center
        """
        offset_x = center[0] - curve[0][0]  # offset wrt first point of curve
        offset_y = center[1] - curve[0][1]
        return [(i + offset_x, j + offset_y) for i, j in curve]

    def reverse(self, p1, p2, curve):
        """
        Flip the curve around the perpendicular bisector of p1, p2
        """
        x1, y1 = p1
        x2, y2 = p2
        a = y2 - y1
        b = x2 - x1
        c = ((x1**2 + y1**2) - (x2**2 + y2**2)) / 2
        line = (a, b, c)
        return [self.reflection(line, point) for point in curve[::-1]]

    def form_base_curve(self, start_point=None):
        """
        Form the base curve from the initial rules and starting point

        """
        if start_point is None:
            start_point = self.start_point
        curve = [start_point]
        for theta, scale_fac, _, _ in self.rules:
            last_x, last_y = curve[-1]
            curve.append((
                last_x + self.base_length * scale_fac * cos(theta),
                last_y + self.base_length * scale_fac * sin(theta)))
        return curve

    def fractal_curve(self, recursion_depth=None):
        """
        Form a recursive curve from rules of recursion_depth
        """
        if not self.rules:
            return [self.start_point]
        if recursion_depth is None:
            recursion_depth = self.recursion_depth
        if recursion_depth == 1:
            return self.form_base_curve()
        curve_prev_level = self.fractal_curve(recursion_depth - 1)
        last_point = curve_prev_level[0]
        curve = []
        for theta, scale_fac, is_flipped, is_reversed in self.rules:
            if is_flipped is None and is_reversed is None:
                curve.append((
                    last_point[0] + self.base_length * cos(theta),
                    last_point[1] + self.base_length * sin(theta)))
                last_point = curve[-1]
                continue
            sub_crv = self.rotate_scale(
                last_point,
                theta,
                scale_fac,
                self.translate(last_point, curve_prev_level))
            if is_flipped:
                sub_crv = self.flip(sub_crv[0], sub_crv[-1], sub_crv)
                # flip the curve around the starting and end point
            if is_reversed:
                sub_crv = self.reverse(sub_crv[0], sub_crv[-1], sub_crv)
                # reverse the curve around the starting and end point
            curve = curve + sub_crv
            last_point = sub_crv[-1]
        return curve

    def remove_repeated_points(self, curve):
        """
        removes the repeated points in the curve
        """
        new_curve = [curve[0]]
        last_point = curve[0]
        for next_point in curve[1:]:
            if next_point != last_point:
                new_curve.append(next_point)
            last_point = next_point
        return new_curve

    def round_corners(self, curve):
        """
        Return the curve with rounded corners

        Replaces two points with their midpoint while retaining the
        start and end points
        """
        round_weight = 3
        rounded_curve = [curve[0]]  # retain the first point
        current_point = curve[0]
        for next_point in curve[1:]:
            mid_point = (
                (current_point[0] + next_point[0] * round_weight) / (1 + round_weight),
                (current_point[1] + next_point[1] * round_weight) / (1 + round_weight))
            rounded_curve.append(mid_point)
            current_point = next_point
            round_weight = 1 / round_weight
        rounded_curve.append(curve[-1])  # retain the last point
        return rounded_curve

    def draw_fractal(self, recursion_depth=None, round_corners=False):
        """
        Draw the fractal curve on the canvas of the parent class
        """
        if recursion_depth:
            curve_to_draw = self.fractal_curve(recursion_depth)
        else:
            curve_to_draw = self.fractal_curve(self.recursion_depth)
        if len(curve_to_draw) > 1:  # draw only if there are more than one points
            if round_corners:
                curve_to_draw = self.round_corners(
                    self.remove_repeated_points(curve_to_draw))
            self.parent.canvas.create_line(curve_to_draw)
        else:
            self.parent.canvas.bell()  # ring bell to indicate wrong action
