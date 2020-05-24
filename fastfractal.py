"""Module for drawing fractals fastly by operations on points directly"""
from math import cos, sin


class FastFractal():
    """
    FastFractal class to generate a list of points denoting points of line
    fractals on the canvas
    """

    def __init__(self, rules, start_point, base_length):
        """
        Initialize the canvas
        """
        self.rules = rules
        self.start_point = start_point
        self.base_length = base_length

    def reflection(line, point):
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

    def rotate_scale(center, theta, scale, curve):
        """
        Rotate the curve (list of points (x,y)) by theta around the
        center (cx,cy) and scale the curve by a factor of scale

        x -> c_x + (x-c_x)*cos(theta)*scale - (y-c_y)*sin(theta)*scale
        y -> c_y + (x-c_x)*sin(theta)*scale + (y-c_y)*cos(theta)*scale
        for each (x,y) tuple in curve
        """
        c_x, c_y = center
        return [[c_x +
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
                 cos(theta)] for i, j in curve]

    def translate(center, curve):
        """
        translate the curve to the provided center
        """
        offset_x = center[0] - curve[0][0]  # offset wrt first point of curve
        offset_y = center[1] - curve[0][1]
        return [[i + offset_x, j + offset_y] for i, j in curve]

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
