#!/usr/bin/env python3

from tkinter import Tk, Frame, Label, Button, BOTH
import setup as st


"""
This module is to display User or Driver information.

Place:      University of Bedfordshire
Author:     Oszkar Feher
Date:       21 October 2020
"""


class InfoScreen(Tk):
    """InfoScreen class to display User or Driver information.
    :inherit: - Tk from tkinter."""

    def __init__(self, main, query, fields):
        """Constructor"""
        # Call of constructor of parent class Tk.
        Tk.__init__(self)
        self.query = query
        self.main = main
        self.fields = fields
        self.build_screen()

    def build_screen(self):
        """Builds another window to display information."""
        # Frame
        frame = Frame(self, **st.mini_frame)
        # Size of window
        x, y = 500, 650
        # Position of the window
        self.geometry(
            "{}x{}+{}+{}".format(x, y,
                                 int(self.main.winfo_screenwidth() // 2 - x // 2),
                                 int(self.main.winfo_screenheight() // 2 - y // 2)))
        self.overrideredirect(True)
        self.update_idletasks()
        frame.pack(fill=BOTH, expand=True)
        str_, text = "{}:{}{}\n\n", ""
        for value in zip(self.fields, *self.query):
            text += str_.format(value[0], " " * (16 - len(value[0])), value[1])
        label = Label(frame, text=text, **st.mini_label)
        # Command - destroys window by pressing Ok
        ok = Button(self, text="Ok", command=lambda: self.destroy(), **st.mini_button)
        label.pack(fill=BOTH, expand=True)
        ok.place(relx=0.5, rely=0.96, anchor='s')
