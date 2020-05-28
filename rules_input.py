"""Class to handle input and fetching rules from GUI"""
from tkinter import Frame, Button, Entry, BooleanVar, \
         LEFT, END, Checkbutton, Tk, Canvas, Radiobutton, Label, W
import re
from math import cos, sin
from math import pi as PI
RAD_FAC = PI / 180  # factor to multiply to convert degrees to radians
DEG_FAC = 180 / PI  # factor multiplied to convert radians to degree


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
        self.preview_canvas = None  # canvas to preview curve
        self.entries = []  # list of dictionaries, each dictionary
        # contains the keys for frame, and its children
        self.add_button = None
        self.sub_button = None
        self.radio_angle_var = BooleanVar(
            self.frame)  # initially set to radians
        self.radio_angle_var.set(True)
        self.init_preview_canvas()
        self.init_info_labels()
        self.init_add_entry_button()
        self.init_sub_entry_button()
        # self.init_extract_rules_button()
        self.frame.grid(row=5,column=0,columnspan=3,sticky='nw',pady=10)

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
            entry_frame, validate='key',
            width=8, validatecommand=vcmd)
        ent_angle = Entry(
            entry_frame, validate='key',
            width=8, validatecommand=vcmd)
        is_reversed_state = BooleanVar(entry_frame)
        is_flipped_state = BooleanVar(entry_frame)
        chkbtn_is_reversed = Checkbutton(
            entry_frame, text='reverse', var=is_reversed_state)
        chkbtn_is_flipped = Checkbutton(
            entry_frame, text='flip', var=is_flipped_state)

        ent_angle.pack(side=LEFT)
        ent_length.pack(side=LEFT)
        chkbtn_is_flipped.pack(side=LEFT)
        chkbtn_is_reversed.pack(side=LEFT)
        entry_frame.grid(row=len(self.entries) + 3, columnspan=4)
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
            self.render_preview()

        self.add_button = Button(self.frame, text='+', command=add_entry)
        self.add_button.grid(row=1, column=2)

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
            self.render_preview()

        self.sub_button = Button(self.frame, text='-', command=sub_entry)
        self.sub_button.grid(row=1, column=3)

    def validate_float(self, p_str):
        """
        Validate if input is a valid floating point number
        """
        # may validate only '[+-].' which needs to be handled later
        float_pattern = r"^[\+\-]?([0-9]*[.])?[0-9]*$"
        if re.search(float_pattern, p_str) or p_str == "":
            return True
        return False

    def extract_rules(self):
        """
        Extract rules from the input fields to a list
        """
        def get_float_value(entry_string):
            """
            Get the float value out of entry strings
            (function to handle corner cases)
            """
            if entry_string in ['', '.', '+.', '-.', '+', '-']:
                return 0.0
            return float(entry_string)

        extracted_rules = []
        for entry in self.entries:
            if self.radio_angle_var.get():  # if true, means radians, extract as is
                ent_angle = get_float_value(entry["ent_angle"].get())
            else:
                ent_angle = get_float_value(
                    entry["ent_angle"].get()) * RAD_FAC  # convert degree to radians
            ent_angle = ent_angle % (2 * PI)
            ent_len = get_float_value(entry["ent_len"].get())
            is_reversed = entry["reverse_state"].get()
            is_flipped = entry["flip_state"].get()
            if ent_angle or ent_len or is_reversed or is_flipped:
                # user entered something, otherwise nothing changed
                extracted_rules.append((
                    ent_angle, ent_len, is_flipped, is_reversed))
        return extracted_rules

    def fill_entries_from_rules(self, rules):
        """
        Fill in the entries in GUI for user feedback
        """
        for rule in rules:
            angle, length, is_flipped, is_reversed = rule
            new_entry = self.create_entry_dictionary()
            # clear and insert angle
            new_entry['ent_angle'].delete(0, END)
            if self.radio_angle_var.get():  # if angle in radians
                new_entry['ent_angle'].insert(0, str(angle))
            else:
                new_entry['ent_angle'].insert(0, str(angle * DEG_FAC))
            # clear and insert length
            new_entry['ent_len'].delete(0, END)
            new_entry['ent_len'].insert(0, str(length))
            # set booleans
            new_entry['reverse_state'].set(is_reversed)
            new_entry['flip_state'].set(is_flipped)

            self.entries.append(new_entry)

#     def init_extract_rules_button(self):
#         """
#         Test button to check extracted rules
#         """
#         def print_extracted():
#             """
#             Print the extracted rules to stdout
#             """
#             print("Extracted:")
#             print(self.extract_rules())
#
#         self.test_button = Button(
#             self.frame, text="extract", command=print_extracted)
#         self.test_button.pack()

    def init_preview_canvas(self):
        """
        Canvas to draw the base curve from rules and give
        preview to the user
        """
        self.preview_canvas = Canvas(
            self.frame, width=200, height=200)
        self.preview_canvas.grid(row=0, columnspan=4, sticky=W)

    def form_base_curve(self, rules):
        """
        Form the base curve from extracted rules for previewing
        Resized to fit into the preview canvas
        """
        curve = [(0, 0)]
        for theta, scale_fac, _, _ in rules:
            last_x, last_y = curve[-1]
            curve.append((
                last_x + scale_fac * cos(theta),
                last_y + scale_fac * sin(theta)))

        min_x = min(point[0] for point in curve)
        min_y = min(point[1] for point in curve)
        scale_y = max(point[1] - min_y for point in curve)
        scale_x = max(point[0] - min_x for point in curve)
        if scale_x == 0 or scale_y == 0:
            return curve
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        to_scale = min(canvas_width / scale_x, canvas_height / scale_y) * 0.9
        curve = [
            ((point[0] - min_x) * to_scale + canvas_width / 10,
             (point[1] - min_y) * to_scale + canvas_height / 10)
            for point in curve]
        return curve

    def render_preview(self):
        """
        Render the preview on canvas on calling the function
        Desired to be called by some update function
        """
        # Not the best way to do it but the curve size is of constant
        # order, <20 segments, so it wouldnt create much difference
        curve = self.form_base_curve(self.extract_rules())
        self.preview_canvas.delete("all")
        if len(curve) > 1:  # draw only if there are more than one points
            self.preview_canvas.create_line(curve)

    def init_info_labels(self):
        """
        Initialize the labels providing info about input fields
        """
        Radiobutton(
            self.frame, variable=self.radio_angle_var,
            value=False, text="Degrees").grid(row=1, column=0)
        Radiobutton(
            self.frame, variable=self.radio_angle_var,
            value=True, text="Radians").grid(row=1, column=1)
        Label(
            self.frame, text="Angle").grid(row=2, column=0, sticky=W)
        Label(
            self.frame, text="Length").grid(row=2, column=1, sticky=W)


if __name__ == "__main__":
    WINDOW = Tk()
    FRAME = Frame(WINDOW)
    FRAME.pack()
    RULES_INPUT = RulesInput(FRAME)
    WINDOW.mainloop()
