"""Main Class for handling GUI of the application"""

import io
import math
import os
import re
from tkinter import Tk, Frame, Canvas, Scrollbar, Menu, filedialog, Button
from tkinter import HORIZONTAL, VERTICAL, BOTH, TOP, LEFT, RIGHT, X, Y, BOTTOM
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
        self.canvas.bind("<MouseWheel>", self.windows_zoomer)  # windows scroll

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
    Class for holding the functionality and fields in the parameters frame of 
    GUI class this class would contain different methods for interaction with
    the canvas and general features desired in an application
    """
    def __init__(self, parent_class):
        """
        Initializing the class into the frame of parent i.e the frame in which
        the elements would be placed
        parent_class intended to access features of parent class
        """
        self.parent_class = parent_class
        self.frame = parent_class.frames["parameters"]
        self.buttons = {
            "btn_save_as" : None
        }
        self.entries = {

        }
        self.init_saveas_button()

    def init_saveas_button(self):
        """
        save_as button
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
                    initialdir = os.getcwd())
            if file_name:
                extension = re.search("\.[\w]+$",file_name)[0]
                if extension == '.png':
                    self.parent_class.save_png(file_name)
                elif extension == ".ps":
                    self.parent_class.save_postscript(file_name)
                elif extension == ".svg":
                    self.parent_class.save_canvas_svg(file_name)
                else:
                    raise TypeError("Unknown Filetype")

        self.buttons["btn_save_as"] = Button(self.frame, text="Save As", command = save)
        self.buttons["btn_save_as"].pack()
        




A_ADV = GUI()
v = Parameters(A_ADV)
rules = [(math.pi/2,1,False,True),(0,0.5773,True,True),(0,0.5773,False,False),(-2*math.pi/3,0.5773,False,False),(-math.pi/6,1,True,False)]
start_point = (100,100)
base_length = 10
fractal = FastFractal(rules,start_point,base_length)
rules = [(math.pi/2,1,False,True),(0,0.5773,True,True),(0,0.5773,False,False),(-2*math.pi/3,0.5773,False,False),(-math.pi/6,1,True,False)]
start_point = (100,100)
base_length = 10
fractal = FastFractal(rules,start_point,base_length)
A_ADV.canvas.create_line(fractal.fractal_curve(8))
A_ADV.window.mainloop()
