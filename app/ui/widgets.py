"""Reusable styled widget factory functions."""
import tkinter as tk
from tkinter import ttk
from typing import Callable


def lighten_color(hex_color: str, factor: float = 0.2) -> str:
    r, g, b = _parse_hex(hex_color)
    return _to_hex(
        min(255, int(r + (255 - r) * factor)),
        min(255, int(g + (255 - g) * factor)),
        min(255, int(b + (255 - b) * factor)),
    )


def darken_color(hex_color: str, factor: float = 0.2) -> str:
    r, g, b = _parse_hex(hex_color)
    return _to_hex(
        max(0, int(r * (1 - factor))),
        max(0, int(g * (1 - factor))),
        max(0, int(b * (1 - factor))),
    )


def styled_button(
    parent: tk.Widget,
    text: str,
    command: Callable,
    row: int,
    col: int,
    colors: dict,
    fonts: dict,
    color: str | None = None,
) -> tk.Button:
    bg = color or colors["accent1"]
    btn = tk.Button(
        parent, text=text, command=command, font=fonts["text"],
        bg=bg, fg=colors["foreground"],
        activebackground=darken_color(bg),
        activeforeground=colors["foreground"],
        relief=tk.FLAT, borderwidth=0, padx=15, pady=8,
    )
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
    btn.bind("<Enter>", lambda _, b=btn, c=bg: b.config(bg=lighten_color(c)))
    btn.bind("<Leave>", lambda _, b=btn, c=bg: b.config(bg=c))
    return btn


def section_title(
    parent: tk.Widget,
    text: str,
    row: int,
    col: int,
    colors: dict,
    fonts: dict,
    colspan: int = 1,
) -> None:
    tk.Label(
        parent, text=text, font=fonts["header"],
        fg=colors["accent2"], bg=colors["panel"], pady=5,
    ).grid(row=row, column=col, columnspan=colspan, sticky="w")


def label_entry(
    parent: tk.Widget,
    text: str,
    variable: tk.Variable,
    row: int,
    col: int,
    colors: dict,
    fonts: dict,
    colspan: int = 1,
) -> tk.Entry:
    frame = ttk.Frame(parent)
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", pady=2)
    frame.columnconfigure(1, weight=1)

    tk.Label(frame, text=text, font=fonts["text"],
             fg=colors["foreground"], bg=colors["panel"], anchor="w",
             ).grid(row=0, column=0, padx=5, pady=2, sticky="w")

    entry = tk.Entry(frame, textvariable=variable, font=fonts["text"],
                     bg=colors["input"], fg=colors["foreground"],
                     insertbackground=colors["foreground"],
                     relief=tk.FLAT, bd=2)
    entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
    return entry


def player_row(
    parent: tk.Widget,
    tag: str,
    name_var: tk.StringVar,
    balance_var: tk.DoubleVar,
    row: int,
    colors: dict,
    fonts: dict,
    on_change: Callable,
) -> None:
    frame = ttk.Frame(parent)
    frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=2)
    frame.columnconfigure(1, weight=2)
    frame.columnconfigure(3, weight=3)

    tk.Label(frame, text=tag, font=fonts["text"],
             fg=colors["accent3"], bg=colors["panel"], anchor="w",
             ).grid(row=0, column=0, padx=(5, 2), pady=2, sticky="w")

    tk.Entry(frame, textvariable=name_var, font=fonts["text"],
             bg=colors["input"], fg=colors["foreground"],
             insertbackground=colors["foreground"],
             relief=tk.FLAT, bd=2, width=12,
             ).grid(row=0, column=1, padx=(0, 10), pady=2, sticky="ew")

    tk.Label(frame, text="Saldo:", font=fonts["text"],
             fg=colors["foreground"], bg=colors["panel"], anchor="w",
             ).grid(row=0, column=2, padx=(5, 2), pady=2, sticky="w")

    tk.Entry(frame, textvariable=balance_var, font=fonts["text"],
             bg=colors["input"], fg=colors["foreground"],
             insertbackground=colors["foreground"],
             relief=tk.FLAT, bd=2,
             ).grid(row=0, column=3, padx=5, pady=2, sticky="ew")

    balance_var.trace_add("write", on_change)
    name_var.trace_add("write", on_change)


def styled_checkbox(
    parent: tk.Widget,
    text: str,
    variable: tk.BooleanVar,
    row: int,
    col: int,
    colors: dict,
    fonts: dict,
    command: Callable,
) -> tk.Checkbutton:
    frame = ttk.Frame(parent)
    frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")
    cb = tk.Checkbutton(
        frame, text=text, variable=variable, command=command,
        font=fonts["text"], fg=colors["foreground"], bg=colors["panel"],
        activebackground=colors["panel"], activeforeground=colors["accent2"],
        selectcolor=colors["panel"],
    )
    cb.pack(anchor="w")
    return cb


# --- helpers ---

def _parse_hex(hex_color: str) -> tuple[int, int, int]:
    return int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)


def _to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"
