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
        self.geometry("431x174+60+164")
        menu = tk.Menu(self)
        self["menu"] = menu
        self.box = tk.Frame(self)
        self.box.grid()
        name_var = tk.StringVar(value="front squat")
        menu.add_command(label="Print name_var", command=lambda: print(name_var.get()))
        menu.add_command(label="Add Combobox", command=self.add_combobox)
        menu.add_command(
            label="Print 'str_var_' attributes", command=self._print_str_var
        )
        cb = ttk.Combobox(self.box, textvariable=name_var, values=self.ex_names)
        cb.grid()

        self.str_num: int = 1
        self.str_var_dict: dict[str, tk.StringVar] = {}

    def _print_str_var(self):
        print(f"{self.str_var_dict = }")

    def _make_var(self, value: str, prefix: str = "str_var_") -> tk.StringVar:
        var_name = prefix + str(self.str_num)
        self.str_num += 1
        var = tk.StringVar(value=value)
        setattr(self, var_name, var)
        self.str_var_dict[var_name] = var
        return var

    def add_combobox(self):
        cb = ttk.Combobox(
            self.box,
            textvariable=self._make_var(self.ex_names[0]),
            values=self.ex_names,
        )
        cb.grid()


if __name__ == "__main__":
    TestCombo().mainloop()
