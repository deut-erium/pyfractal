"""Class to store, import, export, display defined curves """
import math
PI = math.pi
RAD_FAC = PI / 180  # factor to multiply to convert degrees to radians
DEG_FAC = 180 / PI  # factor multiplied to convert radians to degree


class Curve():
    """
    Class to represent a curve through its parameters (base rules)
    implemented for flip representations for now, should be extended later
    """

    def __init__(self):
        """
        Initialize the curve through its base rules
        """
        self.rules = None
        print("TODO")

    def load_from_file(self, filepath):
        """
        Load the curve from a file
        """
        print("TODO", filepath)

    def store_curve_tofile(self, filepath):
        """
        Store the curve representation in a file
        """
        print("TODO", filepath)

    def from_turtle_representation(self, representation_string):
        """
        Initialize the class from the representation_string used to
        define the fractal as could be drawn by turtle

          _____
         /     \\    This curve would be drawn assuming initial
        /       \\   direction in which the turtle is heading to
        |       |    be right and ending direction in which it
        |       |    will end will also be right
        |       |    so the commands executed would be left 90
                     forward l, right 45, forward l/sqrt(2), right 45,
                     forward l, right 45, forward l/sqrt(2), right 45,
                     forward l, left 90
            i.e in such a manner, the total angle rotated by it
            is 0 degrees. The flips are represented similarly

        Representation f:<length_factor>:flipped(-1/1),reversed(-1/1),
                        r/l theta(degrees)
                        c<length_factor>
        instruction of c type (for not fractalizing that length)
        Example of the above curve:
        "l:90,f:1:1:1,r:45,f:0.707:1:-1,r:45,f:1:1:1,r:45, \
        f:0.707:1:-1,r:45,f:1:1:1"
        """
        instructions = representation_string.strip().split(",")
        formed_rules = []
        current_angle = 0  # radians
        for instruction in instructions:
            instr_unpacked = instruction.split(":")
            if instr_unpacked[0] == 'l':
                current_angle += float(instr_unpacked[1]) * RAD_FAC
                current_angle = current_angle % (2 * PI)
            elif instr_unpacked[0] == 'r':
                current_angle -= float(instr_unpacked[1]) * RAD_FAC
                current_angle = current_angle % (2 * PI)
            elif instr_unpacked[0] == 'c':
                length_factor = float(instr_unpacked[1])
                formed_rules.append(
                    (current_angle, length_factor, None, None))
            elif instr_unpacked[0] == 'f':
                length_factor = float(instr_unpacked[1])
                if instr_unpacked[2] == '1':
                    is_flipped = False
                else:
                    is_flipped = True
                if instr_unpacked[3] == '1':
                    is_reversed = False
                else:
                    is_reversed = True
                formed_rules.append(
                    (current_angle, length_factor,
                     is_flipped, is_reversed))
        self.rules = formed_rules
        return formed_rules
