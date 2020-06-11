"""Handling of parameters outside the main GUI class"""

import os
import re
from tkinter import filedialog, Button, Entry, Label, W, END, \
    Checkbutton, BooleanVar
from pyfractal.rules_input import RulesInput


class Parameters():
    """
    Class for holding the functionality and fields in the parameters
    frame of GUI class this class would contain different methods for
    interaction with the canvas and general features desired in an
    application
    """

    def __init__(self, parent_class):
        """
        Initializing the class into the frame of parent GUI class
        i.e parent_class intended to access features of parent class
        """
        self.parent_class = parent_class
        self.frame = parent_class.frames["parameters"]
        self.rules_frame_class = None  # different class to add rules
        # stuff upadated in its own frame
        # things added dynamically
        self.buttons = {
            "btn_save_as": None,
            "btn_clear_canvas": None,
            "btn_draw": None,
            "btn_save_params": None,
            "chkbtn_round_corners": None,
            "chkbtn_color": None
        }
        self.entries = {
            "ent_recursion_depth": None,
            "ent_base_length": None
        }
        self.labels = {
            "lbl_recursion_depth": None,
            "lbl_base_length": None
        }
        self.vars = {
            "round_corners": None,
            "fill_color": None
        }
        self.init_saveas_button()
        self.init_clear_canvas_button()
        self.init_recursion_depth_entry()
        self.init_base_length_entry()
        self.init_draw_button()
        self.init_save_curve_params_button()
        self.init_load_params_button()
        self.init_round_curve_checkbox()
        self.init_fill_color_checkbox()
        self.init_rules_frame()

    def init_saveas_button(self):
        """
        save_as button to save canvas into svg, ps, png extensions
        """
        def save():
            """
            function to invoke different save routines
            """
            file_name = filedialog.asksaveasfilename(
                filetypes=[
                    ("Scalable Vector Graphics", "*.svg"),
                    ("Postscript", "*.ps"),
                    ("Portable Network Graphics", "*.png")
                ],
                initialdir=os.getcwd())
            if file_name:  # save option not cancelled by user
                extension = re.search(r"\.[\w]+$", file_name)[0]
                if extension == '.png':
                    self.parent_class.save_png(file_name)
                elif extension == ".ps":
                    self.parent_class.save_postscript(file_name)
                elif extension == ".svg":
                    self.parent_class.save_canvas_svg(file_name)
                else:
                    raise TypeError("Unknown Filetype")

        self.buttons["btn_save_as"] = Button(
            self.frame, text="Save Canvas As", command=save)
        self.buttons["btn_save_as"].grid(row=5, column=0)

    def init_clear_canvas_button(self):
        """
        Button to clear the canvas to a blank state
        """
        def clear_canvas():
            """ Function to clear the canvas"""
            self.parent_class.canvas.delete("all")

        self.buttons["btn_clear_canvas"] = Button(
            self.frame, width=14, text="Clear", command=clear_canvas)
        self.buttons["btn_clear_canvas"].grid(row=3, column=1)

    def init_recursion_depth_entry(self):
        """
        Entry field to specify recursion depth of the fractal
        from the user, entries fetched on executing draw
        """
        vcmd = (self.frame.register(self.validate_integer), '%P')
        # input validation clarification
        # https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
        self.entries["ent_recursion_depth"] = Entry(
            self.frame, width=2,
            validate='key', validatecommand=vcmd)
        self.labels["lbl_recursion_depth"] = Label(
            self.frame, text="Recursion Depth (int)")
        self.entries["ent_recursion_depth"].grid(
            row=0, column=1, sticky=W, pady=(30, 0))
        self.labels["lbl_recursion_depth"].grid(
            row=0, column=0, sticky=W, pady=(30, 0))

    def validate_integer(self, p_str):
        """
        Validate only if p_str is integer or null input
        """
        # p_str is str
        if re.search(r"^[1-9]\d*$", p_str) or p_str == "":
            return True
        self.frame.bell()  # alert wrong input
        return False

    def validate_float(self, p_str):
        """
        Validate if input is a valid floating point number
        """
        # may validate only '[+-].' which needs to be handled later
        float_pattern = r"^[\+\-]?([0-9]*[.])?[0-9]*$"
        if re.search(float_pattern, p_str) or p_str == "":
            return True
        self.frame.bell()
        return False

    def init_base_length_entry(self):
        """
        Entry field to specify side length of base fractal curve
        """
        vcmd = (self.frame.register(self.validate_float), '%P')
        self.entries["ent_base_length"] = Entry(
            self.frame, width=10,
            validate='key', validatecommand=vcmd)

        self.entries["ent_base_length"] = Entry(
            self.frame, width=10,
            validate='key', validatecommand=vcmd)
        self.labels["lbl_base_length"] = Label(
            self.frame, text="Base Length (float)")
        self.entries["ent_base_length"].grid(row=1, column=1, sticky=W)
        self.labels["lbl_base_length"].grid(row=1, column=0, sticky=W)

    def init_draw_button(self):
        """
        Initialize draw button on the frame which draws the fractal curve
        of the parent class
        """
        def draw():
            """
            Invoke draw function of fractal class of the parent
            with suitable arguments
            """
            recursion_depth = self.get_recursion_depth()
            base_length = self.get_base_length()
            self.parent_class.classes["fractal"].set_base_length(base_length)
            is_curved = self.vars["round_corners"].get()
            fill_color = self.vars["fill_color"].get()
            self.parent_class.classes["fractal"].draw_fractal(
                recursion_depth, is_curved, fill_color)

        self.buttons["btn_draw"] = Button(
            self.frame, width=14, text="Draw Fractal", command=draw)
        self.buttons["btn_draw"].grid(row=3, column=0)

    def init_save_curve_params_button(self):
        """
        Initialize Button to invoke save parameters to a file
        """
        def save_params():
            """
            function to invoke different save routines
            """
            file_name = filedialog.asksaveasfilename(
                filetypes=[
                    ("JSON", "*.json")
                ],
                initialdir=os.getcwd())
            if file_name:  # save option not cancelled by user
                self.parent_class.classes["fractal"].curve.store_curve_tofile(
                    file_name)

        self.buttons["btn_save_params"] = Button(
            self.frame, text="Save Parameters", command=save_params)
        self.buttons["btn_save_params"].grid(row=4, column=1)

    def init_round_curve_checkbox(self):
        """
        Initializes checkbox for drawing curve with rounded corners

        Rounding corners is done simply by replacing points with the
        midpoints of adjacent points on the original fractal curve
        """
        self.vars["round_corners"] = BooleanVar(self.frame)
        self.buttons["chkbtn_round_corners"] = Checkbutton(
            self.frame, text='round corners',
            var=self.vars["round_corners"])
        self.buttons["chkbtn_round_corners"].grid(row=6, column=0)

    def init_fill_color_checkbox(self):
        """
        Initializes checkbox to fill the color in fractal while drawing

        Although the fractal is open curve most of the instances, it will
        fill color by making it closed by connecting starting and ending
        points
        """
        self.vars["fill_color"] = BooleanVar(self.frame)
        self.buttons["chkbtn_color"] = Checkbutton(
            self.frame, text='fill color',
            var=self.vars["fill_color"])
        self.buttons["chkbtn_color"].grid(row=6, column=1)

    def init_load_params_button(self):
        """
        Initialize the button to load parameters from a json file
        """
        def load_params():
            """
            load parameters from the Curve class to the fastfractal
            """
            file_name = filedialog.askopenfilename(
                filetypes=[("JSON", "*.json")])
            if file_name:
                self.parent_class.classes["fractal"].curve.load_from_file(
                    file_name)
                self.parent_class.classes["fractal"].curve.set_parent_parameters(
                )
                self.rules_frame_class.fill_entries_from_rules(
                    self.parent_class.classes["fractal"].rules)
                # fill the entries in rules input on load
                self.set_recursion_depth_entry(
                    self.parent_class.classes["fractal"].recursion_depth)
                self.set_base_length_entry(
                    self.parent_class.classes["fractal"].base_length)
                self.rules_frame_class.render_preview()

        self.buttons["btn_load_params"] = Button(
            self.frame, text="Load Parameters", command=load_params)
        self.buttons["btn_load_params"].grid(row=4, column=0)

    def init_rules_frame(self):
        """
        Initialize a frame to hold entries for input of rule
        """
        self.rules_frame_class = RulesInput(self)

    def get_recursion_depth(self):
        """Return the user provided input of recursion depth"""
        str_depth_input = self.entries["ent_recursion_depth"].get()
        if str_depth_input == '':
            return None  # default of fractal class while drawing in None
            # draws the base curve instead
        return int(str_depth_input)

    def get_base_length(self):
        """Return the user provided input of base length"""
        str_len_input = self.entries["ent_base_length"].get()
        if str_len_input in ['', '.', '+.', '-.', '+', '-']:
            return 10.0  # default base length
        return float(str_len_input)

    def set_recursion_depth_entry(self, recursion_depth):
        """
        Set the given recursion_depth into the entry
        """
        self.entries["ent_recursion_depth"].delete(0, END)
        self.entries["ent_recursion_depth"].insert(
            0, str(recursion_depth))

    def set_base_length_entry(self, base_length):
        """
        Set the provided base_length into the entry field
        """
        self.entries["ent_base_length"].delete(0, END)
        self.entries["ent_base_length"].insert(
            0, str(base_length))
