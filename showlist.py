#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog
import model as MD


class ShowWorkout(tkinter.simpledialog.Dialog):
    def __init__(self, *args, workout: MD.Workout, **kwargs):
        self.routine_editor = args[0].parent
        # To avoid importing start_routine.RoutineEditor
        assert self.routine_editor.__class__.__name__ == "RoutineEditor"

        self.workout = workout
        super().__init__(*args, **kwargs)

    def body(self, master) -> tk.Widget:
        # self._make_var = MethodType(_make_var, self)
        box = tk.Frame(master)
        row: int = 0
        box.grid()
        for text, var_type in zip(
            ("id", "name", "started"), (tk.IntVar, tk.StringVar, tk.StringVar)
        ):
            row += 1
            tk.Label(box, text=f"{text}: ").grid(row=row, column=0, sticky=tk.W)
            var = var_type(value=getattr(self.workout, text))
            tk.Entry(box, textvariable=var).grid(row=row, column=1)

        row += 1
        ttk.Separator(box, orient=tk.HORIZONTAL).grid(
            row=row, columnspan=4, sticky=tk.EW, pady=5
        )
        row += 1
        add_exercise = self.routine_editor.add_exercise
        for row, ex in enumerate(self.workout.exercises, row):
            add_exercise(box, init=ex)
        return box


class ShowList(tkinter.simpledialog.Dialog):
    def __init__(self, *args, items: list[str] = [], **kwargs) -> None:
        self.parent = kwargs.get("parent", None)
        assert (
            self.parent.__class__.__name__ == "RoutineEditor"
        ), "ShowList parent must be RoutineEditor"
        self.items = items
        super().__init__(*args, **kwargs)

    def body(self, master) -> tk.Widget:
        listbox: tk.Listbox = tk.Listbox(
            master, height=len(self.items), selectmode=tk.SINGLE
        )
        listbox.bind("<<ListboxSelect>>", self.on_select)
        for index, item in enumerate(self.items, 1):
            listbox.insert(index, item)
        listbox.grid()
        return listbox

    def on_select(self, event: tk.Event) -> None:
        """Show the selected item in the console."""
        listbox: tk.Listbox = event.widget
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            value = listbox.get(index)
            ShowWorkout(
                self,
                workout=self.parent.session.query(MD.Workout)
                .filter_by(name=value)
                .first(),
            )
