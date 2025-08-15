#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter import ttk


class RoutineEditor(tk.Toplevel):
    wo_exercises: dict[tk.Frame, list[tk.Entry]] = {}

    def __init__(self, root: tk.Tk | tk.Toplevel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._root = root
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        menu = tk.Menu(self)
        menu.add_command(label="Show grid_size()", command=self.show_grid_size)
        self["menu"] = menu
        self.topframe: tk.Frame = tk.Frame(self)
        # topframe = self.topframe
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # topframe.grid(row=0, column=0, sticky=tk.NSEW)
        # ts_frame = tk.Frame(topframe)
        ts_frame = tk.Frame(self)
        ts_frame.grid(row=0, column=0, sticky=tk.W)
        tk.Label(ts_frame, text="When: ").grid(row=0, column=0)
        tk.Entry(ts_frame).grid(row=0, column=1)
        # ex_frame: tk.Frame = tk.Frame(topframe)
        ex_frame: tk.Frame = tk.Frame(self)
        self.ex_frame = ex_frame
        # topframe.rowconfigure(1, weight=1)
        ex_frame.rowconfigure(1, weight=1)
        ex_frame.grid(row=1, column=0, sticky=tk.EW)
        # btn_frame: tk.Frame = tk.Frame(topframe)
        btn_frame: tk.Frame = tk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        tk.Button(
            btn_frame, text="Add exercise", command=lambda: self.add_exercise(ex_frame)
        ).grid(row=0, column=0)
        tk.Button(btn_frame, text="Save workout").grid(row=0, column=1)
        # self.add_exercise(ex_frame)

    def show_grid_size(self):
        # print(self.ex_frame.grid_size())
        print(self.topframe.grid_size())

    def _on_closing(self):
        if self._root:
            self._root.destroy()

    def remove_exercise(self, ex_frame: tk.Frame) -> None:
        if ex_frame in self.wo_exercises:
            ex_frame.destroy()
            del self.wo_exercises[ex_frame]
            self.update_idletasks()

    def add_exercise(self, ex_box: tk.Frame) -> None:
        wo_set: list[tk.Entry] = []

        ex_frame: tk.Frame = tk.Frame(ex_box)
        ex_frame.grid(column=0, sticky=tk.EW)  # NOTE! row= not set increments row
        ttk.Combobox(ex_frame, values=["squat", "bench press", "deadlift"]).grid(
            row=0, column=0, sticky=tk.W
        )
        weight = tk.Entry(ex_frame, width=5)
        wo_set.append(weight)
        weight.grid(row=0, column=1, sticky=tk.W)
        reps = tk.Entry(ex_frame, width=3)
        wo_set.append(reps)
        self.wo_exercises[ex_frame] = wo_set
        reps.grid(row=0, column=2, sticky=tk.W)
        del_btn = tk.Button(
            ex_frame, text="Delete", command=lambda: self.remove_exercise(ex_frame)
        )
        del_btn.grid(row=0, column=3, sticky=tk.W)
        self.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    RoutineEditor(root).mainloop()
