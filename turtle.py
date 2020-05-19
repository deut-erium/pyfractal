"""Self made, custom turtle module"""
import tkinter
import random
ROOT = tkinter.Tk()
ROOT.title = "The Fractalizer"

class Turtle:
    """Turtle class for drawing instructions"""
    def __init__(self, canvas ,x_coord = 0, y_coord = 0):
        """Initialize a new turtle object on the canvas at the provided x and y coordinates"""
        self.x = x_coord
        self.y = y_coord
        self.canvas = canvas

    def __str__(self):
        """String representation containing x and y coordinate"""
        return "x: {0}, y:{1}".format(self.x, self.y)

    def __add__(self,xy_tuple):
        """Add xy_tuple (i.e a tuple containing x and y coordinate values to be added to) the turtle object"""
        return Turtle(self.canvas, self.x + xy_tuple[0], self.y + xy_tuple[1])
    def __sub__(self,xy_tuple):
        """Subtract xy_tuple (i.e a tuple containing x and y coordinate values to be added to) the turtle object"""
        return Turtle(self.canvas, self.x - xy_tuple[0], self.y - xy_tuple[1])
    def __iadd__(self,xy_tuple):
        """Assignment addition of xy_tuple (i.e a tuple containing x and y coordinate values to be added to) the turtle object"""
        self = self + xy_tuple
        return self

    def __isub__(self,xy_tuple):
        """Assignment subtraction xy_tuple (i.e a tuple containing x and y coordinate values to be added to) the turtle object"""
        self = self - xy_tuple
        return self

