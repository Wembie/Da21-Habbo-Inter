import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime
from typing import Callable

from app.constants import CURRENCIES
from app.models.game_state import GameState
from app.models.tip_calculator import calculate_tip, calculate_tip_usdt
from app.ui import dialogs, widgets


class ControlsPanel:
    def __init__(
        self,
        parent: ttk.Frame,
        state: GameState,
        colors: dict,
        fonts: dict,
        on_state_change: Callable[[GameState], None],
    ) -> None:
        self._state = state
        self._colors = colors
        self._fonts = fonts
        self._on_state_change = on_state_change
        self._root = parent.winfo_toplevel()

        self._balance_z0 = tk.DoubleVar(value=state.balance_z0)
        self._balance_z1 = tk.DoubleVar(value=state.balance_z1)
        self._balance_z2 = tk.DoubleVar(value=state.balance_z2)
        self._name_z0 = tk.StringVar(value=state.name_z0)
        self._name_z1 = tk.StringVar(value=state.name_z1)
        self._name_z2 = tk.StringVar(value=state.name_z2)
        self._game_var = tk.DoubleVar()
        self._real_money_var = tk.BooleanVar()
        self._usdt_var = tk.BooleanVar()
        self._currency_var = tk.StringVar(value=state.currency)

        self._build(parent)

    # ------------------------------------------------------------------ build

    def _build(self, parent: ttk.Frame) -> None:
        frame = ttk.LabelFrame(parent, text="CONTROLES", padding="10 10 10 10", style="TLabelframe")
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        for i in range(11):
            frame.rowconfigure(i, pad=5)
        frame.columnconfigure(0, pad=10)
        frame.columnconfigure(1, pad=10)

        self._build_balances(frame)
        self._build_game(frame)
        self._build_payment(frame)
        self._build_result(frame)
        self._build_actions(frame)
        self._build_io(frame)

        tk.Label(
            frame, text="Developed By _Acos_ / Wembie",
            font=self._fonts["small"],
            fg=self._colors["foreground"], bg=self._colors["panel"],
        ).grid(row=10, column=0, columnspan=2, pady=(15, 0))

    def _build_balances(self, parent: ttk.Frame) -> None:
        bf = ttk.Frame(parent)
        bf.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        widgets.section_title(bf, "SALDOS", 0, 0, self._colors, self._fonts, colspan=2)
        for row, (tag, name_var, balance_var) in enumerate([
            ("(Inter)", self._name_z0, self._balance_z0),
            ("(Z1)",    self._name_z1, self._balance_z1),
            ("(Z2)",    self._name_z2, self._balance_z2),
        ], start=1):
            widgets.player_row(bf, tag, name_var, balance_var, row,
                               self._colors, self._fonts, self._sync_to_state)

    def _build_game(self, parent: ttk.Frame) -> None:
        widgets.section_title(parent, "JUEGO", 1, 0, self._colors, self._fonts, colspan=2)
        widgets.label_entry(parent, "Monto del juego:", self._game_var,
                            2, 0, self._colors, self._fonts, colspan=2)

    def _build_payment(self, parent: ttk.Frame) -> None:
        pf = ttk.LabelFrame(parent, text="TIPO DE PAGO", style="TLabelframe")
        pf.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

        widgets.styled_checkbox(pf, "Dinero Real", self._real_money_var, 0, 0,
                                self._colors, self._fonts,
                                lambda: self._on_checkbox(self._real_money_var))
        widgets.styled_checkbox(pf, "USDT", self._usdt_var, 0, 1,
                                self._colors, self._fonts,
                                lambda: self._on_checkbox(self._usdt_var))

        cf = ttk.Frame(pf)
        cf.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 6), sticky="w")
        tk.Label(cf, text="Moneda:", font=self._fonts["text"],
                 fg=self._colors["foreground"], bg=self._colors["panel"],
                 ).pack(side=tk.LEFT, padx=(0, 6))
        self._currency_combo = ttk.Combobox(
            cf, textvariable=self._currency_var,
            values=CURRENCIES, state="disabled",
            font=self._fonts["text"], width=6,
        )
        self._currency_combo.pack(side=tk.LEFT)

    def _build_result(self, parent: ttk.Frame) -> None:
        widgets.section_title(parent, "RESULTADO", 4, 0, self._colors, self._fonts, colspan=2)
        gf = ttk.Frame(parent)
        gf.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
        gf.columnconfigure(0, weight=1)
        gf.columnconfigure(1, weight=1)
        widgets.styled_button(gf, "Z1 GANA", lambda: self._record_game("z1"),
                              0, 0, self._colors, self._fonts, self._colors["accent2"])
        widgets.styled_button(gf, "Z2 GANA", lambda: self._record_game("z2"),
                              0, 1, self._colors, self._fonts, self._colors["accent2"])

    def _build_actions(self, parent: ttk.Frame) -> None:
        widgets.section_title(parent, "ACCIONES", 6, 0, self._colors, self._fonts, colspan=2)
        af = ttk.Frame(parent)
        af.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")
        af.columnconfigure(0, weight=1)
        af.columnconfigure(1, weight=1)
        widgets.styled_button(af, "HISTORIAL", self._show_history,
                              0, 0, self._colors, self._fonts, self._colors["accent4"])
        widgets.styled_button(af, "RESET", self._reset,
                              0, 1, self._colors, self._fonts, self._colors["accent1"])

    def _build_io(self, parent: ttk.Frame) -> None:
        iof = ttk.Frame(parent)
        iof.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")
        iof.columnconfigure(0, weight=1)
        iof.columnconfigure(1, weight=1)
        widgets.styled_button(iof, "IMPORTAR SALDOS", self._import_balances,
                              0, 0, self._colors, self._fonts, self._colors["accent3"])
        widgets.styled_button(iof, "EXPORTAR SALDOS", self._export_balances,
                              0, 1, self._colors, self._fonts, self._colors["accent3"])

    # --------------------------------------------------------- event handlers

    def _on_checkbox(self, clicked_var: tk.BooleanVar) -> None:
        if clicked_var is self._real_money_var and self._real_money_var.get():
            self._usdt_var.set(False)
        elif clicked_var is self._usdt_var and self._usdt_var.get():
            self._real_money_var.set(False)
        self._currency_combo.config(
            state="readonly" if self._real_money_var.get() else "disabled"
        )

    def _sync_to_state(self, *_) -> None:
        self._state.balance_z0 = self._balance_z0.get()
        self._state.balance_z1 = self._balance_z1.get()
        self._state.balance_z2 = self._balance_z2.get()
        self._state.name_z0 = self._name_z0.get()
        self._state.name_z1 = self._name_z1.get()
        self._state.name_z2 = self._name_z2.get()
        self._on_state_change(self._state)

    def _record_game(self, winner: str) -> None:
        try:
            game_amount = self._game_var.get()
        except tk.TclError:
            self._show_error("El monto del juego no es válido.")
            return

        if self._usdt_var.get():
            if game_amount < 1.0:
                self._show_error("El monto del juego debe ser al menos 1 USDT.")
                return
            tip = calculate_tip_usdt(game_amount)
            currency = "USDT"
            payment_method = "USDT"
        else:
            if game_amount < 5.0:
                self._show_error("El monto del juego debe ser al menos 5 créditos.")
                return
            if self._real_money_var.get():
                currency = self._currency_var.get()
                tip = round(game_amount * 0.1, 2)
                payment_method = f"Dinero Real ({currency})"
            else:
                tip = calculate_tip(game_amount)
                currency = "C"
                payment_method = "Créditos Habbo"

        b0 = self._balance_z0.get()
        b1 = self._balance_z1.get()
        b2 = self._balance_z2.get()

        if winner == "z1":
            new_z0 = round(b0 + tip, 2)
            new_z1 = round(b1 + game_amount - tip, 2)
            new_z2 = round(b2 - game_amount, 2)
        else:
            new_z0 = round(b0 + tip, 2)
            new_z1 = round(b1 - game_amount, 2)
            new_z2 = round(b2 + game_amount - tip, 2)

        self._balance_z0.set(new_z0)
        self._balance_z1.set(new_z1)
        self._balance_z2.set(new_z2)

        n0 = self._name_z0.get()
        n1 = self._name_z1.get()
        n2 = self._name_z2.get()
        winner_name = f"{n1} (Z1)" if winner == "z1" else f"{n2} (Z2)"
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

        entry = (
            f"[{timestamp}] Ganador: {winner_name}\n"
            f"Método: {payment_method}\n"
            f"Monto: {game_amount} {currency}\n"
            f"Propina: {tip} {currency}\n"
            f"Saldos: {n0}(Inter)={new_z0}, {n1}(Z1)={new_z1}, {n2}(Z2)={new_z2}"
        )

        self._state.balance_z0 = new_z0
        self._state.balance_z1 = new_z1
        self._state.balance_z2 = new_z2
        self._state.name_z0 = n0
        self._state.name_z1 = n1
        self._state.name_z2 = n2
        self._state.history.append(entry)
        self._on_state_change(self._state)

        dialogs.show_message(
            self._root, "Partida Registrada",
            f"Ganador: {winner_name}\nMonto: {game_amount} {currency}\nPropina: {tip} {currency}",
            self._colors["accent4"], self._colors, self._fonts,
        )

    def _reset(self) -> None:
        if dialogs.show_confirmation(
            self._root, "Confirmar",
            "¿Estás seguro de reiniciar todos los saldos y el historial?",
            self._colors, self._fonts,
        ):
            for var in (self._balance_z0, self._balance_z1, self._balance_z2, self._game_var):
                var.set(0.0)
            self._state.balance_z0 = 0.0
            self._state.balance_z1 = 0.0
            self._state.balance_z2 = 0.0
            self._state.history.clear()
            self._on_state_change(self._state)
            dialogs.show_message(self._root, "Reinicio", "Todos los saldos han sido reiniciados.",
                                 self._colors["accent4"], self._colors, self._fonts)

    def _show_history(self) -> None:
        if not self._state.history:
            dialogs.show_message(self._root, "Historial", "No hay partidas registradas aún.",
                                 self._colors["accent2"], self._colors, self._fonts)
            return
        dialogs.HistoryWindow(
            self._root, self._state.history, self._colors, self._fonts,
            lambda: self._export_history(self._state.history),
        )

    def _export_history(self, history: list[str]) -> None:
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Guardar historial como",
        )
        if not filename:
            return
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("HISTORIAL DE PARTIDAS HABBO\n" + "=" * 50 + "\n\n")
                for i, entry in enumerate(history, 1):
                    f.write(f"Partida #{i}:\n{entry}\n\n" + "-" * 40 + "\n\n")
            dialogs.show_message(self._root, "Éxito", f"Historial exportado a {filename}",
                                 self._colors["accent4"], self._colors, self._fonts)
        except OSError as e:
            self._show_error(str(e))

    def _import_balances(self) -> None:
        filename = filedialog.askopenfilename(
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Abrir archivo de saldos",
        )
        if not filename:
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = f.read()
            for line in data.split("\n"):
                try:
                    if "(Inter):" in line:
                        self._balance_z0.set(float(line.split(":")[1].strip()))
                    elif "(Z1):" in line:
                        self._balance_z1.set(float(line.split(":")[1].strip()))
                    elif "(Z2):" in line:
                        self._balance_z2.set(float(line.split(":")[1].strip()))
                except (ValueError, IndexError):
                    pass
            dialogs.show_message(self._root, "Importación", "Archivo importado correctamente.",
                                 self._colors["accent4"], self._colors, self._fonts)
        except OSError as e:
            self._show_error(str(e))

    def _export_balances(self) -> None:
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Guardar saldos como",
        )
        if not filename:
            return
        try:
            s = self._state
            with open(filename, "w", encoding="utf-8") as f:
                f.write("SALDOS ACTUALES HABBO:\n\n")
                f.write(f"{s.name_z0} (Inter): {s.balance_z0}\n")
                f.write(f"{s.name_z1} (Z1): {s.balance_z1}\n")
                f.write(f"{s.name_z2} (Z2): {s.balance_z2}\n")
                if s.history:
                    f.write(f"\n{'='*20}\nHISTORIAL COMPLETO:\n")
                    for entry in s.history:
                        f.write(f"\n{entry}\n")
            dialogs.show_message(self._root, "Éxito", f"Saldos exportados a {filename}",
                                 self._colors["accent4"], self._colors, self._fonts)
        except OSError as e:
            self._show_error(str(e))

    def _show_error(self, message: str) -> None:
        dialogs.show_message(self._root, "Error", message,
                             self._colors["accent1"], self._colors, self._fonts)
