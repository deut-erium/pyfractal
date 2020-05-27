"""Class to handle input and fetching rules from GUI"""
from tkinter import Frame, Button, Entry, BooleanVar, LEFT, RIGHT, Checkbutton, Tk
import re


class RulesInput():
    """
    Class to manage gui and logic for entry fields of rules
    in Parameters frame
    """

    def __init__(self, parent_frame):
        """
        Initialize parent_frame to the provided class to hold self.frame
        self.frame contains all the elements
        self.entries is a list of dynamically generated entries
        """
        self.parent_frame = parent_frame
        self.frame = Frame(parent_frame)
        self.entries = []  # list of dictionaries, each dictionary
        # contains the keys for frame, and its children
        self.add_button = None
        self.sub_button = None
        self.frame.pack()
        self.init_add_entry_button()
        self.init_sub_entry_button()

    def create_entry_dictionary(self):
        """
        Creates and returns a dictionary which contains references
        to a frame and entries in it
        keys: ["frame", "ent_len", "ent_angle", "chk_is_flip",
        "chk_is_rev", "flip_state","reverse_state"]
        """
        vcmd = (self.frame.register(self.validate_float), '%P')
        entry_frame = Frame(self.frame)
        ent_length = Entry(
            entry_frame, validate='key', validatecommand=vcmd)
        ent_angle = Entry(
            entry_frame, validate='key', validatecommand=vcmd)
        is_reversed_state = BooleanVar(entry_frame)
        is_flipped_state = BooleanVar(entry_frame)
        chkbtn_is_reversed = Checkbutton(
            entry_frame, text='reversed', var=is_reversed_state)
        chkbtn_is_flipped = Checkbutton(
            entry_frame, text='flipped', var=is_flipped_state)

        ent_length.pack(side=LEFT)
        ent_angle.pack(side=LEFT)
        chkbtn_is_flipped.pack(side=LEFT)
        chkbtn_is_reversed.pack(side=LEFT)
        entry_frame.pack()
        entry_dict = {
            "frame": entry_frame,
            "ent_len": ent_length,
            "ent_angle": ent_angle,
            "chk_is_flip": chkbtn_is_flipped,
            "chk_is_rev": chkbtn_is_reversed,
            "flip_state": is_flipped_state,
            "reverse_state": is_reversed_state
        }
        return entry_dict

    def init_add_entry_button(self):
        """
        Initialize the button which adds frames for entry of each rule
        """
        def add_entry():
            """
            create a new entry and add to self.entries
            """
            new_entry = self.create_entry_dictionary()
            self.entries.append(new_entry)

        self.add_button = Button(self.frame, text='+', command=add_entry)
        self.add_button.pack(side=RIGHT)

    def init_sub_entry_button(self):
        """
        Initialize the button to remove entry fields
        """
        def sub_entry():
            """
            Pop and destroy the last entry from self.entries
            """
            if self.entries != []:
                self.entries.pop()["frame"].destroy()

        self.sub_button = Button(self.frame, text='-', command=sub_entry)
        self.sub_button.pack(side=RIGHT)

    def validate_float(self, P):
        """
        Validate if input is a valid floating point number
        """
        # may validate only '[+-].' which needs to be handled later
        float_pattern = r"^[\+\-]?([0-9]*[.])?[0-9]*$"
        if re.search(float_pattern, P) or P == "":
            return True
        return False


if __name__ == "__main__":
    WINDOW = Tk()
    FRAME = Frame(WINDOW)
    FRAME.pack()
    RULES_INPUT = RulesInput(FRAME)
    WINDOW.mainloop()
