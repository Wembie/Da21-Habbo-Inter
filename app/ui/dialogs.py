"""Custom styled dialog windows."""
import tkinter as tk
from tkinter import ttk
from typing import Callable

from app.models.dice_rule import DiceRule, UsdtRange
from app.services import dice_rules_service
from app.ui import widgets


def show_message(
    root: tk.Tk,
    title: str,
    message: str,
    accent_color: str,
    colors: dict,
    fonts: dict,
) -> None:
    dialog = _base_dialog(root, title, colors)

    tk.Frame(dialog, bg=accent_color, height=10).pack(fill=tk.X)
    tk.Label(dialog, text=title, font=fonts["header"],
             bg=colors["panel"], fg=accent_color).pack(pady=(20, 10))
    tk.Label(dialog, text=message, font=fonts["text"],
             bg=colors["panel"], fg=colors["foreground"],
             wraplength=350, justify=tk.CENTER).pack(pady=10, padx=20)

    ok = tk.Button(
        dialog, text="ACEPTAR", font=fonts["text"],
        bg=accent_color, fg=colors["foreground"],
        activebackground=widgets.darken_color(accent_color),
        activeforeground=colors["foreground"],
        relief=tk.FLAT, borderwidth=0, padx=25, pady=8,
        command=dialog.destroy,
    )
    ok.pack(pady=20)
    ok.bind("<Enter>", lambda _, b=ok, c=accent_color: b.config(bg=widgets.lighten_color(c)))
    ok.bind("<Leave>", lambda _, b=ok, c=accent_color: b.config(bg=c))


def show_confirmation(
    root: tk.Tk,
    title: str,
    message: str,
    colors: dict,
    fonts: dict,
) -> bool:
    dialog = _base_dialog(root, title, colors)

    tk.Label(dialog, text=message, font=fonts["text"],
             bg=colors["panel"], fg=colors["foreground"],
             wraplength=350, justify=tk.CENTER).pack(pady=(20, 30), padx=20)

    btn_frame = ttk.Frame(dialog)
    btn_frame.pack(fill=tk.X, padx=20, pady=10)
    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)

    result = [False]

    yes = tk.Button(
        btn_frame, text="SÍ", font=fonts["text"],
        bg=colors["accent4"], fg=colors["foreground"],
        activebackground=widgets.darken_color(colors["accent4"]),
        activeforeground=colors["foreground"],
        relief=tk.FLAT, borderwidth=0, padx=15, pady=8,
        command=lambda: [result.__setitem__(0, True), dialog.destroy()],
    )
    yes.grid(row=0, column=0, padx=5, sticky="e")

    no = tk.Button(
        btn_frame, text="NO", font=fonts["text"],
        bg=colors["accent1"], fg=colors["foreground"],
        activebackground=widgets.darken_color(colors["accent1"]),
        activeforeground=colors["foreground"],
        relief=tk.FLAT, borderwidth=0, padx=15, pady=8,
        command=dialog.destroy,
    )
    no.grid(row=0, column=1, padx=5, sticky="w")

    for btn, color in [(yes, colors["accent4"]), (no, colors["accent1"])]:
        btn.bind("<Enter>", lambda _, b=btn, c=color: b.config(bg=widgets.lighten_color(c)))
        btn.bind("<Leave>", lambda _, b=btn, c=color: b.config(bg=c))

    dialog.wait_window()
    return result[0]


class HistoryWindow:
    def __init__(
        self,
        root: tk.Tk,
        game_history: list[str],
        colors: dict,
        fonts: dict,
        on_export: callable,
    ) -> None:
        win = tk.Toplevel(root)
        win.title("Historial de Partidas")
        win.geometry("600x540")
        win.configure(bg=colors["background"])
        _center(win)

        container = ttk.Frame(win, padding="10 10 10 10")
        container.pack(fill=tk.BOTH, expand=True)

        tk.Label(container, text="HISTORIAL COMPLETO DE PARTIDAS",
                 font=fonts["title"], fg=colors["accent2"],
                 bg=colors["background"]).pack(pady=(0, 10))

        hist_frame = ttk.Frame(container)
        hist_frame.pack(fill=tk.BOTH, expand=True)

        text = tk.Text(hist_frame, wrap=tk.WORD, font=fonts["text"],
                       bg=colors["input"], fg=colors["foreground"],
                       insertbackground=colors["foreground"], relief=tk.FLAT)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sb = ttk.Scrollbar(hist_frame, command=text.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        text.config(yscrollcommand=sb.set)

        text.tag_configure("header", font=fonts["header"], foreground=colors["accent2"])
        text.tag_configure("subheader", font=fonts["header"], foreground=colors["accent3"])
        text.tag_configure("separator", foreground=colors["accent1"])

        text.insert(tk.END, "HISTORIAL COMPLETO DE PARTIDAS\n", "header")
        text.insert(tk.END, "=" * 50 + "\n\n", "separator")
        for i, entry in enumerate(game_history, 1):
            text.insert(tk.END, f"Partida #{i}:\n", "subheader")
            text.insert(tk.END, f"{entry}\n\n")
            text.insert(tk.END, "-" * 40 + "\n\n", "separator")

        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=10, fill=tk.X)
        btn_frame.columnconfigure(0, weight=1)
        widgets.styled_button(btn_frame, "EXPORTAR HISTORIAL", on_export,
                              0, 0, colors, fonts, colors["accent3"])


class DiceRulesConfigWindow:
    """Modal window for creating, editing and deleting dice rules."""

    _TABLE_HELP = (
        'Formato por línea:  "1-10: 0.5"  o  "10+: auto"\n'
        '"auto" = floor(monto / 10)   •   El límite superior es exclusivo'
    )

    def __init__(
        self,
        root: tk.Tk,
        rules: list[DiceRule],
        colors: dict,
        fonts: dict,
        on_close: Callable[[], None],
    ) -> None:
        import copy
        self._rules: list[DiceRule] = copy.deepcopy(rules)
        self._colors = colors
        self._fonts = fonts
        self._on_close = on_close
        self._selected_idx: int = 0

        win = tk.Toplevel(root)
        self._win = win
        win.title("Configurar Dados")
        win.geometry("660x500")
        win.configure(bg=colors["background"])
        win.transient(root)
        win.grab_set()
        win.resizable(False, False)
        _center(win)

        self._build()
        win.protocol("WM_DELETE_WINDOW", self._on_cancel)
        win.wait_window()

    # ── build ─────────────────────────────────────────────────────────────────

    def _build(self) -> None:
        c = self._colors
        f = self._fonts

        main = tk.Frame(self._win, bg=c["background"])
        main.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        # ── left: list ────────────────────────────────────────────────────────
        left = tk.Frame(main, bg=c["panel"], width=170)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left.columnconfigure(0, weight=1)
        left.grid_propagate(False)

        tk.Label(
            left, text="DADOS", font=f["header"],
            fg=c["foreground"], bg=c["panel"],
        ).pack(pady=(10, 4), padx=8, anchor="w")

        tk.Frame(left, bg=c["border"], height=1).pack(fill=tk.X, padx=8)

        lb_frame = tk.Frame(left, bg=c["panel"])
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        self._lb = tk.Listbox(
            lb_frame,
            font=f["text"],
            bg=c["input"],
            fg=c["foreground"],
            selectbackground=c["accent2"],
            selectforeground=c["foreground"],
            activestyle="none",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
        )
        self._lb.pack(fill=tk.BOTH, expand=True)
        self._lb.bind("<<ListboxSelect>>", self._on_list_select)

        btn_row = tk.Frame(left, bg=c["panel"])
        btn_row.pack(pady=(0, 8), padx=6, fill=tk.X)

        for text, cmd, color in [
            ("+ Nuevo",    self._new_rule,    c["accent4"]),
            ("− Eliminar", self._delete_rule, c["accent1"]),
        ]:
            b = tk.Button(
                btn_row, text=text, font=f["small"],
                bg=color, fg=c["foreground"],
                activebackground=widgets.darken_color(color),
                activeforeground=c["foreground"],
                relief=tk.FLAT, bd=0, padx=6, pady=5,
                command=cmd, cursor="hand2",
            )
            b.pack(fill=tk.X, pady=2)

        # ── right: edit form ──────────────────────────────────────────────────
        right = tk.Frame(main, bg=c["panel"])
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(1, weight=1)
        right.rowconfigure(4, weight=1)

        self._vars: dict[str, tk.StringVar] = {}
        fields = [
            ("Nombre:",       "name"),
            ("Símbolo:",      "symbol"),
            ("Mín. Créditos:", "min_credits"),
            ("Mín. USDT:",    "usdt_min"),
        ]

        for i, (label, key) in enumerate(fields):
            tk.Label(
                right, text=label, font=f["text"],
                fg=c["muted"], bg=c["panel"], anchor="e",
            ).grid(row=i, column=0, sticky="e", padx=(10, 6), pady=(8, 2))

            v = tk.StringVar()
            self._vars[key] = v
            hint = "(1 unidad = N créditos)" if key == "symbol" else ""
            entry = tk.Entry(
                right, textvariable=v, font=f["text"],
                bg=c["input"], fg=c["foreground"],
                insertbackground=c["foreground"],
                relief=tk.FLAT, bd=0,
                highlightthickness=1,
                highlightbackground=c["border"],
                highlightcolor=c["accent2"],
                width=18,
            )
            entry.grid(row=i, column=1, sticky="w", padx=(0, 10), pady=(8, 2), ipady=4)

            if hint:
                tk.Label(
                    right, text=hint, font=f["small"],
                    fg=c["muted"], bg=c["panel"],
                ).grid(row=i, column=2, sticky="w", padx=(0, 10))

        # unit_size field
        tk.Label(
            right, text="Tamaño unidad:", font=f["text"],
            fg=c["muted"], bg=c["panel"], anchor="e",
        ).grid(row=len(fields), column=0, sticky="e", padx=(10, 6), pady=(8, 2))

        v = tk.StringVar()
        self._vars["unit_size"] = v
        tk.Entry(
            right, textvariable=v, font=f["text"],
            bg=c["input"], fg=c["foreground"],
            insertbackground=c["foreground"],
            relief=tk.FLAT, bd=0,
            highlightthickness=1,
            highlightbackground=c["border"],
            highlightcolor=c["accent2"],
            width=10,
        ).grid(row=len(fields), column=1, sticky="w", padx=(0, 10), pady=(8, 2), ipady=4)
        tk.Label(
            right, text="créditos/unidad (ej: 50 para Legión)",
            font=f["small"], fg=c["muted"], bg=c["panel"],
        ).grid(row=len(fields), column=2, sticky="w")

        row_table = len(fields) + 1
        tk.Label(
            right, text="Tabla USDT:", font=f["text"],
            fg=c["muted"], bg=c["panel"], anchor="ne",
        ).grid(row=row_table, column=0, sticky="ne", padx=(10, 6), pady=(10, 2))

        table_outer = tk.Frame(right, bg=c["panel"])
        table_outer.grid(
            row=row_table, column=1, columnspan=2,
            sticky="nsew", padx=(0, 10), pady=(10, 2),
        )
        table_outer.columnconfigure(0, weight=1)
        table_outer.rowconfigure(0, weight=1)
        right.rowconfigure(row_table, weight=1)

        self._table_text = tk.Text(
            table_outer,
            font=("Consolas", 9),
            bg=c["input"], fg=c["foreground"],
            insertbackground=c["foreground"],
            relief=tk.FLAT, bd=0,
            highlightthickness=1,
            highlightbackground=c["border"],
            highlightcolor=c["accent2"],
            height=6, width=28,
        )
        self._table_text.grid(row=0, column=0, sticky="nsew")

        tk.Label(
            right, text=self._TABLE_HELP,
            font=f["small"], fg=c["muted"], bg=c["panel"],
            justify=tk.LEFT,
        ).grid(row=row_table + 1, column=1, columnspan=2, sticky="w", padx=(0, 10), pady=(2, 8))

        # ── bottom buttons ────────────────────────────────────────────────────
        bottom = tk.Frame(self._win, bg=c["background"])
        bottom.pack(fill=tk.X, padx=12, pady=(0, 10))

        for text, cmd, color in [
            ("✔  GUARDAR CAMBIOS", self._on_save,   c["accent4"]),
            ("✖  CANCELAR",        self._on_cancel, c["accent1"]),
        ]:
            b = tk.Button(
                bottom, text=text, font=f["button"],
                bg=color, fg=c["foreground"],
                activebackground=widgets.darken_color(color),
                activeforeground=c["foreground"],
                relief=tk.FLAT, bd=0, padx=20, pady=9,
                command=cmd, cursor="hand2",
            )
            b.pack(side=tk.LEFT, padx=(0, 10))

        # populate list and select first
        self._refresh_list()
        if self._rules:
            self._lb.selection_set(0)
            self._load_rule(0)

    # ── list interaction ──────────────────────────────────────────────────────

    def _refresh_list(self) -> None:
        self._lb.delete(0, tk.END)
        for r in self._rules:
            self._lb.insert(tk.END, f"  {r.name}")

    def _on_list_select(self, _event=None) -> None:
        sel = self._lb.curselection()
        if not sel:
            return
        self._save_to_current()
        self._selected_idx = sel[0]
        self._load_rule(sel[0])

    def _load_rule(self, idx: int) -> None:
        r = self._rules[idx]
        self._vars["name"].set(r.name)
        self._vars["symbol"].set(r.symbol)
        self._vars["min_credits"].set(str(r.min_credits))
        self._vars["usdt_min"].set(str(r.usdt_min))
        self._vars["unit_size"].set(str(r.unit_size))

        lines = []
        for u in r.usdt_table:
            if u.to is not None:
                lines.append(f"{u.from_}-{u.to}: {u.tip}")
            else:
                val = "auto" if u.formula == "floor10" else str(u.tip)
                lines.append(f"{u.from_}+: {val}")

        self._table_text.delete("1.0", tk.END)
        self._table_text.insert("1.0", "\n".join(lines))

    def _save_to_current(self) -> None:
        if not self._rules or self._selected_idx >= len(self._rules):
            return
        r = self._rules[self._selected_idx]
        name = self._vars["name"].get().strip()
        if name:
            r.name = name
        r.symbol = (self._vars["symbol"].get().strip() or r.symbol)[:4]
        try:
            r.min_credits = float(self._vars["min_credits"].get())
        except ValueError:
            pass
        try:
            r.usdt_min = float(self._vars["usdt_min"].get())
        except ValueError:
            pass
        try:
            r.unit_size = float(self._vars["unit_size"].get())
        except ValueError:
            pass
        r.usdt_table = self._parse_table(self._table_text.get("1.0", tk.END))

    @staticmethod
    def _parse_table(text: str) -> list[UsdtRange]:
        ranges: list[UsdtRange] = []
        for line in text.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                colon_idx = line.index(":")
                range_part = line[:colon_idx].strip()
                val_part = line[colon_idx + 1:].strip()

                if "+" in range_part:
                    from_ = float(range_part.replace("+", ""))
                    if val_part.lower() == "auto":
                        ranges.append(UsdtRange(from_=from_, to=None, formula="floor10"))
                    else:
                        ranges.append(UsdtRange(from_=from_, to=None, tip=float(val_part)))
                elif "-" in range_part:
                    parts = range_part.split("-", 1)
                    from_ = float(parts[0])
                    to_ = float(parts[1])
                    ranges.append(UsdtRange(from_=from_, to=to_, tip=float(val_part)))
            except (ValueError, IndexError):
                pass
        return ranges

    # ── actions ───────────────────────────────────────────────────────────────

    def _new_rule(self) -> None:
        self._save_to_current()
        n = len(self._rules) + 1
        new = DiceRule(
            id=f"dado_{n}",
            name=f"Dado {n}",
            symbol="C",
            unit_size=1.0,
            min_credits=5.0,
            usdt_min=1.0,
            usdt_table=[
                UsdtRange(from_=1.0, to=10.0, tip=0.5),
                UsdtRange(from_=10.0, to=None, formula="floor10"),
            ],
        )
        self._rules.append(new)
        self._refresh_list()
        idx = len(self._rules) - 1
        self._lb.selection_clear(0, tk.END)
        self._lb.selection_set(idx)
        self._lb.see(idx)
        self._selected_idx = idx
        self._load_rule(idx)

    def _delete_rule(self) -> None:
        if len(self._rules) <= 1:
            show_message(
                self._win, "Error",
                "Debe existir al menos un dado.",
                self._colors["accent1"], self._colors, self._fonts,
            )
            return
        self._rules.pop(self._selected_idx)
        self._selected_idx = max(0, self._selected_idx - 1)
        self._refresh_list()
        self._lb.selection_set(self._selected_idx)
        if self._rules:
            self._load_rule(self._selected_idx)

    def _on_save(self) -> None:
        self._save_to_current()
        dice_rules_service.save(self._rules)
        self._win.destroy()
        self._on_close()

    def _on_cancel(self) -> None:
        self._win.destroy()


# --- helpers ---

def _base_dialog(root: tk.Tk, title: str, colors: dict) -> tk.Toplevel:
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry("400x220")
    dialog.configure(bg=colors["panel"])
    dialog.transient(root)
    dialog.grab_set()
    _center(dialog)
    return dialog


def _center(window: tk.Toplevel) -> None:
    window.update_idletasks()
    w, h = window.winfo_width(), window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (w // 2)
    y = (window.winfo_screenheight() // 2) - (h // 2)
    window.geometry(f"{w}x{h}+{x}+{y}")
