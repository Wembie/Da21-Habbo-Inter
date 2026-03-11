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
        self._root.title("Da21 Habbo Intear")
        self._root.geometry("1000x750")
        self._root.configure(bg=COLORS["background"])

        self._persistence = PersistenceService()
        self._state = self._persistence.load()

        self._fonts = theme.setup_fonts(root)
        theme.setup_styles(ttk.Style(), self._fonts)

        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        container = ttk.Frame(self._root, padding="10 10 10 10", style="TFrame")
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        self._notepad = NotepadPanel(container, COLORS, self._fonts)
        self._controls = ControlsPanel(container, self._state, COLORS, self._fonts,
                                       self._on_state_change)

        self._center()
        self._notepad.update(self._state)

    # ----------------------------------------------------------------- private

    def _on_state_change(self, state: GameState) -> None:
        self._persistence.save(state)
        self._notepad.update(state)

    def _center(self) -> None:
        self._root.update_idletasks()
        w, h = self._root.winfo_width(), self._root.winfo_height()
        x = (self._root.winfo_screenwidth() // 2) - (w // 2)
        y = (self._root.winfo_screenheight() // 2) - (h // 2)
        self._root.geometry(f"{w}x{h}+{x}+{y}")
