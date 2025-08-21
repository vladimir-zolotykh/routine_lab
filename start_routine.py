#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import contextlib
import io
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from sqlalchemy import (
    Engine,
    create_engine,
)
from sqlalchemy.orm import Session, sessionmaker
import argparse
import argcomplete
from types import MethodType
import model as MD
import database as DB
from showtext import ShowText
from askeditstring import askeditstring


def _make_var(self, value: str, prefix: str = "str_var_") -> tk.StringVar:
    if not hasattr(self, "str_num"):
        setattr(self, "str_num", 1)
    var_name = prefix + str(self.str_num)
    self.str_num += 1
    var = tk.StringVar(value=value)
    setattr(self, var_name, var)
    return var


class RoutineEditor(tk.Toplevel):
    wo_exercises: dict[tk.Frame, tuple[tk.StringVar, tk.DoubleVar, tk.IntVar]] = {}

    def __init__(self, root: tk.Tk | tk.Toplevel, session: Session) -> None:
        super().__init__(root)
        menu = tk.Menu(self)
        self.session = session
        menu.add_command(label="Quit", command=self.quit)
        show_menu = tk.Menu(menu)
        show_menu.add_command(
            label="Show exercise names", command=self.show_exercise_names
        )
        menu.add_cascade(label="Show", menu=show_menu)
        self["menu"] = menu
        self._root = root
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.topframe: tk.Frame = tk.Frame(self)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        ts_frame = tk.Frame(self)
        ts_frame.grid(row=0, column=0, sticky=tk.W)
        tk.Label(ts_frame, text="When: ").grid(row=0, column=0)
        self.started_var = tk.StringVar(value=datetime.now().strftime("%y-%m-%d"))
        tk.Entry(ts_frame, textvariable=self.started_var).grid(row=0, column=1)
        ex_frame: tk.Frame = tk.Frame(self)
        self.ex_frame = ex_frame
        btn_frame: tk.Frame = tk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        tk.Button(
            btn_frame, text="Add exercise", command=lambda: self.add_exercise(ex_frame)
        ).grid(row=0, column=0)
        tk.Button(btn_frame, text="Save workout", command=self.save_workout).grid(
            row=0, column=1
        )
        self._make_var = MethodType(_make_var, self)

    def _on_closing(self):
        if self._root:
            self._root.destroy()

    def draft_wo_name(self, started: datetime, exercises: list[MD.Exercise]) -> str:
        return started.strftime("%y-%m-%d") + "-".join(
            ex.exercise_name.name for ex in exercises
        )

    def save_workout(self) -> None:
        try:
            wo: MD.Workout = MD.Workout(
                started=datetime.strptime(self.started_var.get(), "%y-%m-%d")
            )
            for _, (ex_name_var, weight_var, reps_var) in self.wo_exercises.items():
                ex_name_obj: MD.ExerciseName = MD.ensure_exercise(
                    self.session, ex_name_var.get()
                )
                ex: MD.Exercise = MD.Exercise(
                    exercise_name=ex_name_obj,
                    weight=weight_var.get(),
                    reps=reps_var.get(),
                )
                wo.exercises.append(ex)
                session.add(ex)
            self.session.add(wo)
            wo.name = askeditstring(
                os.path.basename(__file__),
                "Workout name? ",
                default_str=self.draft_wo_name(wo.started, wo.exercises),
                parent=self,
            )
            if wo.name is None:
                raise ValueError("Workout namining cancelled")
            session.commit()
        except Exception as e:
            self.session.rollback()
            if isinstance(e, ValueError):
                showinfo(
                    os.path.basename(__file__),
                    str(e),
                    parent=self,
                )
            else:
                raise

    def remove_exercise(self, ex_frame: tk.Frame) -> None:
        if ex_frame in self.wo_exercises:
            ex_frame.destroy()
            del self.wo_exercises[ex_frame]
            if not self.wo_exercises:
                self.ex_frame.grid_forget()
            self.update_idletasks()

    def show_exercise_names(self):
        with contextlib.redirect_stdout(io.StringIO()) as s:
            for ex_name in self.session.query(MD.ExerciseName).all():
                print(ex_name)
            ShowText(self, message=s.getvalue())

    def add_exercise(self, ex_box: tk.Frame) -> None:
        if not self.wo_exercises:
            self.ex_frame.rowconfigure(1, weight=1)
            self.ex_frame.grid(row=1, column=0, sticky=tk.EW)

        ex_frame: tk.Frame = tk.Frame(ex_box)
        ex_frame.grid(column=0, sticky=tk.EW)  # NOTE! row= not set increments row
        ex_names = [en.name for en in self.session.query(MD.ExerciseName).all()]
        ex_name_var = self._make_var(value=ex_names[0])
        cb = ttk.Combobox(ex_frame, textvariable=ex_name_var, values=ex_names)
        cb.grid(row=0, column=0, sticky=tk.W)

        weight_var = tk.DoubleVar(value=100.0)
        weight = tk.Entry(ex_frame, textvariable=weight_var, width=5)
        weight.grid(row=0, column=1, sticky=tk.W)
        reps_var = tk.IntVar(value=5)
        reps = tk.Entry(ex_frame, textvariable=reps_var, width=3)
        self.wo_exercises[ex_frame] = (ex_name_var, weight_var, reps_var)
        reps.grid(row=0, column=2, sticky=tk.W)
        del_btn = tk.Button(
            ex_frame, text="Delete", command=lambda: self.remove_exercise(ex_frame)
        )
        del_btn.grid(row=0, column=3, sticky=tk.W)
        self.update_idletasks()


parser = argparse.ArgumentParser(
    description="Workout editor", formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

if __name__ == "__main__":
    parser.add_argument("--db", help="Workout db", default="routine.db")
    parser.add_argument("--echo", help="Echo DB commands", action="store_true")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    engine: Engine
    engine = create_engine(f"sqlite+pysqlite:///{args.db}", echo=args.echo, future=True)
    root = tk.Tk()
    root.withdraw()
    # SessionLocal -- <class 'sqlalchemy.orm.session.sessionmaker'>
    MD.Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    with MD.Session(engine) as session:
        try:
            for ex_name in DB.exercise_names:
                MD.ensure_exercise(session, ex_name)
            session.commit()
        except Exception:
            session.rollback()
            raise
        re = RoutineEditor(root, session)
    re.geometry("+779+266")
    re.mainloop()
