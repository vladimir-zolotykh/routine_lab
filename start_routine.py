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
        topframe: tk.Frame = tk.Frame(self)
        self.columnconfigure(0, weight=1)
        topframe.grid(row=0, column=0, sticky=tk.NSEW)
        ts_frame = tk.Frame(topframe)
        ts_frame.grid(row=0, column=0, sticky=tk.W)
        tk.Label(ts_frame, text="When: ").grid(row=0, column=0)
        tk.Entry(ts_frame).grid(row=0, column=1)
        ex_frame: tk.Frame = tk.Frame(topframe)
        topframe.rowconfigure(1, weight=1)
        ex_frame.grid(row=1, column=0, sticky=tk.EW)
        btn_frame: tk.Frame = tk.Frame(topframe)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        tk.Button(btn_frame, text="Add exercise").grid(row=0, column=0)
        tk.Button(btn_frame, text="Save workout").grid(row=0, column=1)
        self.add_exercise(ex_frame)

    def _on_closing(self):
        if self._root:
            self._root.destroy()

    def remove_exerecise(self, ex_frame: tk.Frame) -> None:
        if ex_frame in self.wo_exercises:
            del self.wo_exercises[ex_frame]

    def add_exercise(self, ex_box: tk.Frame, start_row: int = 1) -> None:
        wo_set: list[tk.Entry] = []

        ex_frame: tk.Frame = tk.Frame(ex_box)
        ex_frame.grid(row=start_row, column=0, sticky=tk.EW)
        ttk.Combobox(ex_frame).grid(row=0, column=0, sticky=tk.W)
        weight = tk.Entry(ex_frame)
        wo_set.append(weight)
        weight.grid(row=0, column=1, sticky=tk.W)
        reps = tk.Entry(ex_frame)
        wo_set.append(reps)
        self.wo_exercises[ex_frame] = wo_set
        reps.grid(row=0, column=2, sticky=tk.W)
        del_btn = tk.Button(
            ex_frame, text="Delete", command=lambda: self.remove_exerecise(ex_frame)
        )
        del_btn.grid(row=0, column=3, sticky=tk.W)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    RoutineEditor(root).mainloop()
