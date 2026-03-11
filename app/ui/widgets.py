"""Reusable styled widget factory functions."""
import tkinter as tk
from tkinter import ttk
from typing import Callable


# ─────────────────────────────────────────── color helpers ──────────────────

def lighten_color(hex_color: str, factor: float = 0.18) -> str:
    r, g, b = _parse_hex(hex_color)
    return _to_hex(
        min(255, int(r + (255 - r) * factor)),
        min(255, int(g + (255 - g) * factor)),
        min(255, int(b + (255 - b) * factor)),
    )


def darken_color(hex_color: str, factor: float = 0.18) -> str:
    r, g, b = _parse_hex(hex_color)
    return _to_hex(
        max(0, int(r * (1 - factor))),
        max(0, int(g * (1 - factor))),
        max(0, int(b * (1 - factor))),
    )


# ─────────────────────────────────────────── canvas helpers ─────────────────

def _create_rounded_rect(
    canvas: tk.Canvas, x: int, y: int, w: int, h: int, r: int, **kw
) -> int:
    """Draw a smooth rounded rectangle on a Canvas, return item id."""
    pts = [
        x + r, y,       x + w - r, y,
        x + w, y,       x + w, y + r,
        x + w, y + h - r, x + w, y + h,
        x + w - r, y + h, x + r, y + h,
        x, y + h,       x, y + h - r,
        x, y + r,       x, y,
        x + r, y,
    ]
    return canvas.create_polygon(pts, smooth=True, **kw)


# ──────────────────────────────────────── RoundedButton ─────────────────────

class RoundedButton(tk.Canvas):
    """Canvas-based button with rounded corners and hover effect."""

    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        command: Callable,
        bg_color: str,
        fg_color: str,
        parent_bg: str,
        fonts: dict,
        width: int = 160,
        height: int = 46,
        radius: int = 10,
    ) -> None:
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent_bg,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self._command = command
        self._bg = bg_color
        self._hover_bg = lighten_color(bg_color, 0.22)

        self._rect = _create_rounded_rect(
            self, 0, 0, width, height, radius,
            fill=bg_color, outline="",
        )
        self._label = self.create_text(
            width // 2, height // 2,
            text=text,
            font=fonts["button"],
            fill=fg_color,
        )

        # ── Fix: only bind Button-1 at canvas level to avoid double-firing ──
        for item in (self._rect, self._label):
            self.tag_bind(item, "<Enter>", self._on_enter)
            self.tag_bind(item, "<Leave>", self._on_leave)

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>",    self._on_enter)
        self.bind("<Leave>",    self._on_leave)

    def set_text(self, text: str) -> None:
        self.itemconfig(self._label, text=text)

    def _on_click(self, _: tk.Event) -> None:
        self._command()

    def _on_enter(self, _: tk.Event) -> None:
        self.itemconfig(self._rect, fill=self._hover_bg)

    def _on_leave(self, _: tk.Event) -> None:
        self.itemconfig(self._rect, fill=self._bg)


# ──────────────────────────────────────── factories ─────────────────────────

def styled_button(
    parent: tk.Widget,
    text: str,
    command: Callable,
    row: int,
    col: int,
    colors: dict,
    fonts: dict,
    color: str | None = None,
    parent_bg: str | None = None,
    width: int = 160,
    height: int = 46,
) -> RoundedButton:
    bg = color or colors["accent1"]
    pbg = parent_bg or colors["panel"]
    btn = RoundedButton(parent, text, command, bg, colors["foreground"],
                        pbg, fonts, width=width, height=height)
    btn.grid(row=row, column=col, padx=6, pady=5, sticky="ew")
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
    frame = tk.Frame(parent, bg=colors["panel"])
    frame.grid(row=row, column=col, columnspan=colspan,
               sticky="ew", pady=(16, 4), padx=2)

    tk.Frame(frame, bg=colors["accent2"], width=4).pack(
        side=tk.LEFT, fill=tk.Y, padx=(0, 10)
    )
    tk.Label(
        frame, text=text, font=fonts["header"],
        fg=colors["foreground"], bg=colors["panel"], pady=4,
    ).pack(side=tk.LEFT, anchor="w")


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
    frame = tk.Frame(parent, bg=colors["panel"])
    frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", pady=2)
    frame.columnconfigure(1, weight=1)

    tk.Label(frame, text=text, font=fonts["text"],
             fg=colors["muted"], bg=colors["panel"], anchor="w",
             ).grid(row=0, column=0, padx=5, pady=2, sticky="w")

    entry = tk.Entry(frame, textvariable=variable, font=fonts["text"],
                     bg=colors["input"], fg=colors["foreground"],
                     insertbackground=colors["foreground"],
                     relief=tk.FLAT, bd=0, highlightthickness=1,
                     highlightbackground=colors["border"],
                     highlightcolor=colors["accent2"])
    entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew", ipady=4)
    return entry


def player_card(
    parent: tk.Widget,
    role: str,
    tag_color: str,
    name_var: tk.StringVar,
    balance_var: tk.DoubleVar,
    col: int,
    colors: dict,
    fonts: dict,
    on_change: Callable,
) -> None:
    """Card with avatar circle, role tag, large balance (red if negative), editable fields."""
    card_bg = colors.get("card", colors["panel"])

    card = tk.Frame(
        parent, bg=card_bg,
        highlightthickness=1, highlightbackground=tag_color,
        padx=12, pady=10,
    )
    card.grid(row=0, column=col, padx=5, pady=4, sticky="nsew")
    card.columnconfigure(0, weight=1)

    # Colored top stripe (thicker)
    tk.Frame(card, bg=tag_color, height=4).grid(
        row=0, column=0, sticky="ew", pady=(0, 10)
    )

    # Avatar + role row
    top_row = tk.Frame(card, bg=card_bg)
    top_row.grid(row=1, column=0, sticky="w", pady=(0, 6))

    av = tk.Canvas(top_row, width=40, height=40, bg=card_bg, highlightthickness=0)
    av.pack(side=tk.LEFT, padx=(0, 10))
    av.create_oval(2, 2, 38, 38, fill=tag_color, outline="")
    av.create_text(20, 20, text=role[0], font=fonts["header"], fill=colors.get("panel", "#13132A"))

    tk.Label(
        top_row, text=role, font=fonts["tag"],
        fg=tag_color, bg=card_bg,
    ).pack(side=tk.LEFT, anchor="s", pady=(0, 3))

    # Balance display — large, red when negative
    bal_label = tk.Label(
        card, text=_fmt(balance_var.get()),
        font=fonts["balance"], fg=tag_color, bg=card_bg,
    )
    bal_label.grid(row=2, column=0, sticky="w", pady=(0, 12))

    # Name field
    tk.Label(card, text="Nombre", font=fonts["small"],
             fg=colors["muted"], bg=card_bg,
             ).grid(row=3, column=0, sticky="w")
    tk.Entry(card, textvariable=name_var, font=fonts["text"],
             bg=colors["input"], fg=colors["foreground"],
             insertbackground=colors["foreground"],
             relief=tk.FLAT, bd=0,
             highlightthickness=1, highlightbackground=colors["border"],
             highlightcolor=tag_color,
             ).grid(row=4, column=0, sticky="ew", ipady=5, pady=(2, 10))

    # Balance field
    tk.Label(card, text="Saldo", font=fonts["small"],
             fg=colors["muted"], bg=card_bg,
             ).grid(row=5, column=0, sticky="w")
    tk.Entry(card, textvariable=balance_var, font=fonts["text"],
             bg=colors["input"], fg=colors["foreground"],
             insertbackground=colors["foreground"],
             relief=tk.FLAT, bd=0,
             highlightthickness=1, highlightbackground=colors["border"],
             highlightcolor=tag_color,
             ).grid(row=6, column=0, sticky="ew", ipady=5, pady=(2, 0))

    def _update_label(*_) -> None:
        try:
            val = balance_var.get()
            color = colors.get("danger", colors["accent1"]) if val < 0 else tag_color
            bal_label.config(text=_fmt(val), fg=color)
        except tk.TclError:
            pass

    balance_var.trace_add("write", _update_label)
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
    frame = tk.Frame(parent, bg=colors["panel"])
    frame.grid(row=row, column=col, padx=10, pady=8, sticky="w")
    cb = tk.Checkbutton(
        frame, text=text, variable=variable, command=command,
        font=fonts["text"],
        fg=colors["foreground"], bg=colors["panel"],
        activebackground=colors["panel"],
        activeforeground=colors["accent2"],
        selectcolor=colors["input"],
        cursor="hand2",
    )
    cb.pack(anchor="w")
    return cb


# ─────────────────────────────────────────── private ────────────────────────

def _fmt(value: float) -> str:
    return f"{value:,.1f}"


def _parse_hex(hex_color: str) -> tuple[int, int, int]:
    return int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)


def _to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"
