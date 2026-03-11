import tkinter as tk
from tkinter import filedialog, ttk, font
from datetime import datetime
import json
import os


class CuentaApp:
    NOTES_PLACEHOLDER = "Escribe tus notas personales aquí...\n\nPuedes guardar y cargar tus notas con los botones de abajo."
    AUTOSAVE_FILE = "da21_autosave.json"

    def __init__(self, root):
        self.root = root
        self.root.title("Da21 Habbo Intear")
        self.root.geometry("1000x750")
        self.root.configure(bg="#202A44")

        self.colors = {
            "background": "#202A44",
            "foreground": "#FFFFFF",
            "accent1": "#FF5F5D",
            "accent2": "#3BBFEF",
            "accent3": "#FFD166",
            "accent4": "#06D6A0",
            "panel": "#2A3655",
            "border": "#3BBFEF",
            "input": "#2F3B5C",
        }

        self.balance_z0 = tk.DoubleVar()
        self.balance_z1 = tk.DoubleVar()
        self.balance_z2 = tk.DoubleVar()
        self.name_z0 = tk.StringVar(value="Inter")
        self.name_z1 = tk.StringVar(value="Jugador 1")
        self.name_z2 = tk.StringVar(value="Jugador 2")
        self.game_var = tk.DoubleVar()
        self.real_money_var = tk.BooleanVar()
        self.usdt_var = tk.BooleanVar()
        self.game_history = []

        self.title_font = font.Font(family="Segoe UI", size=14, weight="bold")
        self.header_font = font.Font(family="Segoe UI", size=12, weight="bold")
        self.text_font = font.Font(family="Segoe UI", size=10)
        self.small_font = font.Font(family="Segoe UI", size=8)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure("TLabelframe", background=self.colors["panel"], foreground=self.colors["foreground"])
        self.style.configure("TLabelframe.Label", background=self.colors["panel"], foreground=self.colors["foreground"], font=self.header_font)
        self.style.configure("TButton", background=self.colors["accent1"], foreground=self.colors["foreground"], font=self.text_font)

        self.main_container = ttk.Frame(self.root, padding="10 10 10 10", style="TFrame")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.columnconfigure(1, weight=1)
        self.main_container.rowconfigure(0, weight=1)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.create_widgets()
        self.create_notepad_section()
        self.center_window()
        self.load_autosave()
        self.update_notepad()

    def center_window(self):
        """Center the main window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def load_autosave(self):
        """Load autosaved state if available"""
        if os.path.exists(self.AUTOSAVE_FILE):
            try:
                with open(self.AUTOSAVE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.balance_z0.set(data.get("z0", 0.0))
                self.balance_z1.set(data.get("z1", 0.0))
                self.balance_z2.set(data.get("z2", 0.0))
                self.name_z0.set(data.get("name_z0", "Inter"))
                self.name_z1.set(data.get("name_z1", "Jugador 1"))
                self.name_z2.set(data.get("name_z2", "Jugador 2"))
                self.game_history = data.get("history", [])
            except (json.JSONDecodeError, KeyError, OSError):
                pass

    def save_autosave(self):
        """Save current state automatically"""
        try:
            data = {
                "z0": self.balance_z0.get(),
                "z1": self.balance_z1.get(),
                "z2": self.balance_z2.get(),
                "name_z0": self.name_z0.get(),
                "name_z1": self.name_z1.get(),
                "name_z2": self.name_z2.get(),
                "history": self.game_history,
            }
            with open(self.AUTOSAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def create_widgets(self):
        main_frame = ttk.LabelFrame(self.main_container, text="CONTROLES", padding="10 10 10 10", style="TLabelframe")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        for i in range(10):
            main_frame.rowconfigure(i, pad=5)
        main_frame.columnconfigure(0, pad=10)
        main_frame.columnconfigure(1, pad=10)

        balance_frame = ttk.Frame(main_frame)
        balance_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)

        self.create_section_title(balance_frame, "SALDOS", 0, 0, colspan=2)
        self.create_player_row(balance_frame, "(Inter)", self.name_z0, self.balance_z0, 1)
        self.create_player_row(balance_frame, "(Z1)", self.name_z1, self.balance_z1, 2)
        self.create_player_row(balance_frame, "(Z2)", self.name_z2, self.balance_z2, 3)

        self.balance_z0.set(0.0)
        self.balance_z1.set(0.0)
        self.balance_z2.set(0.0)

        self.create_section_title(main_frame, "JUEGO", 1, 0, colspan=2)
        self.create_label_entry(main_frame, "Monto del juego:", self.game_var, 2, 0, colspan=2)

        payment_frame = ttk.LabelFrame(main_frame, text="TIPO DE PAGO", style="TLabelframe")
        payment_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

        self.create_styled_checkbox(payment_frame, "Dinero Real", self.real_money_var, 0, 0)
        self.create_styled_checkbox(payment_frame, "USDT", self.usdt_var, 0, 1)

        self.create_section_title(main_frame, "RESULTADO", 4, 0, colspan=2)

        game_frame = ttk.Frame(main_frame)
        game_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
        game_frame.columnconfigure(0, weight=1)
        game_frame.columnconfigure(1, weight=1)

        self.create_styled_button(game_frame, "Z1 GANA", lambda: self.update_balances("z1"),
                                  0, 0, color=self.colors["accent2"])
        self.create_styled_button(game_frame, "Z2 GANA", lambda: self.update_balances("z2"),
                                  0, 1, color=self.colors["accent2"])

        self.create_section_title(main_frame, "ACCIONES", 6, 0, colspan=2)

        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)

        self.create_styled_button(action_frame, "HISTORIAL", self.show_history,
                                  0, 0, color=self.colors["accent4"])
        self.create_styled_button(action_frame, "RESET", self.reset,
                                  0, 1, color=self.colors["accent1"])

        io_frame = ttk.Frame(main_frame)
        io_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")
        io_frame.columnconfigure(0, weight=1)
        io_frame.columnconfigure(1, weight=1)

        self.create_styled_button(io_frame, "IMPORTAR SALDOS", self.import_balances,
                                  0, 0, color=self.colors["accent3"])
        self.create_styled_button(io_frame, "EXPORTAR SALDOS", self.export_balances,
                                  0, 1, color=self.colors["accent3"])

        credit_label = tk.Label(main_frame, text="Developed By _Acos_ / Wembie",
                                font=self.small_font, fg=self.colors["foreground"], bg=self.colors["panel"])
        credit_label.grid(row=9, column=0, columnspan=2, pady=(15, 0))

    def create_notepad_section(self):
        notepad_container = ttk.Frame(self.main_container, style="TFrame")
        notepad_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        notepad_container.rowconfigure(0, weight=1)
        notepad_container.rowconfigure(1, weight=1)
        notepad_container.columnconfigure(0, weight=1)

        self.create_notepad_frame(notepad_container, "SALDOS", 0, "balances")
        self.create_notepad_frame(notepad_container, "NOTAS PERSONALES", 1, "notes")

    def create_notepad_frame(self, parent, title, row, notepad_type):
        notepad_frame = ttk.LabelFrame(parent, text=title, style="TLabelframe")
        notepad_frame.grid(row=row, column=0, padx=5, pady=5, sticky="nsew")
        notepad_frame.columnconfigure(0, weight=1)
        notepad_frame.rowconfigure(0, weight=1)

        text_frame = ttk.Frame(notepad_frame)
        text_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        notepad = tk.Text(text_frame, wrap=tk.WORD, font=self.text_font,
                          bg=self.colors["input"], fg=self.colors["foreground"],
                          insertbackground=self.colors["foreground"],
                          selectbackground=self.colors["accent2"], relief=tk.FLAT)
        notepad.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(text_frame, command=notepad.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        notepad.config(yscrollcommand=scrollbar.set)

        if notepad_type == "notes":
            self.personal_notepad = notepad

            buttons_frame = ttk.Frame(notepad_frame)
            buttons_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
            buttons_frame.columnconfigure(0, weight=1)
            buttons_frame.columnconfigure(1, weight=1)

            self.create_styled_button(buttons_frame, "GUARDAR NOTAS", self.save_personal_notes,
                                      0, 0, color=self.colors["accent4"])
            self.create_styled_button(buttons_frame, "CARGAR NOTAS", self.load_personal_notes,
                                      0, 1, color=self.colors["accent3"])

            self.personal_notepad.insert(tk.END, self.NOTES_PLACEHOLDER)
            self.personal_notepad.config(fg="#888888")
            self.personal_notepad.bind("<FocusIn>", self._on_notes_focus_in)
            self.personal_notepad.bind("<FocusOut>", self._on_notes_focus_out)
        else:
            self.notepad = notepad

    def _on_notes_focus_in(self, _):
        """Clear placeholder text when focused"""
        if self.personal_notepad.get("1.0", tk.END).strip() == self.NOTES_PLACEHOLDER.strip():
            self.personal_notepad.delete("1.0", tk.END)
            self.personal_notepad.config(fg=self.colors["foreground"])

    def _on_notes_focus_out(self, _):
        """Restore placeholder if empty"""
        if not self.personal_notepad.get("1.0", tk.END).strip():
            self.personal_notepad.insert(tk.END, self.NOTES_PLACEHOLDER)
            self.personal_notepad.config(fg="#888888")

    def create_section_title(self, parent, text, row, col, colspan=1):
        title = tk.Label(parent, text=text, font=self.header_font,
                         fg=self.colors["accent2"], bg=self.colors["panel"],
                         pady=5)
        title.grid(row=row, column=col, columnspan=colspan, sticky="w")

    def create_player_row(self, parent, tag, name_var, balance_var, row):
        """Create a row with an editable name field and a balance field"""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=2)
        frame.columnconfigure(1, weight=2)
        frame.columnconfigure(3, weight=3)

        tk.Label(frame, text=tag, font=self.text_font,
                 fg=self.colors["accent3"], bg=self.colors["panel"], anchor="w"
                 ).grid(row=0, column=0, padx=(5, 2), pady=2, sticky="w")

        tk.Entry(frame, textvariable=name_var, font=self.text_font,
                 bg=self.colors["input"], fg=self.colors["foreground"],
                 insertbackground=self.colors["foreground"],
                 relief=tk.FLAT, bd=2, width=12
                 ).grid(row=0, column=1, padx=(0, 10), pady=2, sticky="ew")

        tk.Label(frame, text="Saldo:", font=self.text_font,
                 fg=self.colors["foreground"], bg=self.colors["panel"], anchor="w"
                 ).grid(row=0, column=2, padx=(5, 2), pady=2, sticky="w")

        tk.Entry(frame, textvariable=balance_var, font=self.text_font,
                 bg=self.colors["input"], fg=self.colors["foreground"],
                 insertbackground=self.colors["foreground"],
                 relief=tk.FLAT, bd=2
                 ).grid(row=0, column=3, padx=5, pady=2, sticky="ew")

        balance_var.trace_add("write", self.update_notepad)
        name_var.trace_add("write", self.update_notepad)

    def create_label_entry(self, parent, text, variable, row, col, colspan=1):
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", pady=2)
        frame.columnconfigure(1, weight=1)

        label = tk.Label(frame, text=text, font=self.text_font,
                         fg=self.colors["foreground"], bg=self.colors["panel"],
                         anchor="w")
        label.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        entry = tk.Entry(frame, textvariable=variable, font=self.text_font,
                         bg=self.colors["input"], fg=self.colors["foreground"],
                         insertbackground=self.colors["foreground"],
                         relief=tk.FLAT, bd=2)
        entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        return entry

    def create_styled_checkbox(self, parent, text, variable, row, col):
        checkbox_frame = ttk.Frame(parent)
        checkbox_frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")

        checkbox = tk.Checkbutton(checkbox_frame, text=text, variable=variable,
                                  command=lambda v=variable: self.check_checkbox(v),
                                  font=self.text_font,
                                  fg=self.colors["foreground"], bg=self.colors["panel"],
                                  activebackground=self.colors["panel"],
                                  activeforeground=self.colors["accent2"],
                                  selectcolor=self.colors["panel"])
        checkbox.pack(anchor="w")

        return checkbox

    def create_styled_button(self, parent, text, command, row, col, color=None):
        if color is None:
            color = self.colors["accent1"]

        button = tk.Button(parent, text=text, command=command, font=self.text_font,
                           bg=color, fg=self.colors["foreground"],
                           activebackground=self.darken_color(color),
                           activeforeground=self.colors["foreground"],
                           relief=tk.FLAT, borderwidth=0, padx=15, pady=8)
        button.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        button.bind("<Enter>", lambda e, b=button, c=color: self.on_hover(b, c))
        button.bind("<Leave>", lambda e, b=button, c=color: self.on_leave(b, c))

        return button

    def on_hover(self, button, color):
        button.config(bg=self.lighten_color(color))

    def on_leave(self, button, color):
        button.config(bg=color)

    def lighten_color(self, hex_color, factor=0.2):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    def darken_color(self, hex_color, factor=0.2):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        return f"#{r:02x}{g:02x}{b:02x}"

    def update_notepad(self, *_):
        try:
            self.notepad.delete("1.0", tk.END)
            self.notepad.insert(tk.END, "SALDOS ACTUALES:\n\n")
            self.notepad.insert(tk.END, f"{self.name_z0.get()} (Inter): {self.balance_z0.get()}\n")
            self.notepad.insert(tk.END, f"{self.name_z1.get()} (Z1): {self.balance_z1.get()}\n")
            self.notepad.insert(tk.END, f"{self.name_z2.get()} (Z2): {self.balance_z2.get()}\n")

            if self.game_history:
                self.notepad.insert(tk.END, f"\n{'='*20}\n")
                self.notepad.insert(tk.END, "ÚLTIMAS PARTIDAS:\n")
                for game_entry in self.game_history[-5:]:
                    self.notepad.insert(tk.END, f"\n{game_entry}\n")
        except AttributeError:
            pass

    def check_checkbox(self, clicked_var):
        """Ensure only one payment option is selected (mutual exclusion)"""
        if clicked_var is self.real_money_var and self.real_money_var.get():
            self.usdt_var.set(False)
        elif clicked_var is self.usdt_var and self.usdt_var.get():
            self.real_money_var.set(False)

    def update_balances(self, winner):
        try:
            game_amount = self.game_var.get()
        except tk.TclError:
            self.show_error("Error", "El monto del juego no es válido.")
            return

        if self.usdt_var.get():
            if game_amount < 1.0:
                self.show_error("Error", "El monto del juego debe ser al menos 1 USDT.")
                return
            tip = self.calculate_tip_usdt(game_amount)
        else:
            if game_amount < 5.0:
                self.show_error("Error", "El monto del juego debe ser al menos 5 créditos.")
                return
            if self.real_money_var.get():
                tip = round(game_amount * 0.1, 2)
            else:
                tip = self.calculate_tip(game_amount)

        initial_z0 = self.balance_z0.get()
        initial_z1 = self.balance_z1.get()
        initial_z2 = self.balance_z2.get()

        if winner == "z1":
            new_z0 = round(initial_z0 + tip, 2)
            new_z1 = round(initial_z1 + game_amount - tip, 2)
            new_z2 = round(initial_z2 - game_amount, 2)
        else:
            new_z0 = round(initial_z0 + tip, 2)
            new_z1 = round(initial_z1 - game_amount, 2)
            new_z2 = round(initial_z2 + game_amount - tip, 2)

        self.balance_z0.set(new_z0)
        self.balance_z1.set(new_z1)
        self.balance_z2.set(new_z2)

        if self.usdt_var.get():
            payment_method = "USDT"
            currency = "USDT"
        elif self.real_money_var.get():
            payment_method = "Dinero Real"
            currency = "$"
        else:
            payment_method = "Créditos Habbo"
            currency = "C"

        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

        n0 = self.name_z0.get()
        n1 = self.name_z1.get()
        n2 = self.name_z2.get()
        winner_name = f"{n1} (Z1)" if winner == "z1" else f"{n2} (Z2)"

        game_entry = (
            f"[{timestamp}] Ganador: {winner_name}\n"
            f"Método: {payment_method}\n"
            f"Monto: {game_amount} {currency}\n"
            f"Propina: {tip} {currency}\n"
            f"Saldos: {n0}(Inter)={new_z0}, {n1}(Z1)={new_z1}, {n2}(Z2)={new_z2}"
        )

        self.game_history.append(game_entry)
        self.update_notepad()
        self.save_autosave()

        self.show_success(
            "Partida Registrada",
            f"Ganador: {winner_name}\n"
            f"Monto: {game_amount} {currency}\n"
            f"Propina: {tip} {currency}"
        )

    def calculate_tip(self, game_amount):
        if 5.0 <= game_amount < 10.0:
            return 2.0
        elif 10.0 <= game_amount < 15.0:
            return 3.0
        elif 15.0 <= game_amount < 20.0:
            return 4.0
        elif 20.0 <= game_amount < 26.0:
            return 5.0
        elif 26.0 <= game_amount < 31.0:
            return 6.0
        elif 31.0 <= game_amount < 36.0:
            return 7.0
        elif 36.0 <= game_amount < 41.0:
            return 8.0
        elif 41.0 <= game_amount < 50.0:
            return 9.0
        elif 50.0 <= game_amount < 100.0:
            return 10.0
        elif 100.0 <= game_amount < 150.0:
            return 20.0
        elif 150.0 <= game_amount < 500.0:
            return 30.0
        else:
            return round(50.0 * (game_amount // 500.0), 2)

    def calculate_tip_usdt(self, game_amount):
        if 1.0 <= game_amount < 10.0:
            return 0.5
        else:
            return round((game_amount // 10.0), 2)

    def reset(self):
        if self.show_confirmation("Confirmar", "¿Estás seguro de reiniciar todos los saldos y el historial?"):
            self.balance_z0.set(0.0)
            self.balance_z1.set(0.0)
            self.balance_z2.set(0.0)
            self.game_var.set(0.0)
            self.game_history.clear()
            self.update_notepad()
            self.save_autosave()
            self.show_success("Reinicio", "Todos los saldos han sido reiniciados.")

    def show_history(self):
        if not self.game_history:
            self.show_info("Historial", "No hay partidas registradas aún.")
            return

        hist_window = tk.Toplevel(self.root)
        hist_window.title("Historial de Partidas")
        hist_window.geometry("600x540")
        hist_window.configure(bg=self.colors["background"])

        hist_window.update_idletasks()
        w, h = hist_window.winfo_width(), hist_window.winfo_height()
        x = (hist_window.winfo_screenwidth() // 2) - (w // 2)
        y = (hist_window.winfo_screenheight() // 2) - (h // 2)
        hist_window.geometry(f"{w}x{h}+{x}+{y}")

        hist_container = ttk.Frame(hist_window, padding="10 10 10 10")
        hist_container.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(hist_container, text="HISTORIAL DE PARTIDAS",
                               font=self.title_font, fg=self.colors["accent2"],
                               bg=self.colors["background"])
        title_label.pack(pady=(0, 10))

        hist_frame = ttk.Frame(hist_container)
        hist_frame.pack(fill=tk.BOTH, expand=True)

        hist_text = tk.Text(hist_frame, wrap=tk.WORD, font=self.text_font,
                            bg=self.colors["input"], fg=self.colors["foreground"],
                            insertbackground=self.colors["foreground"],
                            relief=tk.FLAT)
        hist_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(hist_frame, command=hist_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        hist_text.config(yscrollcommand=scrollbar.set)

        hist_text.tag_configure("header", font=self.header_font, foreground=self.colors["accent2"])
        hist_text.tag_configure("subheader", font=self.header_font, foreground=self.colors["accent3"])
        hist_text.tag_configure("normal", font=self.text_font)
        hist_text.tag_configure("separator", font=self.text_font, foreground=self.colors["accent1"])

        hist_text.insert(tk.END, "HISTORIAL COMPLETO DE PARTIDAS\n", "header")
        hist_text.insert(tk.END, "=" * 50 + "\n\n", "separator")

        for i, game_entry in enumerate(self.game_history, 1):
            hist_text.insert(tk.END, f"Partida #{i}:\n", "subheader")
            hist_text.insert(tk.END, f"{game_entry}\n\n", "normal")
            hist_text.insert(tk.END, "-" * 40 + "\n\n", "separator")

        button_frame = ttk.Frame(hist_container)
        button_frame.pack(pady=10, fill=tk.X)
        button_frame.columnconfigure(0, weight=1)

        self.create_styled_button(button_frame, "EXPORTAR HISTORIAL",
                                  lambda: self.export_history(self.game_history),
                                  0, 0, color=self.colors["accent3"])

    def export_history(self, history):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Guardar historial como"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write("HISTORIAL DE PARTIDAS HABBO\n")
                    file.write("=" * 50 + "\n\n")
                    for i, game_entry in enumerate(history, 1):
                        file.write(f"Partida #{i}:\n{game_entry}\n\n")
                        file.write("-" * 40 + "\n\n")
                self.show_success("Éxito", f"Historial exportado a {filename}")
            except OSError as e:
                self.show_error("Error", f"Error al exportar historial: {str(e)}")

    def import_balances(self):
        filename = filedialog.askopenfilename(
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Abrir archivo de saldos"
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    data = file.read()
                self.notepad.delete("1.0", tk.END)
                self.notepad.insert(tk.END, data)

                for line in data.split('\n'):
                    try:
                        if "(Inter):" in line:
                            self.balance_z0.set(float(line.split(":")[1].strip()))
                        elif "(Z1):" in line:
                            self.balance_z1.set(float(line.split(":")[1].strip()))
                        elif "(Z2):" in line:
                            self.balance_z2.set(float(line.split(":")[1].strip()))
                    except (ValueError, IndexError):
                        pass

                self.show_success("Importación", "Archivo importado correctamente.")
            except OSError as e:
                self.show_error("Error", f"Error al importar archivo: {str(e)}")

    def export_balances(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Guardar saldos como"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write("SALDOS ACTUALES HABBO:\n\n")
                    file.write(f"{self.name_z0.get()} (Inter): {self.balance_z0.get()}\n")
                    file.write(f"{self.name_z1.get()} (Z1): {self.balance_z1.get()}\n")
                    file.write(f"{self.name_z2.get()} (Z2): {self.balance_z2.get()}\n")

                    if self.game_history:
                        file.write(f"\n{'='*20}\n")
                        file.write("HISTORIAL COMPLETO:\n")
                        for game_entry in self.game_history:
                            file.write(f"\n{game_entry}\n")

                self.show_success("Éxito", f"Saldos exportados a {filename}")
            except OSError as e:
                self.show_error("Error", f"Error al exportar archivo: {str(e)}")

    def save_personal_notes(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Guardar notas como"
        )
        if filename:
            try:
                content = self.personal_notepad.get("1.0", tk.END)
                if content.strip() == self.NOTES_PLACEHOLDER.strip():
                    content = ""
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.show_success("Éxito", f"Notas guardadas en {filename}")
            except OSError as e:
                self.show_error("Error", f"Error al guardar notas: {str(e)}")

    def load_personal_notes(self):
        filename = filedialog.askopenfilename(
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Abrir archivo de notas"
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.personal_notepad.delete("1.0", tk.END)
                self.personal_notepad.config(fg=self.colors["foreground"])
                self.personal_notepad.insert(tk.END, content)
                self.show_success("Carga Exitosa", f"Notas cargadas desde {filename}")
            except OSError as e:
                self.show_error("Error", f"Error al cargar notas: {str(e)}")

    def show_error(self, title, message):
        self.show_message(title, message, "#FF5F5D")

    def show_success(self, title, message):
        self.show_message(title, message, "#06D6A0")

    def show_info(self, title, message):
        self.show_message(title, message, "#3BBFEF")

    def show_confirmation(self, title, message):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x220")
        dialog.configure(bg=self.colors["panel"])
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        message_label = tk.Label(dialog, text=message, font=self.text_font,
                                 bg=self.colors["panel"], fg=self.colors["foreground"],
                                 wraplength=350, justify=tk.CENTER)
        message_label.pack(pady=(20, 30), padx=20)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        result = [False]

        yes_button = tk.Button(
            button_frame, text="SÍ", font=self.text_font,
            bg=self.colors["accent4"], fg=self.colors["foreground"],
            activebackground=self.darken_color(self.colors["accent4"]),
            activeforeground=self.colors["foreground"],
            relief=tk.FLAT, borderwidth=0, padx=15, pady=8,
            command=lambda: [result.__setitem__(0, True), dialog.destroy()]
        )
        yes_button.grid(row=0, column=0, padx=5, sticky="e")

        no_button = tk.Button(
            button_frame, text="NO", font=self.text_font,
            bg=self.colors["accent1"], fg=self.colors["foreground"],
            activebackground=self.darken_color(self.colors["accent1"]),
            activeforeground=self.colors["foreground"],
            relief=tk.FLAT, borderwidth=0, padx=15, pady=8,
            command=dialog.destroy
        )
        no_button.grid(row=0, column=1, padx=5, sticky="w")

        yes_button.bind("<Enter>", lambda e, b=yes_button, c=self.colors["accent4"]: self.on_hover(b, c))
        yes_button.bind("<Leave>", lambda e, b=yes_button, c=self.colors["accent4"]: self.on_leave(b, c))
        no_button.bind("<Enter>", lambda e, b=no_button, c=self.colors["accent1"]: self.on_hover(b, c))
        no_button.bind("<Leave>", lambda e, b=no_button, c=self.colors["accent1"]: self.on_leave(b, c))

        dialog.wait_window()
        return result[0]

    def show_message(self, title, message, accent_color):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x220")
        dialog.configure(bg=self.colors["panel"])
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        header = tk.Frame(dialog, bg=accent_color, height=10)
        header.pack(fill=tk.X)

        title_label = tk.Label(dialog, text=title, font=self.header_font,
                               bg=self.colors["panel"], fg=accent_color)
        title_label.pack(pady=(20, 10))

        message_label = tk.Label(dialog, text=message, font=self.text_font,
                                 bg=self.colors["panel"], fg=self.colors["foreground"],
                                 wraplength=350, justify=tk.CENTER)
        message_label.pack(pady=10, padx=20)

        ok_button = tk.Button(
            dialog, text="ACEPTAR", font=self.text_font,
            bg=accent_color, fg=self.colors["foreground"],
            activebackground=self.darken_color(accent_color),
            activeforeground=self.colors["foreground"],
            relief=tk.FLAT, borderwidth=0, padx=25, pady=8,
            command=dialog.destroy
        )
        ok_button.pack(pady=20)

        ok_button.bind("<Enter>", lambda e, b=ok_button, c=accent_color: self.on_hover(b, c))
        ok_button.bind("<Leave>", lambda e, b=ok_button, c=accent_color: self.on_leave(b, c))


if __name__ == "__main__":
    root = tk.Tk()
    app = CuentaApp(root)
    root.mainloop()
