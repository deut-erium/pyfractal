"""Class to store, import, export, display defined curves """
import math
import json
from pkg_resources import resource_string as resource_bytes
PI = math.pi
RAD_FAC = PI / 180  # factor to multiply to convert degrees to radians
DEG_FAC = 180 / PI  # factor multiplied to convert radians to degree


class Curve():
    """
    Class to represent a curve through its parameters (base rules)
    implemented for flip representations for now, should be extended later
    """

    def __init__(self, parent=None):
        """
        Initialize the curve through its base rules
        """
        self.parent = parent
        self.rules = None
        self.base_length = None
        self.start_point = None
        self.recursion_depth = 1

    def load_from_file(self, filepath):
        """
        Load the curve from a file
        """
        with open(filepath, 'r') as curve_data_file:
            try:
                curve_data = json.load(curve_data_file)
                self.rules = curve_data["rules"]
                self.base_length = curve_data["base_length"]
                self.start_point = curve_data["start_point"]
                self.recursion_depth = curve_data["recursion_depth"]
            except (json.JSONDecodeError, KeyError):
                print("Malformed JSON data")

    def load_from_resource(self, resource_file):
        """
        Load curve data from resource_file in the package
        """
        resource_data = resource_bytes('pyfractal', resource_file)
        try:
            curve_data = json.loads(resource_data)
            self.rules = curve_data["rules"]
            self.base_length = curve_data["base_length"]
            self.start_point = curve_data["start_point"]
            self.recursion_depth = curve_data["recursion_depth"]
        except (json.JSONDecodeError, KeyError):
            print("Malformed JSON data")
        except FileNotFoundError:
            print("Curve resource file not found/available")

    def store_curve_tofile(self, filepath):
        """
        Store the curve representation in a file (JSON)
        """
        self.get_parameters()
        curve_data = {
            "rules": self.rules,
            "base_length": self.base_length,
            "start_point": self.start_point,
            "recursion_depth": self.recursion_depth
        }
        with open(filepath, 'w') as write_file:
            json.dump(curve_data, write_file, indent=2)

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

    def convert_rules_angles(self, rules=None, to_radians=True):
        """
        Convert the angles used in representation from degrees to
        radians and vice versa.
        to_radians = True changes the angles in degrees to radians
        to_radians = False changes radian angles to degrees
        if no rules are provided, it modifies self.rules
        """
        modify_self_rules = False
        if rules is None:
            rules = self.rules
            modify_self_rules = True
        converted_rules = []
        for rule in rules:
            angle, factor, is_flipped, is_reversed = rule
            if to_radians:
                new_angle = angle * RAD_FAC
            else:
                new_angle = angle * DEG_FAC
            converted_rules.append((
                new_angle, factor, is_flipped, is_reversed))
        if modify_self_rules:
            self.rules = converted_rules
        return converted_rules

    def get_parameters(self):
        """
        Get the curve parameters from the parent(FastFractal) class
        """
        self.rules = self.parent.rules
        self.start_point = self.parent.start_point
        self.base_length = self.parent.base_length
        self.recursion_depth = self.parent.recursion_depth

    def set_parent_parameters(self):
        """
        Set the curve parameters in the parent(FastFractal) class
        """
        self.parent.rules = self.rules
        self.parent.start_point = self.start_point
        self.parent.base_length = self.base_length
        self.parent.recursion_depth = self.recursion_depth
