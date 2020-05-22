"""Main Class for handling GUI of the application"""
from tkinter import Tk, Frame, Canvas, Scrollbar, Menu
from tkinter import HORIZONTAL, VERTICAL, BOTH, TOP, LEFT, RIGHT, X, Y, BOTTOM


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
        self.frm_canvas = None
        self.frm_parameters = None
        self.menubar = None
        self.helpmenu = None
        self.filemenu = None
        self.editmenu = None
        self.init_canvas_frame()
        self.init_parameters_frame()
        self.init_menu_bar()
        self.window.mainloop()

    def init_canvas_frame(self, max_width=1080, max_height=1920):
        """
        Creates and initializes a Frame for the canvas
        max_width, max_height determine the maximum scrollable area
        """
        self.frm_canvas = Frame(master=self.window, width=400, height=400)
        self.canvas = Canvas(
            master=self.frm_canvas,
            scrollregion=(0, 0, max_width, max_height))
        h_scrl_bar = Scrollbar(self.frm_canvas, orient=HORIZONTAL)
        h_scrl_bar.pack(side=BOTTOM, fill=X)
        h_scrl_bar.config(command=self.canvas.xview)
        v_scrl_bar = Scrollbar(self.frm_canvas, orient=VERTICAL)
        v_scrl_bar.pack(side=RIGHT, fill=Y)
        v_scrl_bar.config(command=self.canvas.yview)
        self.canvas.config(
            xscrollcommand=h_scrl_bar.set,
            yscrollcommand=v_scrl_bar.set)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.frm_canvas.pack(anchor="nw", side=TOP, expand=True, fill=BOTH)

    def init_parameters_frame(self, height=200, width=400):
        """
            Initializes frame for parameters/buttons
        """
        self.frm_parameters = Frame(
            master=self.window,
            width=width,
            height=height,
            bg="pink")
        self.frm_parameters.pack(
            anchor="ne",
            side=BOTTOM,
            expand=False,
            fill=BOTH)

    def init_menu_bar(self):
        """
        initializes the menubar
        """
        self.menubar = Menu(self.window)
        self.init_filemenu()
        self.init_editmenu()
        self.init_helpmenu()
        self.window.config(menu=self.menubar)

    def init_filemenu(self):
        """
        initializes filemenu in menubar
        """
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=todo)
        self.filemenu.add_command(label="Open", command=todo)
        self.filemenu.add_command(label="Save", command=todo)
        self.filemenu.add_command(label="Save as...", command=todo)
        self.filemenu.add_command(label="Close", command=todo)
        self.filemenu.add_separator()
        self.menubar.add_cascade(label="File", menu=self.filemenu)

    def init_editmenu(self):
        """
        initializes editmenu in menubar
        """
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Undo", command=todo)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Cut", command=todo)
        self.editmenu.add_command(label="Copy", command=todo)
        self.editmenu.add_command(label="Paste", command=todo)
        self.editmenu.add_command(label="Delete", command=todo)
        self.editmenu.add_command(label="Select All", command=todo)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

    def init_helpmenu(self):
        """
        initializes helpmenu in menubar
        """
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=todo)
        self.helpmenu.add_command(label="About...", command=todo)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)


A_ADV = GUI()
