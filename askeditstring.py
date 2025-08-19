#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter.simpledialog import _QueryDialog


class QueryEditString(_QueryDialog):
    def __init__(self, *args, **kw):
        self.default_str = ""
        if "default_str" in kw:
            self.default_str = kw["default_str"]
            del kw["default_str"]
        super().__init__(*args, **kw)

    def body(self, master):
        entry = super().body(master)
        self.default_str_var = tk.StringVar(value=self.default_str)
        entry.configure(textvariable=self.default_str_var)
        return entry

    def getresult(self):
        return self.default_str_var.get()


def askeditstring(title, prompt, **kw):
    """get a string from the user

    Arguments:

        title       -- the dialog title
        prompt      -- the label text
        default_str -- initial Entry widget value
        **kw        -- see SimpleDialog class

    Return value is a string
    """
    d = QueryEditString(title, prompt, **kw)
    return d.result
