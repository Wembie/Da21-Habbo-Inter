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
        # (name_label, balance_label) for each player: [inter, z1, z2]
        self._stat_refs: list[tuple[tk.Label, tk.Label]] = []

        container = ttk.Frame(parent, style="TFrame")
        container.grid(row=0, column=1, sticky="nsew", padx=(4, 8), pady=8)
        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1)

        self._build_balance_frame(container)
        self._personal_notepad = self._build_personal_frame(container)

    # ------------------------------------------------------------------ build

    def _build_balance_frame(self, parent: ttk.Frame) -> None:
        lf = ttk.LabelFrame(parent, text="RESUMEN", style="TLabelframe")
        lf.grid(row=0, column=0, padx=4, pady=(4, 4), sticky="nsew")
        lf.columnconfigure(0, weight=1)
        lf.rowconfigure(3, weight=1)

        # ── Stat cards ──────────────────────────────────────────────────────
        cards_frame = tk.Frame(lf, bg=self._colors["panel"])
        cards_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(6, 2))
        cards_frame.columnconfigure(0, weight=1)

        for role, color_key in [("Inter", "inter"), ("Z1", "z1"), ("Z2", "z2")]:
            name_lbl, bal_lbl = self._make_stat_card(cards_frame, role, color_key)
            self._stat_refs.append((name_lbl, bal_lbl))

        # ── Separator ───────────────────────────────────────────────────────
        tk.Frame(lf, bg=self._colors["border"], height=1).grid(
            row=1, column=0, sticky="ew", padx=8, pady=(6, 0)
        )

        # ── History header ──────────────────────────────────────────────────
        hist_hdr = tk.Frame(lf, bg=self._colors["panel"])
        hist_hdr.grid(row=2, column=0, sticky="ew", padx=8, pady=(8, 2))
        tk.Label(
            hist_hdr, text="\u00daLTIMAS PARTIDAS",
            font=self._fonts["small"], fg=self._colors["muted"],
            bg=self._colors["panel"],
        ).pack(anchor="w")

        # ── History text ────────────────────────────────────────────────────
        hist_tf = tk.Frame(lf, bg=self._colors["panel"])
        hist_tf.grid(row=3, column=0, sticky="nsew", padx=6, pady=(0, 8))
        hist_tf.columnconfigure(0, weight=1)
        hist_tf.rowconfigure(0, weight=1)

        mono = self._fonts.get("mono", self._fonts["small"])
        self._history_text = tk.Text(
            hist_tf,
            wrap=tk.WORD,
            font=mono,
            bg=self._colors["input"],
            fg=self._colors["foreground"],
            insertbackground=self._colors["foreground"],
            selectbackground=self._colors["highlight"],
            selectforeground=self._colors["foreground"],
            relief=tk.FLAT, bd=0,
            highlightthickness=1,
            highlightbackground=self._colors["border"],
            highlightcolor=self._colors["accent2"],
            padx=8, pady=8,
            state=tk.DISABLED,
        )
        self._history_text.grid(row=0, column=0, sticky="nsew")
        self._history_text.tag_configure(
            "entry", font=mono, foreground=self._colors["foreground"]
        )

        sb = ttk.Scrollbar(hist_tf, command=self._history_text.yview,
                           style="Vertical.TScrollbar")
        sb.grid(row=0, column=1, sticky="ns")
        self._history_text.config(yscrollcommand=sb.set)

    def _make_stat_card(
        self, parent: tk.Frame, role: str, color_key: str
    ) -> tuple[tk.Label, tk.Label]:
        tag_color = self._colors[color_key]
        card_bg = self._colors.get("card", self._colors["panel"])

        # Thin border wrapper
        outer = tk.Frame(parent, bg=self._colors["border"], pady=1, padx=1)
        outer.pack(fill=tk.X, pady=2)

        card = tk.Frame(outer, bg=card_bg, pady=5)
        card.pack(fill=tk.X)
        card.columnconfigure(2, weight=1)

        # Left colored stripe
        tk.Frame(card, bg=tag_color, width=4).grid(
            row=0, column=0, rowspan=2, sticky="ns", padx=(4, 8)
        )

        # Avatar circle
        av = tk.Canvas(card, width=26, height=26, bg=card_bg, highlightthickness=0)
        av.grid(row=0, column=1, rowspan=2, padx=(0, 8), sticky="w")
        av.create_oval(1, 1, 25, 25, fill=tag_color, outline="")
        av.create_text(
            13, 13, text=role[0],
            font=self._fonts["small"],
            fill=self._colors.get("panel", "#191930"),
        )

        # Name label
        name_lbl = tk.Label(
            card, text=f"... ({role})",
            font=self._fonts["small"], fg=tag_color, bg=card_bg, anchor="w",
        )
        name_lbl.grid(row=0, column=2, sticky="w", padx=(0, 6))

        # Balance label
        bal_lbl = tk.Label(
            card, text="0.0",
            font=self._fonts["header"], fg=tag_color, bg=card_bg, anchor="w",
        )
        bal_lbl.grid(row=1, column=2, sticky="w", padx=(0, 6))

        return name_lbl, bal_lbl

    def _build_personal_frame(self, parent: ttk.Frame) -> tk.Text:
        lf = ttk.LabelFrame(parent, text="NOTAS PERSONALES", style="TLabelframe")
        lf.grid(row=1, column=0, padx=4, pady=(4, 4), sticky="nsew")
        lf.columnconfigure(0, weight=1)
        lf.rowconfigure(0, weight=1)

        notepad = self._text_with_scrollbar(lf)

        bf = tk.Frame(lf, bg=self._colors["panel"])
        bf.grid(row=1, column=0, padx=5, pady=6, sticky="ew")
        bf.columnconfigure(0, weight=1)
        bf.columnconfigure(1, weight=1)

        widgets.styled_button(
            bf, "\u2193  GUARDAR NOTAS", self._save_notes,
            0, 0, self._colors, self._fonts, self._colors["accent4"],
        )
        widgets.styled_button(
            bf, "\u2191  CARGAR NOTAS", self._load_notes,
            0, 1, self._colors, self._fonts, self._colors["accent2"],
        )

        notepad.insert(tk.END, NOTES_PLACEHOLDER)
        notepad.config(fg=self._colors["muted"])
        notepad.bind("<FocusIn>",  self._on_focus_in)
        notepad.bind("<FocusOut>", self._on_focus_out)
        return notepad

    def _text_with_scrollbar(self, parent: ttk.LabelFrame) -> tk.Text:
        tf = tk.Frame(parent, bg=self._colors["panel"])
        tf.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        tf.columnconfigure(0, weight=1)
        tf.rowconfigure(0, weight=1)

        text = tk.Text(
            tf,
            wrap=tk.WORD,
            font=self._fonts["text"],
            bg=self._colors["input"],
            fg=self._colors["foreground"],
            insertbackground=self._colors["foreground"],
            selectbackground=self._colors["highlight"],
            selectforeground=self._colors["foreground"],
            relief=tk.FLAT, bd=0,
            highlightthickness=1,
            highlightbackground=self._colors["border"],
            highlightcolor=self._colors["accent2"],
            padx=8, pady=8,
            spacing1=2, spacing3=2,
        )
        text.grid(row=0, column=0, sticky="nsew")

        sb = ttk.Scrollbar(tf, command=text.yview, style="Vertical.TScrollbar")
        sb.grid(row=0, column=1, sticky="ns")
        text.config(yscrollcommand=sb.set)
        return text

    # ------------------------------------------------------------------ public

    def update(self, state: GameState) -> None:
        players = [
            (state.name_z0, "Inter", "inter", state.balance_z0),
            (state.name_z1, "Z1",   "z1",    state.balance_z1),
            (state.name_z2, "Z2",   "z2",    state.balance_z2),
        ]
        for i, (name, role, color_key, balance) in enumerate(players):
            name_lbl, bal_lbl = self._stat_refs[i]
            name_lbl.config(text=f"{name} ({role})")
            danger = self._colors.get("danger", self._colors["accent1"])
            val_color = danger if balance < 0 else self._colors[color_key]
            bal_lbl.config(text=f"{balance:,.1f}", fg=val_color)

        # Update history text
        self._history_text.config(state=tk.NORMAL)
        self._history_text.delete("1.0", tk.END)
        for entry in state.history[-5:]:
            self._history_text.insert(tk.END, f"{entry}\n\n", "entry")
        self._history_text.config(state=tk.DISABLED)

    # --------------------------------------------------------------- callbacks

    def _on_focus_in(self, _) -> None:
        if self._personal_notepad.get("1.0", tk.END).strip() == NOTES_PLACEHOLDER.strip():
            self._personal_notepad.delete("1.0", tk.END)
            self._personal_notepad.config(fg=self._colors["foreground"])

    def _on_focus_out(self, _) -> None:
        if not self._personal_notepad.get("1.0", tk.END).strip():
            self._personal_notepad.insert(tk.END, NOTES_PLACEHOLDER)
            self._personal_notepad.config(fg=self._colors["muted"])

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
            dialogs.show_message(
                self._root, "\u00c9xito", f"Notas guardadas en {filename}",
                self._colors["accent4"], self._colors, self._fonts,
            )
        except OSError as e:
            dialogs.show_message(
                self._root, "Error", str(e),
                self._colors["accent1"], self._colors, self._fonts,
            )

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
            dialogs.show_message(
                self._root, "Carga Exitosa", f"Notas cargadas desde {filename}",
                self._colors["accent4"], self._colors, self._fonts,
            )
        except OSError as e:
            dialogs.show_message(
                self._root, "Error", str(e),
                self._colors["accent1"], self._colors, self._fonts,
            )
