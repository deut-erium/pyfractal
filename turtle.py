"""Self made, custom turtle module"""
#import tkinter
#import random
import math
#ROOT = tkinter.Tk()
#ROOT.title = "The Fractalizer"


class Turtle:
    """Turtle class for drawing instructions"""

    def __init__(self, canvas, x_coord=0, y_coord=0, angle=0, radians = False, pendown = True):
        """
            Initialize a new turtle object on the canvas at the provided x and y coordinates
            heading denotes the direction in which the turtle is heading in radians
            radians specifies whether the angle provided is in radians
            pendown indicates the drawing state of the turtle pen
        """
        self.x = x_coord
        self.y = y_coord
        self.canvas = canvas
        # Note that angle is stored as a radian value internally
        self.angle = angle if radians else angle * math.pi / 180
        self.angle = self.angle % (math.pi * 2)
        self.pendown = True

    def __str__(self):
        """String representation containing x and y coordinate"""
        return "x: {0}, y:{1}, angle:{2}, pendown:{3}".format(
            self.x, self.y, self.angle * 180 / math.pi, pendown)

    def __add__(self, xy_tuple):
        """Add xy_tuple (i.e a tuple containing x and y coordinate values to be added to) the turtle object"""
        if not isinstance(xy_tuple, (tuple, list)) or len(xy_tuple) < 2:
            raise ValueError("Expected a tuple or list of size 2")
        return Turtle(self.canvas, self.x + xy_tuple[0], self.y + xy_tuple[1])

    def __sub__(self, xy_tuple):
        """Subtract xy_tuple (i.e a tuple containing x and y coordinate values to be added to) the turtle object"""
        if not isinstance(xy_tuple, (tuple, list)) or len(xy_tuple) < 2:
            raise ValueError("Expected a tuple or list of size 2")
        return Turtle(self.canvas, self.x - xy_tuple[0], self.y - xy_tuple[1])

    def __iadd__(self, xy_tuple):
        """Assignment addition of xy_tuple (i.e a tuple containing x and y coordinate values to be added to) the turtle object"""
        if not isinstance(xy_tuple, (tuple, list)) or len(xy_tuple) < 2:
            raise ValueError("Expected a tuple or list of size 2")
        self.x, self.y = self.x + xy_tuple[0], self.y + xy_tuple[1]
        return self

    def __isub__(self, xy_tuple):
        """Assignment subtraction xy_tuple (i.e a tuple containing x and y coordinate values to be added to) the turtle object"""
        if not isinstance(xy_tuple, (tuple, list)) or len(xy_tuple) < 2:
            raise ValueError("Expected a tuple or list of size 2")
        self.x, self.y = self.x + xy_tuple[0], self.y + xy_tuple[1] 
        return self

    def recenter(self, xy_tuple):
        """
            Recenter itself to x-y tuple provided in coordinates
            Note: this method does not draw anything on screen
        """
        if not isinstance(xy_tuple, (tuple, list)) or len(xy_tuple) != 2:
            raise ValueError("Expected a tuple or list of size 2")
        self.x, self.y = xy_tuple

    def reface(self, angle, radians=False):
        """
            Change the facing angle to provided angle in degrees
            provided angle is in radians if radians = True
        """
        self.angle = angle if radians else angle * math.pi / 180
        self.angle = self.angle % (math.pi * 2)

    def forward(self, length):
        """Move forward length units in angle direction"""           
        x_move = math.cos(self.angle) * length
        y_move = math.sin(self.angle) * length
        if self.pendown:
            self.canvas.create_line(self.x, self.y, self.x + x_move, self.y + y_move)
        self.x, self.y = self.x + x_move, self.y + y_move

    def backward(self, length):
        """Move backwards length units without changing facing angle"""
        self.forward(-length)

    def left(self, angle, radians=False):
        """ Turn left by the angle specified
            the angle specified is in radians if radians == True, degrees otherwise
        """
        self.angle = self.angle + (angle if radians else angle * math.pi / 180)
        self.angle = self.angle % (math.pi * 2)

    def right(self, angle, radians=False):
        """ Turn right by the angle specified
            the angle specified is in radians if radians == True, degrees otherwise
        """
        self.left(-angle, radians)
    
    def set_pendown(self):
        """Set the penstate to down i.e pendown = True"""
        self.pendown = True

    def set_penup(self):
        """Set the penstate to up i.e pendown = False"""
        self.pendown = False

