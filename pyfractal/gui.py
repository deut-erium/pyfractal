"""Main Class for handling GUI of the application"""

import io
from tkinter import Tk, Frame, Canvas, Scrollbar, Menu, ttk
from tkinter import HORIZONTAL, VERTICAL, BOTH, LEFT, RIGHT, \
    X, Y, BOTTOM, StringVar
from PIL import Image
from pkg_resources import resource_listdir
import canvasvg
from .fastfractal import FastFractal
from .parameters import Parameters


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
        self.combo_box = {
            "class": None,
            "variable": None
        }
        self.init_canvas_frame()
        self.init_parameters_frame()
        # self.init_menu_bar()
        self.classes = {
            "parameters": Parameters(self),
            "fractal": FastFractal(self)
        }
        self.init_parameter_combobox()

    def init_canvas_frame(self, max_width=4000, max_height=4000):
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

    def init_parameters_frame(self, height=400, width=200):
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

    def init_parameter_combobox(self):
        """
        Initialize the combobox for pre-defined curves
        """
        def load_resource():
            """
            Load the data of selected resource of selected item
            """
            resource_file = 'curves/' + self.combo_box["class"].get() + '.json'
            self.classes["fractal"].curve.load_from_resource(
                resource_file)
            self.classes["fractal"].curve.set_parent_parameters()
            self.classes["parameters"].rules_frame_class.fill_entries_from_rules(
                self.classes["fractal"].rules)
            self.classes["parameters"].set_base_length_entry(
                self.classes["fractal"].base_length)
            self.classes["parameters"].rules_frame_class.render_preview()

        self.combo_box["variable"] = StringVar()
        self.combo_box["class"] = ttk.Combobox(
            self.frames["parameters"],
            textvariable=self.combo_box["variable"],
            postcommand=load_resource)
        self.combo_box["class"]["values"] = sorted(list(map(
            lambda x: x.strip('.json'),
            resource_listdir('pyfractal', 'curves'))))
        # read curves resource, remove the json extension
        self.combo_box["class"].grid(row=5, column=1)
        self.combo_box["class"].current(0)
# load_resource()

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

    def run(self):
        """Function to run the mainloop of window of GUI class"""
        self.window.mainloop()


if __name__ == '__main__':
    A_ADV = GUI()
    A_ADV.run()
