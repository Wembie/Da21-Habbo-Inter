import tkinter as tk
from tkinter import font, ttk

from app.constants import COLORS


def setup_fonts(root: tk.Tk) -> dict[str, font.Font]:  # noqa: ARG001
    return {
        "title":   font.Font(family="Segoe UI", size=20, weight="bold"),
        "header":  font.Font(family="Segoe UI", size=12, weight="bold"),
        "text":    font.Font(family="Segoe UI", size=10),
        "small":   font.Font(family="Segoe UI", size=9),
        "balance": font.Font(family="Segoe UI", size=24, weight="bold"),
        "button":  font.Font(family="Segoe UI", size=11, weight="bold"),
        "tag":     font.Font(family="Segoe UI", size=13, weight="bold"),
        "amount":  font.Font(family="Segoe UI", size=30, weight="bold"),
        "mono":    font.Font(family="Consolas",  size=9),
    }


def setup_styles(style: ttk.Style, fonts: dict) -> None:
    style.theme_use("clam")

    style.configure("TFrame",
                    background=COLORS["background"])

    style.configure("Panel.TFrame",
                    background=COLORS["panel"])

    style.configure("TLabelframe",
                    background=COLORS["panel"],
                    foreground=COLORS["foreground"],
                    bordercolor=COLORS["border"],
                    relief="flat",
                    borderwidth=1)

    style.configure("TLabelframe.Label",
                    background=COLORS["panel"],
                    foreground=COLORS["muted"],
                    font=fonts["header"])

    style.configure("TButton",
                    background=COLORS["accent1"],
                    foreground=COLORS["foreground"],
                    font=fonts["button"])

    style.configure("TCombobox",
                    fieldbackground=COLORS["input"],
                    background=COLORS["panel"],
                    foreground=COLORS["foreground"],
                    selectbackground=COLORS["accent2"],
                    selectforeground=COLORS["foreground"],
                    arrowcolor=COLORS["muted"])

    style.map("TCombobox",
              fieldbackground=[("readonly", COLORS["input"])],
              foreground=[("readonly", COLORS["foreground"])],
              selectbackground=[("readonly", COLORS["highlight"])])

    style.configure("Vertical.TScrollbar",
                    background=COLORS["panel"],
                    troughcolor=COLORS["input"],
                    arrowcolor=COLORS["muted"],
                    bordercolor=COLORS["border"])
