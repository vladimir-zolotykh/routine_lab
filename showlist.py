#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
import tkinter.simpledialog


class ShowList(tkinter.simpledialog.Dialog):
    def __init__(self, *args, items: list[str] = [], **kwargs) -> None:
        self.items = items
        super().__init__(*args, **kwargs)

    def body(self, master) -> tk.Widget:
        listbox: tk.Listbox = tk.Listbox(master, height=len(self.items))
        for index, item in enumerate(self.items, 1):
            listbox.insert(index, item)
        listbox.grid()
        return listbox
