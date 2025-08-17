#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter import ttk


class TestCombo(tk.Tk):
    ex_names = [
        "front squat",
        "squat",
        "bench press",
        "deadlift",
        "pullup",
        "overhead press",
        "biceps curl",
    ]

    def __init__(self):
        super().__init__()
        menu = tk.Menu(self)
        self["menu"] = menu
        self.box = tk.Frame(self)
        self.box.grid()
        name_var = tk.StringVar(value="front squat")
        menu.add_command(label="Print name_var", command=lambda: print(name_var.get()))
        menu.add_command(label="Add Combobox", command=self.add_combobox)
        cb = ttk.Combobox(self.box, textvariable=name_var, values=self.ex_names)
        cb.grid()

    def add_combobox(self):
        name_var = tk.StringVar(value=self.ex_names[0])
        cb = ttk.Combobox(self.box, textvariable=name_var, values=self.ex_names)
        cb.grid()


if __name__ == "__main__":
    TestCombo().mainloop()
