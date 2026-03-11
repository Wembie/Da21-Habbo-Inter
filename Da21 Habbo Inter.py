import tkinter as tk
from tkinter import filedialog, ttk, font
from datetime import datetime
import json
import os


class CuentaApp:
    PLACEHOLDER_NOTAS = "Escribe tus notas personales aquí...\n\nPuedes guardar y cargar tus notas con los botones de abajo."
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

        self.saldo_z0 = tk.DoubleVar()
        self.saldo_z1 = tk.DoubleVar()
        self.saldo_z2 = tk.DoubleVar()
        self.nombre_z0 = tk.StringVar(value="Inter")
        self.nombre_z1 = tk.StringVar(value="Jugador 1")
        self.nombre_z2 = tk.StringVar(value="Jugador 2")
        self.juego_var = tk.DoubleVar()
        self.dinero_real_var = tk.BooleanVar()
        self.usdt_var = tk.BooleanVar()
        self.historial_partidas = []

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
        self.cargar_autosave()
        self.actualizar_notepad()

    def center_window(self):
        """Center the main window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def cargar_autosave(self):
        """Load autosaved state if available"""
        if os.path.exists(self.AUTOSAVE_FILE):
            try:
                with open(self.AUTOSAVE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.saldo_z0.set(data.get("z0", 0.0))
                self.saldo_z1.set(data.get("z1", 0.0))
                self.saldo_z2.set(data.get("z2", 0.0))
                self.nombre_z0.set(data.get("nombre_z0", "Inter"))
                self.nombre_z1.set(data.get("nombre_z1", "Jugador 1"))
                self.nombre_z2.set(data.get("nombre_z2", "Jugador 2"))
                self.historial_partidas = data.get("historial", [])
            except (json.JSONDecodeError, KeyError, OSError):
                pass

    def guardar_autosave(self):
        """Save current state automatically"""
        try:
            data = {
                "z0": self.saldo_z0.get(),
                "z1": self.saldo_z1.get(),
                "z2": self.saldo_z2.get(),
                "nombre_z0": self.nombre_z0.get(),
                "nombre_z1": self.nombre_z1.get(),
                "nombre_z2": self.nombre_z2.get(),
                "historial": self.historial_partidas,
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
        self.create_player_row(balance_frame, "(Inter)", self.nombre_z0, self.saldo_z0, 1)
        self.create_player_row(balance_frame, "(Z1)", self.nombre_z1, self.saldo_z1, 2)
        self.create_player_row(balance_frame, "(Z2)", self.nombre_z2, self.saldo_z2, 3)

        self.saldo_z0.set(0.0)
        self.saldo_z1.set(0.0)
        self.saldo_z2.set(0.0)

        self.create_section_title(main_frame, "JUEGO", 1, 0, colspan=2)
        self.create_label_entry(main_frame, "Monto del juego:", self.juego_var, 2, 0, colspan=2)

        payment_frame = ttk.LabelFrame(main_frame, text="TIPO DE PAGO", style="TLabelframe")
        payment_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

        self.create_styled_checkbox(payment_frame, "Dinero Real", self.dinero_real_var, 0, 0)
        self.create_styled_checkbox(payment_frame, "USDT", self.usdt_var, 0, 1)

        self.create_section_title(main_frame, "RESULTADO", 4, 0, colspan=2)

        game_frame = ttk.Frame(main_frame)
        game_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
        game_frame.columnconfigure(0, weight=1)
        game_frame.columnconfigure(1, weight=1)

        self.create_styled_button(game_frame, "Z1 GANA", lambda: self.actualizar_saldos("z1"),
                                  0, 0, color=self.colors["accent2"])
        self.create_styled_button(game_frame, "Z2 GANA", lambda: self.actualizar_saldos("z2"),
                                  0, 1, color=self.colors["accent2"])

        self.create_section_title(main_frame, "ACCIONES", 6, 0, colspan=2)

        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)

        self.create_styled_button(action_frame, "HISTORIAL", self.mostrar_historial,
                                  0, 0, color=self.colors["accent4"])
        self.create_styled_button(action_frame, "RESET", self.resetear,
                                  0, 1, color=self.colors["accent1"])

        io_frame = ttk.Frame(main_frame)
        io_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")
        io_frame.columnconfigure(0, weight=1)
        io_frame.columnconfigure(1, weight=1)

        self.create_styled_button(io_frame, "IMPORTAR SALDOS", self.importar_saldos,
                                  0, 0, color=self.colors["accent3"])
        self.create_styled_button(io_frame, "EXPORTAR SALDOS", self.exportar_saldos,
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

        self.create_notepad_frame(notepad_container, "SALDOS", 0, "saldos")
        self.create_notepad_frame(notepad_container, "NOTAS PERSONALES", 1, "notas")

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

        if notepad_type == "notas":
            self.personal_notepad = notepad

            buttons_frame = ttk.Frame(notepad_frame)
            buttons_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
            buttons_frame.columnconfigure(0, weight=1)
            buttons_frame.columnconfigure(1, weight=1)

            self.create_styled_button(buttons_frame, "GUARDAR NOTAS", self.guardar_notas_personales,
                                      0, 0, color=self.colors["accent4"])
            self.create_styled_button(buttons_frame, "CARGAR NOTAS", self.cargar_notas_personales,
                                      0, 1, color=self.colors["accent3"])

            # Placeholder behavior
            self.personal_notepad.insert(tk.END, self.PLACEHOLDER_NOTAS)
            self.personal_notepad.config(fg="#888888")
            self.personal_notepad.bind("<FocusIn>", self._on_notas_focus_in)
            self.personal_notepad.bind("<FocusOut>", self._on_notas_focus_out)
        else:
            self.notepad = notepad

    def _on_notas_focus_in(self, _):
        """Clear placeholder text when focused"""
        if self.personal_notepad.get("1.0", tk.END).strip() == self.PLACEHOLDER_NOTAS.strip():
            self.personal_notepad.delete("1.0", tk.END)
            self.personal_notepad.config(fg=self.colors["foreground"])

    def _on_notas_focus_out(self, _):
        """Restore placeholder if empty"""
        if not self.personal_notepad.get("1.0", tk.END).strip():
            self.personal_notepad.insert(tk.END, self.PLACEHOLDER_NOTAS)
            self.personal_notepad.config(fg="#888888")

    def create_section_title(self, parent, text, row, col, colspan=1):
        title = tk.Label(parent, text=text, font=self.header_font,
                         fg=self.colors["accent2"], bg=self.colors["panel"],
                         pady=5)
        title.grid(row=row, column=col, columnspan=colspan, sticky="w")

    def create_player_row(self, parent, tag, nombre_var, saldo_var, row):
        """Create a row with an editable name field and a balance field"""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=2)
        frame.columnconfigure(1, weight=2)
        frame.columnconfigure(3, weight=3)

        tk.Label(frame, text=tag, font=self.text_font,
                 fg=self.colors["accent3"], bg=self.colors["panel"], anchor="w"
                 ).grid(row=0, column=0, padx=(5, 2), pady=2, sticky="w")

        tk.Entry(frame, textvariable=nombre_var, font=self.text_font,
                 bg=self.colors["input"], fg=self.colors["foreground"],
                 insertbackground=self.colors["foreground"],
                 relief=tk.FLAT, bd=2, width=12
                 ).grid(row=0, column=1, padx=(0, 10), pady=2, sticky="ew")

        tk.Label(frame, text="Saldo:", font=self.text_font,
                 fg=self.colors["foreground"], bg=self.colors["panel"], anchor="w"
                 ).grid(row=0, column=2, padx=(5, 2), pady=2, sticky="w")

        tk.Entry(frame, textvariable=saldo_var, font=self.text_font,
                 bg=self.colors["input"], fg=self.colors["foreground"],
                 insertbackground=self.colors["foreground"],
                 relief=tk.FLAT, bd=2
                 ).grid(row=0, column=3, padx=5, pady=2, sticky="ew")

        saldo_var.trace_add("write", self.actualizar_notepad)
        nombre_var.trace_add("write", self.actualizar_notepad)

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

        if variable in [self.saldo_z0, self.saldo_z1, self.saldo_z2]:
            variable.trace_add("write", self.actualizar_notepad)

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

    def actualizar_notepad(self, *args):
        try:
            self.notepad.delete("1.0", tk.END)
            self.notepad.insert(tk.END, "SALDOS ACTUALES:\n\n")
            self.notepad.insert(tk.END, f"{self.nombre_z0.get()} (Inter): {self.saldo_z0.get()}\n")
            self.notepad.insert(tk.END, f"{self.nombre_z1.get()} (Z1): {self.saldo_z1.get()}\n")
            self.notepad.insert(tk.END, f"{self.nombre_z2.get()} (Z2): {self.saldo_z2.get()}\n")

            if self.historial_partidas:
                self.notepad.insert(tk.END, f"\n{'='*20}\n")
                self.notepad.insert(tk.END, "ÚLTIMAS PARTIDAS:\n")
                for partida in self.historial_partidas[-5:]:
                    self.notepad.insert(tk.END, f"\n{partida}\n")
        except AttributeError:
            pass

    def check_checkbox(self, clicked_var):
        """Ensure only one payment option is selected (mutual exclusion)"""
        if clicked_var is self.dinero_real_var and self.dinero_real_var.get():
            self.usdt_var.set(False)
        elif clicked_var is self.usdt_var and self.usdt_var.get():
            self.dinero_real_var.set(False)

    def actualizar_saldos(self, ganador):
        try:
            monto_juego = self.juego_var.get()
        except tk.TclError:
            self.mostrar_mensaje_error("Error", "El monto del juego no es válido.")
            return

        if self.usdt_var.get():
            if monto_juego < 1.0:
                self.mostrar_mensaje_error("Error", "El monto del juego debe ser al menos 1 USDT.")
                return
            propina = self.calcular_propina_usdt(monto_juego)
        else:
            if monto_juego < 5.0:
                self.mostrar_mensaje_error("Error", "El monto del juego debe ser al menos 5 créditos.")
                return
            if self.dinero_real_var.get():
                propina = round(monto_juego * 0.1, 2)
            else:
                propina = self.calcular_propina(monto_juego)

        saldo_z0_inicial = self.saldo_z0.get()
        saldo_z1_inicial = self.saldo_z1.get()
        saldo_z2_inicial = self.saldo_z2.get()

        if ganador == "z1":
            nuevo_z0 = round(saldo_z0_inicial + propina, 2)
            nuevo_z1 = round(saldo_z1_inicial + monto_juego - propina, 2)
            nuevo_z2 = round(saldo_z2_inicial - monto_juego, 2)
        else:
            nuevo_z0 = round(saldo_z0_inicial + propina, 2)
            nuevo_z1 = round(saldo_z1_inicial - monto_juego, 2)
            nuevo_z2 = round(saldo_z2_inicial + monto_juego - propina, 2)

        self.saldo_z0.set(nuevo_z0)
        self.saldo_z1.set(nuevo_z1)
        self.saldo_z2.set(nuevo_z2)

        currency = "USDT" if self.usdt_var.get() else ("$" if self.dinero_real_var.get() else "C")
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

        n0 = self.nombre_z0.get()
        n1 = self.nombre_z1.get()
        n2 = self.nombre_z2.get()
        nombre_ganador = f"{n1} (Z1)" if ganador == "z1" else f"{n2} (Z2)"

        partida = (
            f"[{timestamp}] Ganador: {nombre_ganador}\n"
            f"Monto: {monto_juego} {currency}\n"
            f"Propina: {propina} {currency}\n"
            f"Saldos: {n0}={nuevo_z0}, {n1}={nuevo_z1}, {n2}={nuevo_z2}"
        )

        self.historial_partidas.append(partida)
        self.actualizar_notepad()
        self.guardar_autosave()

        self.mostrar_mensaje_exito(
            "Partida Registrada",
            f"Ganador: {nombre_ganador}\n"
            f"Monto: {monto_juego} {currency}\n"
            f"Propina: {propina} {currency}"
        )

    def calcular_propina(self, monto_juego):
        if 5.0 <= monto_juego < 10.0:
            return 2.0
        elif 10.0 <= monto_juego < 15.0:
            return 3.0
        elif 15.0 <= monto_juego < 20.0:
            return 4.0
        elif 20.0 <= monto_juego < 26.0:
            return 5.0
        elif 26.0 <= monto_juego < 31.0:
            return 6.0
        elif 31.0 <= monto_juego < 36.0:
            return 7.0
        elif 36.0 <= monto_juego < 41.0:
            return 8.0
        elif 41.0 <= monto_juego < 50.0:
            return 9.0
        elif 50.0 <= monto_juego < 100.0:
            return 10.0
        elif 100.0 <= monto_juego < 150.0:
            return 20.0
        elif 150.0 <= monto_juego < 500.0:
            return 30.0
        else:
            return round(50.0 * (monto_juego // 500.0), 2)

    def calcular_propina_usdt(self, monto_juego):
        if 1.0 <= monto_juego < 10.0:
            return 0.5
        else:
            return round((monto_juego // 10.0), 2)

    def resetear(self):
        if self.mostrar_mensaje_confirmacion("Confirmar", "¿Estás seguro de reiniciar todos los saldos y el historial?"):
            self.saldo_z0.set(0.0)
            self.saldo_z1.set(0.0)
            self.saldo_z2.set(0.0)
            self.juego_var.set(0.0)
            self.historial_partidas.clear()
            self.actualizar_notepad()
            self.guardar_autosave()
            self.mostrar_mensaje_exito("Reinicio", "Todos los saldos han sido reiniciados.")

    def mostrar_historial(self):
        if not self.historial_partidas:
            self.mostrar_mensaje_info("Historial", "No hay partidas registradas aún.")
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

        for i, partida in enumerate(self.historial_partidas, 1):
            hist_text.insert(tk.END, f"Partida #{i}:\n", "subheader")
            hist_text.insert(tk.END, f"{partida}\n\n", "normal")
            hist_text.insert(tk.END, "-" * 40 + "\n\n", "separator")

        button_frame = ttk.Frame(hist_container)
        button_frame.pack(pady=10, fill=tk.X)
        button_frame.columnconfigure(0, weight=1)

        self.create_styled_button(button_frame, "EXPORTAR HISTORIAL",
                                  lambda: self.exportar_historial(self.historial_partidas),
                                  0, 0, color=self.colors["accent3"])

    def exportar_historial(self, historial):
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
                    for i, partida in enumerate(historial, 1):
                        file.write(f"Partida #{i}:\n{partida}\n\n")
                        file.write("-" * 40 + "\n\n")
                self.mostrar_mensaje_exito("Éxito", f"Historial exportado a {filename}")
            except OSError as e:
                self.mostrar_mensaje_error("Error", f"Error al exportar historial: {str(e)}")

    def importar_saldos(self):
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
                        if "Inter (Z0):" in line:
                            self.saldo_z0.set(float(line.split(":")[1].strip()))
                        elif "Jugador 1 (Z1):" in line:
                            self.saldo_z1.set(float(line.split(":")[1].strip()))
                        elif "Jugador 2 (Z2):" in line:
                            self.saldo_z2.set(float(line.split(":")[1].strip()))
                    except (ValueError, IndexError):
                        pass

                self.mostrar_mensaje_exito("Importación", "Archivo importado correctamente.")
            except OSError as e:
                self.mostrar_mensaje_error("Error", f"Error al importar archivo: {str(e)}")

    def exportar_saldos(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Guardar saldos como"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write("SALDOS ACTUALES HABBO:\n\n")
                    file.write(f"{self.nombre_z0.get()} (Inter): {self.saldo_z0.get()}\n")
                    file.write(f"{self.nombre_z1.get()} (Z1): {self.saldo_z1.get()}\n")
                    file.write(f"{self.nombre_z2.get()} (Z2): {self.saldo_z2.get()}\n")

                    if self.historial_partidas:
                        file.write(f"\n{'='*20}\n")
                        file.write("HISTORIAL COMPLETO:\n")
                        for partida in self.historial_partidas:
                            file.write(f"\n{partida}\n")

                self.mostrar_mensaje_exito("Éxito", f"Saldos exportados a {filename}")
            except OSError as e:
                self.mostrar_mensaje_error("Error", f"Error al exportar archivo: {str(e)}")

    def guardar_notas_personales(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Guardar notas como"
        )
        if filename:
            try:
                content = self.personal_notepad.get("1.0", tk.END)
                if content.strip() == self.PLACEHOLDER_NOTAS.strip():
                    content = ""
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.mostrar_mensaje_exito("Éxito", f"Notas guardadas en {filename}")
            except OSError as e:
                self.mostrar_mensaje_error("Error", f"Error al guardar notas: {str(e)}")

    def cargar_notas_personales(self):
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
                self.mostrar_mensaje_exito("Carga Exitosa", f"Notas cargadas desde {filename}")
            except OSError as e:
                self.mostrar_mensaje_error("Error", f"Error al cargar notas: {str(e)}")

    def mostrar_mensaje_error(self, titulo, mensaje):
        self.mostrar_mensaje_personalizado(titulo, mensaje, "#FF5F5D")

    def mostrar_mensaje_exito(self, titulo, mensaje):
        self.mostrar_mensaje_personalizado(titulo, mensaje, "#06D6A0")

    def mostrar_mensaje_info(self, titulo, mensaje):
        self.mostrar_mensaje_personalizado(titulo, mensaje, "#3BBFEF")

    def mostrar_mensaje_confirmacion(self, titulo, mensaje):
        dialog = tk.Toplevel(self.root)
        dialog.title(titulo)
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

        message_label = tk.Label(dialog, text=mensaje, font=self.text_font,
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

    def mostrar_mensaje_personalizado(self, titulo, mensaje, color_acento):
        dialog = tk.Toplevel(self.root)
        dialog.title(titulo)
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

        header = tk.Frame(dialog, bg=color_acento, height=10)
        header.pack(fill=tk.X)

        title_label = tk.Label(dialog, text=titulo, font=self.header_font,
                               bg=self.colors["panel"], fg=color_acento)
        title_label.pack(pady=(20, 10))

        message_label = tk.Label(dialog, text=mensaje, font=self.text_font,
                                 bg=self.colors["panel"], fg=self.colors["foreground"],
                                 wraplength=350, justify=tk.CENTER)
        message_label.pack(pady=10, padx=20)

        ok_button = tk.Button(
            dialog, text="ACEPTAR", font=self.text_font,
            bg=color_acento, fg=self.colors["foreground"],
            activebackground=self.darken_color(color_acento),
            activeforeground=self.colors["foreground"],
            relief=tk.FLAT, borderwidth=0, padx=25, pady=8,
            command=dialog.destroy
        )
        ok_button.pack(pady=20)

        ok_button.bind("<Enter>", lambda e, b=ok_button, c=color_acento: self.on_hover(b, c))
        ok_button.bind("<Leave>", lambda e, b=ok_button, c=color_acento: self.on_leave(b, c))


if __name__ == "__main__":
    root = tk.Tk()
    app = CuentaApp(root)
    root.mainloop()
