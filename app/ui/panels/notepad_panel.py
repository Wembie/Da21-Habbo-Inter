import tkinter as tk
from tkinter import filedialog, ttk

from app.constants import NOTES_PLACEHOLDER
from app.models.game_state import GameState
from app.ui import dialogs, widgets


class NotepadPanel:
    def __init__(self, parent: ttk.Frame, colors: dict, fonts: dict) -> None:
        self._colors = colors
        self._fonts = fonts
        self._root = parent.winfo_toplevel()

        container = ttk.Frame(parent, style="TFrame")
        container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1)

        self._balance_notepad = self._build_text_frame(container, "SALDOS", 0)
        self._personal_notepad = self._build_personal_frame(container)

    # ------------------------------------------------------------------ build

    def _build_text_frame(self, parent: ttk.Frame, title: str, row: int) -> tk.Text:
        lf = ttk.LabelFrame(parent, text=title, style="TLabelframe")
        lf.grid(row=row, column=0, padx=5, pady=5, sticky="nsew")
        lf.columnconfigure(0, weight=1)
        lf.rowconfigure(0, weight=1)
        return self._text_with_scrollbar(lf)

    def _build_personal_frame(self, parent: ttk.Frame) -> tk.Text:
        lf = ttk.LabelFrame(parent, text="NOTAS PERSONALES", style="TLabelframe")
        lf.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        lf.columnconfigure(0, weight=1)
        lf.rowconfigure(0, weight=1)

        notepad = self._text_with_scrollbar(lf)

        bf = ttk.Frame(lf)
        bf.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        bf.columnconfigure(0, weight=1)
        bf.columnconfigure(1, weight=1)
        widgets.styled_button(bf, "GUARDAR NOTAS", self._save_notes,
                              0, 0, self._colors, self._fonts, self._colors["accent4"])
        widgets.styled_button(bf, "CARGAR NOTAS", self._load_notes,
                              0, 1, self._colors, self._fonts, self._colors["accent3"])

        notepad.insert(tk.END, NOTES_PLACEHOLDER)
        notepad.config(fg="#888888")
        notepad.bind("<FocusIn>", self._on_focus_in)
        notepad.bind("<FocusOut>", self._on_focus_out)
        return notepad

    def _text_with_scrollbar(self, parent: ttk.LabelFrame) -> tk.Text:
        tf = ttk.Frame(parent)
        tf.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        tf.columnconfigure(0, weight=1)
        tf.rowconfigure(0, weight=1)

        text = tk.Text(tf, wrap=tk.WORD, font=self._fonts["text"],
                       bg=self._colors["input"], fg=self._colors["foreground"],
                       insertbackground=self._colors["foreground"],
                       selectbackground=self._colors["accent2"], relief=tk.FLAT)
        text.grid(row=0, column=0, sticky="nsew")

        sb = ttk.Scrollbar(tf, command=text.yview)
        sb.grid(row=0, column=1, sticky="ns")
        text.config(yscrollcommand=sb.set)
        return text

    # ------------------------------------------------------------------ public

    def update(self, state: GameState) -> None:
        self._balance_notepad.delete("1.0", tk.END)
        self._balance_notepad.insert(tk.END, "SALDOS ACTUALES:\n\n")
        self._balance_notepad.insert(tk.END, f"{state.name_z0} (Inter): {state.balance_z0}\n")
        self._balance_notepad.insert(tk.END, f"{state.name_z1} (Z1): {state.balance_z1}\n")
        self._balance_notepad.insert(tk.END, f"{state.name_z2} (Z2): {state.balance_z2}\n")
        if state.history:
            self._balance_notepad.insert(tk.END, f"\n{'='*20}\nÚLTIMAS PARTIDAS:\n")
            for entry in state.history[-5:]:
                self._balance_notepad.insert(tk.END, f"\n{entry}\n")

    # --------------------------------------------------------------- callbacks

    def _on_focus_in(self, _) -> None:
        if self._personal_notepad.get("1.0", tk.END).strip() == NOTES_PLACEHOLDER.strip():
            self._personal_notepad.delete("1.0", tk.END)
            self._personal_notepad.config(fg=self._colors["foreground"])

    def _on_focus_out(self, _) -> None:
        if not self._personal_notepad.get("1.0", tk.END).strip():
            self._personal_notepad.insert(tk.END, NOTES_PLACEHOLDER)
            self._personal_notepad.config(fg="#888888")

    def _save_notes(self) -> None:
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Guardar notas como",
        )
        if not filename:
            return
        try:
            content = self._personal_notepad.get("1.0", tk.END)
            if content.strip() == NOTES_PLACEHOLDER.strip():
                content = ""
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            dialogs.show_message(self._root, "Éxito", f"Notas guardadas en {filename}",
                                 self._colors["accent4"], self._colors, self._fonts)
        except OSError as e:
            dialogs.show_message(self._root, "Error", str(e),
                                 self._colors["accent1"], self._colors, self._fonts)

    def _load_notes(self) -> None:
        filename = filedialog.askopenfilename(
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Abrir archivo de notas",
        )
        if not filename:
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            self._personal_notepad.delete("1.0", tk.END)
            self._personal_notepad.config(fg=self._colors["foreground"])
            self._personal_notepad.insert(tk.END, content)
            dialogs.show_message(self._root, "Carga Exitosa", f"Notas cargadas desde {filename}",
                                 self._colors["accent4"], self._colors, self._fonts)
        except OSError as e:
            dialogs.show_message(self._root, "Error", str(e),
                                 self._colors["accent1"], self._colors, self._fonts)
