import tkinter as tk
from tkinter import ttk

from app.constants import COLORS
from app.models.game_state import GameState
from app.services.persistence import PersistenceService
from app.ui import theme
from app.ui.panels.controls_panel import ControlsPanel
from app.ui.panels.notepad_panel import NotepadPanel


class CuentaApp:
    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._root.title("Da21 Habbo Inter")
        self._root.geometry("1160x840")
        self._root.configure(bg=COLORS["background"])
        self._root.resizable(True, True)
        self._root.minsize(980, 720)

        self._persistence = PersistenceService()
        self._state = self._persistence.load()

        self._fonts = theme.setup_fonts(root)
        theme.setup_styles(ttk.Style(), self._fonts)

        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=0)   # header — fixed
        self._root.rowconfigure(1, weight=1)   # main content

        self._build_header()

        container = ttk.Frame(self._root, padding="6 6 6 6", style="TFrame")
        container.grid(row=1, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        self._notepad = NotepadPanel(container, COLORS, self._fonts)
        self._controls = ControlsPanel(
            container, self._state, COLORS, self._fonts, self._on_state_change
        )

        self._center()
        self._notepad.update(self._state)

    # ----------------------------------------------------------------- build

    def _build_header(self) -> None:
        header = tk.Frame(self._root, bg=COLORS["panel"])
        header.grid(row=0, column=0, sticky="ew")

        # Triple-color accent stripe (Inter / Z1 / Z2)
        for stripe_color in (COLORS["inter"], COLORS["z1"], COLORS["z2"]):
            tk.Frame(header, bg=stripe_color, width=5).pack(side=tk.LEFT, fill=tk.Y)

        # Title block
        title_block = tk.Frame(header, bg=COLORS["panel"])
        title_block.pack(side=tk.LEFT, padx=14, pady=8)

        tk.Label(
            title_block,
            text="Da21 Habbo Inter",
            font=self._fonts["title"],
            fg=COLORS["foreground"],
            bg=COLORS["panel"],
        ).pack(anchor="w")

        tk.Label(
            title_block,
            text="Sistema de gesti\u00f3n de saldos  \u2022  by _Acos_ / Wembie",
            font=self._fonts["small"],
            fg=COLORS["muted"],
            bg=COLORS["panel"],
        ).pack(anchor="w")

        # Version pill on the right
        pill = tk.Frame(header, bg=COLORS["highlight"], padx=8, pady=3)
        pill.pack(side=tk.RIGHT, padx=12, pady=8)
        tk.Label(
            pill, text="v1.0.0",
            font=self._fonts["small"],
            fg=COLORS["muted"],
            bg=COLORS["highlight"],
        ).pack()

    # ----------------------------------------------------------------- private

    def _on_state_change(self, state: GameState) -> None:
        self._persistence.save(state)
        self._notepad.update(state)

    def _center(self) -> None:
        self._root.update_idletasks()
        w, h = self._root.winfo_width(), self._root.winfo_height()
        x = (self._root.winfo_screenwidth()  // 2) - (w // 2)
        y = (self._root.winfo_screenheight() // 2) - (h // 2)
        self._root.geometry(f"{w}x{h}+{x}+{y}")
