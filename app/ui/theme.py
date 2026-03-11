import tkinter as tk
from tkinter import font, ttk

from app.constants import COLORS


def setup_fonts(root: tk.Tk) -> dict[str, font.Font]:  # noqa: ARG001
    return {
        "title": font.Font(family="Segoe UI", size=14, weight="bold"),
        "header": font.Font(family="Segoe UI", size=12, weight="bold"),
        "text": font.Font(family="Segoe UI", size=10),
        "small": font.Font(family="Segoe UI", size=8),
    }


def setup_styles(style: ttk.Style, fonts: dict) -> None:
    style.theme_use("clam")
    style.configure("TFrame", background=COLORS["background"])
    style.configure(
        "TLabelframe",
        background=COLORS["panel"],
        foreground=COLORS["foreground"],
    )
    style.configure(
        "TLabelframe.Label",
        background=COLORS["panel"],
        foreground=COLORS["foreground"],
        font=fonts["header"],
    )
    style.configure(
        "TButton",
        background=COLORS["accent1"],
        foreground=COLORS["foreground"],
        font=fonts["text"],
    )
