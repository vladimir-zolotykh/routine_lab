#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk


class RoutineEditor(tk.Toplevel):
    def __init__(self, root: tk.Tk | tk.Toplevel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._root = root
        topframe: tk.Frame = tk.Frame(self)
        self.columnconfigure(0, weight=1)
        topframe.grid(row=0, column=0, sticky=tk.NSEW)
        tk.Entry(topframe).grid(row=0, column=0)
        ex_frame: tk.Frame = tk.Frame(topframe)
        topframe.rowconfigure(1, weight=1)
        ex_frame.grid(row=1, column=1, sticky=tk.EW)
        self.add_exercise(ex_frame)
        btn_frame: tk.Frame = tk.Frame(topframe)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        tk.Button(btn_frame, text="Add exercise").grid(row=0, column=0)
        tk.Button(btn_frame, text="Save workout").grid(row=0, column=1)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        if self._root:
            self._root.destroy()

    def add_exercise(self, ex_box):
        pass
        # print(self.nametowidget(tk._default_root))


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    RoutineEditor(root).mainloop()
