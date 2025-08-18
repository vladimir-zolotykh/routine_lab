#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import itertools
import tkinter as tk
import tkinter.simpledialog


def get_size(text: str) -> tuple[int, int]:
    it1: Iterator[str]
    it2: Iterator[str]
    it1, it2 = itertools.tee(text.split("\n"))
    return len(max(it1, key=len)), sum(1 for _ in it2)


class ShowText(tkinter.simpledialog.Dialog):
    def __init__(self, *args, message="", **kwargs):
        self.message = message
        super().__init__(*args, **kwargs)

    def body(self, master) -> tk.Widget:
        w, h = get_size(self.message)
        text = tk.Text(master, width=w, height=h)
        text.grid()
        text.insert(tk.END, self.message)
        return text
