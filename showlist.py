#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
import tkinter.simpledialog


class ShowList(tkinter.simpledialog.Dialog):
    def __init__(self, *args, items: list[str] = [], **kwargs) -> None:
        self.parent = kwargs.get("parent", None)
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
            print(f"Selected: {value}")
            # ShowWorkout(self.parent, get_workout(value))
