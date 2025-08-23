#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
import tkinter.simpledialog
import model as MD


class ShowWorkout(tkinter.simpledialog.Dialog):
    def __init__(self, *args, workout: MD.Workout, **kwargs):
        self.workout = workout
        super().__init__(*args, **kwargs)

    def body(self, master) -> tk.Widget:
        text = tk.Text(master)
        text.grid()
        text.insert(tk.END, f"id: {str(self.workout.id)}\n")
        text.insert(tk.END, f"name: {self.workout.name}\n")
        text.insert(tk.END, f"started: {self.workout.started.strftime('%y-%m-%d')}\n")
        for ex_row, ex in enumerate(self.workout.exercises):
            ex: str = ", ".join(
                map(str, [str(ex.id), ex.exercise_name.name, ex.weight, ex.reps])
            )
            text.insert(tk.END, "    " + ex + "\n")
        return text


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
