"""Main Class for handling GUI of the application"""

import io
import math
import os
import re
from tkinter import Tk, Frame, Canvas, Scrollbar, Menu, filedialog, Button, Entry, Label
from tkinter import HORIZONTAL, VERTICAL, BOTH, TOP, \
    LEFT, RIGHT, X, Y, BOTTOM
from PIL import Image
import canvasvg
from fastfractal import FastFractal


def todo():
    """ function substituted to do"""
    print("OK")


class GUI():
    """Class for handling GUI of application"""

    def __init__(self, min_height=600, min_width=600):
        """
        Initialize the main window of the application

        Initializes other relevant fields too
        """
        self.window = Tk()
        # set minimum size to which the window can be reduced
        self.window.minsize(min_width, min_height)
        self.canvas = None
        self.frames = {
            "parameters": None,
            "canvas": None
        }
        self.menubar = {
            "menubar": None,
            "helpmenu": None,
            "filemenu": None,
            "editmenu": None
        }
        self.init_canvas_frame()
        self.init_parameters_frame()
        self.init_menu_bar()
        self.classes = {
            "parameters": Parameters(self),
            "fractal": FastFractal(self)
        }

    def init_canvas_frame(self, max_width=1080, max_height=1920):
        """
        Creates and initializes a Frame for the canvas
        max_width, max_height determine the maximum scrollable area
        """
        self.frames["canvas"] = Frame(
            master=self.window, width=400, height=400)
        self.canvas = Canvas(
            master=self.frames["canvas"],
            scrollregion=(0, 0, max_width, max_height))
        h_scrl_bar = Scrollbar(self.frames["canvas"], orient=HORIZONTAL)
        h_scrl_bar.pack(side=BOTTOM, fill=X)
        h_scrl_bar.config(command=self.canvas.xview)
        v_scrl_bar = Scrollbar(self.frames["canvas"], orient=VERTICAL)
        v_scrl_bar.pack(side=RIGHT, fill=Y)
        v_scrl_bar.config(command=self.canvas.yview)
        self.canvas.config(
            xscrollcommand=h_scrl_bar.set,
            yscrollcommand=v_scrl_bar.set)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.frames["canvas"].pack(
            anchor="nw", side=LEFT, expand=True, fill=BOTH)

        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        self.canvas.bind("<Button-4>", self.linux_zoomer_plus)
        self.canvas.bind("<Button-5>", self.linux_zoomer_minus)
        # windows scroll
        self.canvas.bind("<MouseWheel>", self.windows_zoomer)

    def move_start(self, event):
        """
        Mark the coordinates to start moving
        """
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        """
        move to dragged position
        """
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def windows_zoomer(self, event):
        """
        Zoomer functionality for windows
        """
        if event.delta > 0:
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif event.delta < 0:
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def linux_zoomer_plus(self, event):
        """
        Zoom into functionality linux
        """
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def linux_zoomer_minus(self, event):
        """
        Zoom out functionality linux
        """
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def init_parameters_frame(self, height=400, width=300):
        """
            Initializes frame for parameters/buttons
        """
        self.frames["parameters"] = Frame(
            master=self.window,
            width=width,
            height=height,
            bg="pink")
        self.frames["parameters"].pack(
            anchor="ne",
            side=RIGHT,
            expand=False,
            fill=BOTH)

    def init_menu_bar(self):
        """
        initializes the menubar
        """
        self.menubar["menubar"] = Menu(self.window)
        self.init_filemenu()
        self.init_editmenu()
        self.init_helpmenu()
        self.window.config(menu=self.menubar["menubar"])

    def init_filemenu(self):
        """
        initializes filemenu in menubar
        """
        self.menubar["filemenu"] = Menu(self.menubar["menubar"], tearoff=0)
        self.menubar["filemenu"].add_command(label="New", command=todo)
        self.menubar["filemenu"].add_command(label="Open", command=todo)
        self.menubar["filemenu"].add_command(label="Save", command=todo)
        self.menubar["filemenu"].add_command(label="Save as...", command=todo)
        self.menubar["filemenu"].add_command(label="Close", command=todo)
        self.menubar["filemenu"].add_separator()
        self.menubar["menubar"].add_cascade(
            label="File", menu=self.menubar["filemenu"])

    def init_editmenu(self):
        """
        initializes editmenu in menubar
        """
        self.menubar["editmenu"] = Menu(self.menubar["menubar"], tearoff=0)
        self.menubar["editmenu"].add_command(label="Undo", command=todo)
        self.menubar["editmenu"].add_separator()
        self.menubar["editmenu"].add_command(label="Cut", command=todo)
        self.menubar["editmenu"].add_command(label="Copy", command=todo)
        self.menubar["editmenu"].add_command(label="Paste", command=todo)
        self.menubar["editmenu"].add_command(label="Delete", command=todo)
        self.menubar["editmenu"].add_command(label="Select All", command=todo)
        self.menubar["menubar"].add_cascade(
            label="Edit", menu=self.menubar["editmenu"])

    def init_helpmenu(self):
        """
        initializes helpmenu in menubar
        """
        self.menubar["helpmenu"] = Menu(self.menubar["menubar"], tearoff=0)
        self.menubar["helpmenu"].add_command(label="Help Index", command=todo)
        self.menubar["helpmenu"].add_command(label="About...", command=todo)
        self.menubar["menubar"].add_cascade(
            label="Help", menu=self.menubar["helpmenu"])

    def save_canvas_svg(self, filename):
        """
        Save the canvas as an svg
        """
        canvasvg.saveall(filename, self.canvas)

    def save_postscript(self, filename):
        """
        Save canvas as postscript
        """
        with open(filename, 'w') as savefile:
            savefile.write(self.canvas.postscript())

    def save_png(self, filename):
        """
        Save canvas as png
        """
        post_script = self.canvas.postscript().encode()
        img = Image.open(io.BytesIO(post_script))
        img.save(filename, format="PNG")


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
        self.buttons = {
            "btn_save_as": None,
            "btn_clear_canvas": None,
            "btn_draw": None,
            "btn_save_params": None
        }
        self.entries = {
            "ent_recursion_depth": None,
            "ent_base_length": None
        }
        self.labels = {
            "lbl_recursion_depth": None,
            "lbl_base_length": None
        }
        self.init_saveas_button()
        self.init_clear_canvas_button()
        self.init_recursion_depth_entry()
        self.init_base_length_entry()
        self.init_draw_button()
        self.init_save_curve_params_button()
        self.init_load_params_button()

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
            self.frame, text="Save As", command=save)
        self.buttons["btn_save_as"].pack()

    def init_clear_canvas_button(self):
        """
        Button to clear the canvas to a blank state
        """
        def clear_canvas():
            """ Function to clear the canvas"""
            self.parent_class.canvas.delete("all")

        self.buttons["btn_clear_canvas"] = Button(
            self.frame, text="Clear", command=clear_canvas)
        self.buttons["btn_clear_canvas"].pack()

    def init_recursion_depth_entry(self):
        """
        Entry field to specify recursion depth of the fractal
        from the user, entries fetched on executing draw
        """
        vcmd = (self.frame.register(self.validate_integer), '%P')
        # input validation clarification
        # https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
        self.entries["ent_recursion_depth"] = Entry(
            self.frame, width=10,
            validate='key', validatecommand=vcmd)
        self.labels["lbl_recursion_depth"] = Label(
            self.frame, text="Recursion Depth")
        self.entries["ent_recursion_depth"].pack(side=RIGHT)
        self.labels["lbl_recursion_depth"].pack(side=LEFT)

    def validate_integer(self, P):
        """
        Validate only if P is integer or null input
        """
        # P is str
        if re.search(r"^[1-9]\d*$", P) or P == "":
            return True
        return False

    def validate_float(self, P):
        """
        Validate if input is a valid floating point number
        """
        # may validate only '[+-].' which needs to be handled later
        float_pattern = r"^[\+\-]?([0-9]*[.])?[0-9]*$"
        if re.search(float_pattern, P) or P == "":
            return True
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
            self.frame, text="Base Length")
        self.entries["ent_base_length"].pack(side=RIGHT)
        self.labels["lbl_base_length"].pack(side=LEFT)

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
            rules = [
                (math.pi / 2,
                 1,
                 False,
                 True),
                (0,
                 0.5773,
                 True,
                 True),
                (0,
                 0.5773,
                 False,
                 False),
                (-2 * math.pi / 3,
                 0.5773,
                 False,
                 False),
                (-math.pi / 6,
                 1,
                 True,
                 False)]
            start_point = (100, 100)
            recursion_depth = self.get_recursion_depth()
            base_length = self.get_base_length()
            self.parent_class.classes["fractal"].set_rules(rules)
            self.parent_class.classes["fractal"].set_base_length(base_length)
            self.parent_class.classes["fractal"].set_startpoint(start_point)
            self.parent_class.classes["fractal"].draw_fractal(recursion_depth)

        self.buttons["btn_draw"] = Button(
            self.frame, text="Draw Fractal", command=draw)
        self.buttons["btn_draw"].pack()
    
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
                self.parent_class.classes["fractal"].curve.store_curve_tofile(file_name)

        self.buttons["btn_save_params"] = Button(
            self.frame, text="Save Parameters", command=save_params)
        self.buttons["btn_save_params"].pack()
    
    def init_load_params_button(self):
        """
        Initialize the button to load parameters from a json file
        """
        def load_params():
            """
            load parameters from the Curve class to the fastfractal
            """
            file_name = filedialog.askopenfilename(filetypes = [("JSON","*.json")])
            if file_name:
                self.parent_class.classes["fractal"].curve.load_from_file(file_name)
                self.parent_class.classes["fractal"].curve.set_parent_parameters()
        self.buttons["btn_load_params"] = Button(
                self.frame, text="Load Parameters", command=load_params)
        self.buttons["btn_load_params"].pack()

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
        if str_len_input in ['', '.', '+.', '-.']:
            return 10.0  # default base length
        return float(str_len_input)


A_ADV = GUI()
# A_ADV.canvas.create_line(fractal.fractal_curve(7))
A_ADV.window.mainloop()
