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
        height: int = 36,
        radius: int = 8,
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

        # Only canvas-level Button-1 to avoid double-firing
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
    height: int = 36,
) -> RoundedButton:
    bg = color or colors["accent1"]
    pbg = parent_bg or colors["panel"]
    btn = RoundedButton(parent, text, command, bg, colors["foreground"],
                        pbg, fonts, width=width, height=height)
    btn.grid(row=row, column=col, padx=5, pady=4, sticky="ew")
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
               sticky="ew", pady=(8, 2), padx=2)

    tk.Frame(frame, bg=colors["accent2"], width=3).pack(
        side=tk.LEFT, fill=tk.Y, padx=(0, 8)
    )
    tk.Label(
        frame, text=text, font=fonts["header"],
        fg=colors["foreground"], bg=colors["panel"], pady=2,
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
             ).grid(row=0, column=0, padx=4, pady=1, sticky="w")

    entry = tk.Entry(frame, textvariable=variable, font=fonts["text"],
                     bg=colors["input"], fg=colors["foreground"],
                     insertbackground=colors["foreground"],
                     relief=tk.FLAT, bd=0, highlightthickness=1,
                     highlightbackground=colors["border"],
                     highlightcolor=colors["accent2"])
    entry.grid(row=0, column=1, padx=4, pady=1, sticky="ew", ipady=3)
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
    """Compact card: avatar circle, role, balance (red if negative), editable fields."""
    card_bg = colors.get("card", colors["panel"])

    card = tk.Frame(
        parent, bg=card_bg,
        highlightthickness=1, highlightbackground=tag_color,
        padx=8, pady=6,
    )
    card.grid(row=0, column=col, padx=4, pady=3, sticky="nsew")
    card.columnconfigure(0, weight=1)

    # Colored top stripe
    tk.Frame(card, bg=tag_color, height=3).grid(
        row=0, column=0, sticky="ew", pady=(0, 6)
    )

    # Avatar + role row
    top_row = tk.Frame(card, bg=card_bg)
    top_row.grid(row=1, column=0, sticky="w", pady=(0, 3))

    av = tk.Canvas(top_row, width=28, height=28, bg=card_bg, highlightthickness=0)
    av.pack(side=tk.LEFT, padx=(0, 7))
    av.create_oval(1, 1, 27, 27, fill=tag_color, outline="")
    av.create_text(14, 14, text=role[0], font=fonts["small"], fill=colors.get("panel", "#191930"))

    tk.Label(
        top_row, text=role, font=fonts["tag"],
        fg=tag_color, bg=card_bg,
    ).pack(side=tk.LEFT, anchor="s", pady=(0, 1))

    # Balance — large, red when negative
    bal_label = tk.Label(
        card, text=_fmt(balance_var.get()),
        font=fonts["balance"], fg=tag_color, bg=card_bg,
    )
    bal_label.grid(row=2, column=0, sticky="w", pady=(0, 6))

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
             ).grid(row=4, column=0, sticky="ew", ipady=3, pady=(1, 6))

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
             ).grid(row=6, column=0, sticky="ew", ipady=3, pady=(1, 0))

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
    frame.grid(row=row, column=col, padx=8, pady=5, sticky="w")
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

class SearchableCurrencyPicker(tk.Frame):
    """Button that shows the current currency and opens a live-search picker popup."""

    def __init__(
        self,
        parent: tk.Widget,
        variable: tk.StringVar,
        currencies: list[str],
        colors: dict,
        fonts: dict,
    ) -> None:
        super().__init__(parent, bg=colors["panel"])
        self._var = variable
        self._currencies = currencies
        self._colors = colors
        self._fonts = fonts
        self._enabled = False
        self._popup: tk.Toplevel | None = None
        self._close_bind_id: str = ""

        self._btn = tk.Button(
            self,
            textvariable=variable,
            font=fonts["text"],
            width=7,
            bg=colors["input"],
            fg=colors["muted"],
            activebackground=colors["card"],
            activeforeground=colors["foreground"],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=colors["border"],
            highlightcolor=colors["accent2"],
            command=self._toggle_picker,
        )
        self._btn.pack()

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled
        self._btn.config(
            fg=self._colors["foreground"] if enabled else self._colors["muted"],
            cursor="hand2" if enabled else "arrow",
        )
        if not enabled and self._popup and self._popup.winfo_exists():
            self._popup.destroy()
            self._popup = None

    def _toggle_picker(self) -> None:
        if not self._enabled:
            return
        if self._popup and self._popup.winfo_exists():
            self._popup.destroy()
            self._popup = None
            return
        self._open_picker()

    def _open_picker(self) -> None:
        root = self.winfo_toplevel()
        popup = tk.Toplevel(root)
        self._popup = popup
        popup.overrideredirect(True)
        popup.configure(bg=self._colors["border"])
        popup.lift()

        x = self._btn.winfo_rootx()
        y = self._btn.winfo_rooty() + self._btn.winfo_height() + 3
        popup.geometry(f"190x260+{x}+{y}")

        search_var = tk.StringVar()
        search_entry = tk.Entry(
            popup,
            textvariable=search_var,
            font=self._fonts["text"],
            bg=self._colors["input"],
            fg=self._colors["foreground"],
            insertbackground=self._colors["foreground"],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=self._colors["accent2"],
            highlightcolor=self._colors["accent2"],
        )
        search_entry.pack(fill=tk.X, padx=1, pady=(1, 0), ipady=5)
        search_entry.focus_set()

        lb_frame = tk.Frame(popup, bg=self._colors["border"])
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=(1, 1))

        lb = tk.Listbox(
            lb_frame,
            font=self._fonts["text"],
            bg=self._colors["input"],
            fg=self._colors["foreground"],
            selectbackground=self._colors["accent2"],
            selectforeground=self._colors["foreground"],
            activestyle="none",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
        )
        sb = ttk.Scrollbar(lb_frame, command=lb.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        lb.config(yscrollcommand=sb.set)
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        filtered: list[str] = []

        def _populate(items: list[str]) -> None:
            nonlocal filtered
            filtered = items
            lb.delete(0, tk.END)
            for item in items:
                lb.insert(tk.END, item)

        _populate(self._currencies)

        cur = self._var.get()
        if cur in self._currencies:
            idx = self._currencies.index(cur)
            lb.see(idx)
            lb.selection_set(idx)

        def _filter(*_) -> None:
            q = search_var.get().upper()
            _populate([c for c in self._currencies if q in c])

        search_var.trace_add("write", _filter)

        def _select(_event=None) -> None:
            sel = lb.curselection()
            if sel:
                self._var.set(filtered[sel[0]])
            _close()

        def _close() -> None:
            if popup.winfo_exists():
                popup.destroy()
            self._popup = None
            try:
                root.unbind("<Button-1>", self._close_bind_id)
            except Exception:
                pass

        lb.bind("<Double-Button-1>", _select)
        lb.bind("<Return>", _select)
        lb.bind("<Escape>", lambda _e: _close())
        search_entry.bind("<Return>", lambda _e: _select())
        search_entry.bind("<Escape>", lambda _e: _close())
        search_entry.bind(
            "<Down>",
            lambda _e: (lb.focus_set(), lb.selection_set(0)) if lb.size() > 0 else None,
        )

        def _close_on_outside(event: tk.Event) -> None:
            if not popup.winfo_exists():
                return
            w = event.widget
            while w is not None:
                if w is popup:
                    return
                try:
                    w = w.master
                except Exception:
                    break
            _close()

        def _bind_close() -> None:
            self._close_bind_id = root.bind("<Button-1>", _close_on_outside, "+")

        root.after(150, _bind_close)


# ─────────────────────────────────────────── private ────────────────────────

def _fmt(value: float) -> str:
    return f"{value:,.1f}"


def _parse_hex(hex_color: str) -> tuple[int, int, int]:
    return int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)


def _to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"
