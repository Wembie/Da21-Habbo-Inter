import tkinter as tk
from tkinter import filedialog, ttk, font
# Only import what's needed - no unnecessary imports

class CuentaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Da21 Habbo Intear")
        self.root.geometry("1000x750")  # Set a better initial size
        self.root.configure(bg="#202A44")
        
        # Define color scheme
        self.colors = {
            "background": "#202A44",  # Dark blue background
            "foreground": "#FFFFFF",  # White text
            "accent1": "#FF5F5D",     # Coral for important buttons
            "accent2": "#3BBFEF",     # Bright blue for game actions
            "accent3": "#FFD166",     # Gold for import/export
            "accent4": "#06D6A0",     # Mint green for positive actions
            "panel": "#2A3655",       # Slightly lighter blue for panels
            "border": "#3BBFEF"       # Border color
        }

        # Variables
        self.saldo_z0 = tk.DoubleVar()
        self.saldo_z1 = tk.DoubleVar()
        self.saldo_z2 = tk.DoubleVar()
        self.juego_var = tk.DoubleVar()
        self.dinero_real_var = tk.BooleanVar()
        self.usdt_var = tk.BooleanVar()
        self.historial_partidas = []
        
        # Store initial balances for history tracking
        self.saldos_iniciales = {"z0": 0.0, "z1": 0.0, "z2": 0.0}
        
        # Create custom fonts
        self.title_font = font.Font(family="Segoe UI", size=14, weight="bold")
        self.header_font = font.Font(family="Segoe UI", size=12, weight="bold")
        self.text_font = font.Font(family="Segoe UI", size=10)
        self.small_font = font.Font(family="Segoe UI", size=8)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure("TLabelframe", background=self.colors["panel"], foreground=self.colors["foreground"])
        self.style.configure("TLabelframe.Label", background=self.colors["panel"], foreground=self.colors["foreground"], font=self.header_font)
        self.style.configure("TButton", background=self.colors["accent1"], foreground=self.colors["foreground"], font=self.text_font)
        
        # Create the main container with padding
        self.main_container = ttk.Frame(self.root, padding="10 10 10 10", style="TFrame")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.columnconfigure(1, weight=1)
        self.main_container.rowconfigure(0, weight=1)
        
        # Make the window resizable
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create the interface
        self.create_widgets()
        self.create_notepad_section()
        
        # Update the notepad initially
        self.actualizar_notepad()

    def create_widgets(self):
        # Create a main frame for controls with rounded corners
        main_frame = ttk.LabelFrame(self.main_container, text="CONTROLES", padding="10 10 10 10", style="TLabelframe")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Custom styling for widgets in main frame
        for i in range(10):
            main_frame.rowconfigure(i, pad=5)
        main_frame.columnconfigure(0, pad=10)
        main_frame.columnconfigure(1, pad=10)
        
        # Balance section with custom labels
        balance_frame = ttk.Frame(main_frame)
        balance_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Title for balance section
        self.create_section_title(balance_frame, "SALDOS", 0, 0, colspan=2)
        
        # Labels and entries for saldos with custom styling
        self.create_label_entry(balance_frame, "Saldo Inter (Z0):", self.saldo_z0, 1, 0)
        self.create_label_entry(balance_frame, "Saldo Jugador 1 (Z1):", self.saldo_z1, 2, 0)
        self.create_label_entry(balance_frame, "Saldo Jugador 2 (Z2):", self.saldo_z2, 3, 0)

        # Set default values
        self.saldo_z0.set(0.0)
        self.saldo_z1.set(0.0)
        self.saldo_z2.set(0.0)
        
        # Game section
        self.create_section_title(main_frame, "JUEGO", 1, 0, colspan=2)
        
        # Game amount with styled label and entry
        self.create_label_entry(main_frame, "Monto del juego:", self.juego_var, 2, 0, colspan=2)

        # Checkboxes for payment type with an attractive frame
        payment_frame = ttk.LabelFrame(main_frame, text="TIPO DE PAGO", style="TLabelframe")
        payment_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=10)
        
        # Styled checkboxes
        self.create_styled_checkbox(payment_frame, "Dinero Real", self.dinero_real_var, 0, 0)
        self.create_styled_checkbox(payment_frame, "USDT", self.usdt_var, 0, 1)
        
        # Game outcome buttons with colorful styling
        self.create_section_title(main_frame, "RESULTADO", 4, 0, colspan=2)
        
        game_frame = ttk.Frame(main_frame)
        game_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
        game_frame.columnconfigure(0, weight=1)
        game_frame.columnconfigure(1, weight=1)
        
        self.create_styled_button(game_frame, "Z1 GANA", lambda: self.actualizar_saldos("z1"), 
                                 0, 0, color=self.colors["accent2"])
        self.create_styled_button(game_frame, "Z2 GANA", lambda: self.actualizar_saldos("z2"), 
                                 0, 1, color=self.colors["accent2"])

        # History and reset buttons
        self.create_section_title(main_frame, "ACCIONES", 6, 0, colspan=2)
        
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)
        
        self.create_styled_button(action_frame, "HISTORIAL", self.mostrar_historial, 
                                 0, 0, color=self.colors["accent4"])
        self.create_styled_button(action_frame, "RESET", self.resetear, 
                                 0, 1, color=self.colors["accent1"])

        # Import/Export buttons
        io_frame = ttk.Frame(main_frame)
        io_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")
        io_frame.columnconfigure(0, weight=1)
        io_frame.columnconfigure(1, weight=1)
        
        self.create_styled_button(io_frame, "IMPORTAR SALDOS", self.importar_saldos, 
                                 0, 0, color=self.colors["accent3"])
        self.create_styled_button(io_frame, "EXPORTAR SALDOS", self.exportar_saldos, 
                                 0, 1, color=self.colors["accent3"])
        
        # Credit label with custom styling
        credit_label = tk.Label(main_frame, text="Developed By _Acos_ / Wembie", 
                              font=self.small_font, fg=self.colors["foreground"], bg=self.colors["panel"])
        credit_label.grid(row=9, column=0, columnspan=2, pady=(15, 0))

    def create_notepad_section(self):
        # Create main frame for notepads
        notepad_container = ttk.Frame(self.main_container, style="TFrame")
        notepad_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        notepad_container.rowconfigure(0, weight=1)
        notepad_container.rowconfigure(1, weight=1)
        notepad_container.columnconfigure(0, weight=1)
        
        # First notepad for saldos
        self.create_notepad_frame(notepad_container, "SALDOS", 0, "saldos")
        
        # Second notepad for personal notes
        self.create_notepad_frame(notepad_container, "NOTAS PERSONALES", 1, "notas")

    def create_notepad_frame(self, parent, title, row, notepad_type):
        # Create LabelFrame for notepad
        notepad_frame = ttk.LabelFrame(parent, text=title, style="TLabelframe")
        notepad_frame.grid(row=row, column=0, padx=5, pady=5, sticky="nsew")
        notepad_frame.columnconfigure(0, weight=1)
        notepad_frame.rowconfigure(0, weight=1)
        
        # Create a frame to hold text and scrollbar
        text_frame = ttk.Frame(notepad_frame)
        text_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        # Notepad with scrollbar and custom styling
        notepad = tk.Text(text_frame, wrap=tk.WORD, font=self.text_font,
                        bg="#2F3B5C", fg=self.colors["foreground"], 
                        insertbackground=self.colors["foreground"],
                        selectbackground=self.colors["accent2"], relief=tk.FLAT)
        notepad.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(text_frame, command=notepad.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        notepad.config(yscrollcommand=scrollbar.set)
        
        # Add buttons frame for personal notes
        if notepad_type == "notas":
            self.personal_notepad = notepad
            
            # Add buttons for personal notes
            buttons_frame = ttk.Frame(notepad_frame)
            buttons_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
            
            self.create_styled_button(buttons_frame, "GUARDAR NOTAS", self.guardar_notas_personales, 
                                    0, 0, color=self.colors["accent4"])
            self.create_styled_button(buttons_frame, "CARGAR NOTAS", self.cargar_notas_personales, 
                                    0, 1, color=self.colors["accent3"])
            
            # Load placeholder text
            self.personal_notepad.insert(tk.END, "Escribe tus notas personales aquí...\n\n"
                                        "Puedes guardar y cargar tus notas con los botones de abajo.")
        else:
            self.notepad = notepad
            
    def create_section_title(self, parent, text, row, col, colspan=1):
        """Create styled section title"""
        title = tk.Label(parent, text=text, font=self.header_font, 
                       fg=self.colors["accent2"], bg=self.colors["panel"],
                       pady=5)
        title.grid(row=row, column=col, columnspan=colspan, sticky="w")
        
    def create_label_entry(self, parent, text, variable, row, col, colspan=1):
        """Create styled label and entry pair"""
        # Frame to hold label and entry
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", pady=2)
        frame.columnconfigure(1, weight=1)
        
        # Label
        label = tk.Label(frame, text=text, font=self.text_font, 
                       fg=self.colors["foreground"], bg=self.colors["panel"],
                       anchor="w")
        label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        
        # Entry with styling
        entry = tk.Entry(frame, textvariable=variable, font=self.text_font,
                       bg="#2F3B5C", fg=self.colors["foreground"],
                       insertbackground=self.colors["foreground"],
                       relief=tk.FLAT, bd=2)
        entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        # Add trace for saldo variables
        if variable in [self.saldo_z0, self.saldo_z1, self.saldo_z2]:
            variable.trace_add("write", self.actualizar_notepad)
            
        return entry
    
    def create_styled_checkbox(self, parent, text, variable, row, col):
        """Create a styled checkbox that looks modern"""
        checkbox_frame = ttk.Frame(parent)
        checkbox_frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")
        
        checkbox = tk.Checkbutton(checkbox_frame, text=text, variable=variable,
                                command=self.check_checkbox, font=self.text_font,
                                fg=self.colors["foreground"], bg=self.colors["panel"],
                                activebackground=self.colors["panel"],
                                activeforeground=self.colors["accent2"],
                                selectcolor=self.colors["panel"])
        checkbox.pack(anchor="w")
        
        return checkbox
        
    def create_styled_button(self, parent, text, command, row, col, color=None):
        """Create styled button with hover effect"""
        if color is None:
            color = self.colors["accent1"]
            
        button = tk.Button(parent, text=text, command=command, font=self.text_font,
                         bg=color, fg=self.colors["foreground"],
                         activebackground=self.darken_color(color),
                         activeforeground=self.colors["foreground"],
                         relief=tk.FLAT, borderwidth=0, padx=15, pady=8)
        button.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        # Add hover effect
        button.bind("<Enter>", lambda e, b=button, c=color: self.on_hover(b, c))
        button.bind("<Leave>", lambda e, b=button, c=color: self.on_leave(b, c))
        
        return button
    
    def on_hover(self, button, color):
        """Change button appearance on hover"""
        button.config(bg=self.lighten_color(color))
        
    def on_leave(self, button, color):
        """Restore button appearance when not hovering"""
        button.config(bg=color)
    
    def lighten_color(self, hex_color, factor=0.2):
        """Lighten the given color by factor"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def darken_color(self, hex_color, factor=0.2):
        """Darken the given color by factor"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        
        return f"#{r:02x}{g:02x}{b:02x}"

    def actualizar_notepad(self, *args):
        """Update the notepad with current balances"""
        try:
            self.notepad.delete("1.0", tk.END)
            self.notepad.insert(tk.END, f"SALDOS ACTUALES:\n\n")
            self.notepad.insert(tk.END, f"Inter (Z0): {self.saldo_z0.get()}\n")
            self.notepad.insert(tk.END, f"Jugador 1 (Z1): {self.saldo_z1.get()}\n")
            self.notepad.insert(tk.END, f"Jugador 2 (Z2): {self.saldo_z2.get()}\n")
            
            # Add history summary if available
            if self.historial_partidas:
                self.notepad.insert(tk.END, f"\n{'='*20}\n")
                self.notepad.insert(tk.END, f"ÚLTIMAS PARTIDAS:\n")
                
                # Show only last 5 games to keep it clean
                for partida in self.historial_partidas[-5:]:
                    self.notepad.insert(tk.END, f"\n{partida}\n")
        except:
            # Avoid errors when initializing
            pass

    def check_checkbox(self):
        """Ensure only one payment option is selected"""
        if self.dinero_real_var.get():
            self.usdt_var.set(False)
        elif self.usdt_var.get():
            self.dinero_real_var.set(False)

    def actualizar_saldos(self, ganador):
        """Update balances after a game"""
        try:
            monto_juego = self.juego_var.get()
            
            # Validate game amount
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
            
            # Store initial balances before updating
            saldo_z0_inicial = self.saldo_z0.get()
            saldo_z1_inicial = self.saldo_z1.get()
            saldo_z2_inicial = self.saldo_z2.get()
            
            # Calculate new balances
            if ganador == "z1":
                nuevo_z0 = round(saldo_z0_inicial + propina, 2)
                nuevo_z1 = round(saldo_z1_inicial + monto_juego - propina, 2)
                nuevo_z2 = round(saldo_z2_inicial - monto_juego, 2)
            else:  # z2 wins
                nuevo_z0 = round(saldo_z0_inicial + propina, 2)
                nuevo_z1 = round(saldo_z1_inicial - monto_juego, 2)
                nuevo_z2 = round(saldo_z2_inicial + monto_juego - propina, 2)
            
            # Update variables
            self.saldo_z0.set(nuevo_z0)
            self.saldo_z1.set(nuevo_z1)
            self.saldo_z2.set(nuevo_z2)
            
            # Format for currency display
            currency = "USDT" if self.usdt_var.get() else ("$" if self.dinero_real_var.get() else "C")
            
            # Create history entry with clear formatting and current balances
            partida = (
                f"Ganador: {'Jugador 1' if ganador=='z1' else 'Jugador 2'}\n"
                f"Monto: {monto_juego} {currency}\n"
                f"Propina: {propina} {currency}\n"
                f"Saldos: Z0={nuevo_z0}, Z1={nuevo_z1}, Z2={nuevo_z2}"
            )
            
            self.historial_partidas.append(partida)
            
            # Update the notepad
            self.actualizar_notepad()
            
            # Show success message
            self.mostrar_mensaje_exito(
                "Partida Registrada", 
                f"Ganador: {'Jugador 1' if ganador=='z1' else 'Jugador 2'}\n"
                f"Monto: {monto_juego} {currency}\n"
                f"Propina: {propina} {currency}"
            )
            
        except Exception as e:
            self.mostrar_mensaje_error("Error", f"Error al actualizar saldos: {str(e)}")

    def calcular_propina(self, monto_juego):
        """Calculate tip amount for regular credits"""
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
        else:  # >= 500
            return round(50.0 * (monto_juego // 500.0), 2)

    def calcular_propina_usdt(self, monto_juego):
        """Calculate tip amount for USDT"""
        if 1.0 <= monto_juego < 10.0:
            return 0.5
        else:  # >= 10.0
            return round((monto_juego // 10.0), 2)

    def resetear(self):
        """Reset all values and clear history"""
        if self.mostrar_mensaje_confirmacion("Confirmar", "¿Estás seguro de reiniciar todos los saldos y el historial?"):
            self.saldo_z0.set(0.0)
            self.saldo_z1.set(0.0)
            self.saldo_z2.set(0.0)
            self.juego_var.set(0.0)
            self.historial_partidas.clear()
            self.actualizar_notepad()
            self.mostrar_mensaje_exito("Reinicio", "Todos los saldos han sido reiniciados.")

    def mostrar_historial(self):
        """Display game history in a separate window with improved styling"""
        if not self.historial_partidas:
            self.mostrar_mensaje_info("Historial", "No hay partidas registradas aún.")
            return
            
        # Create history window with styling
        hist_window = tk.Toplevel(self.root)
        hist_window.title("Historial de Partidas")
        hist_window.geometry("600x540")
        hist_window.configure(bg=self.colors["background"])
        
        # Add padding
        hist_container = ttk.Frame(hist_window, padding="10 10 10 10")
        hist_container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(hist_container, text="HISTORIAL DE PARTIDAS", 
                             font=self.title_font, fg=self.colors["accent2"],
                             bg=self.colors["background"])
        title_label.pack(pady=(0, 10))
        
        # Create scrollable text widget with styling
        hist_frame = ttk.Frame(hist_container)
        hist_frame.pack(fill=tk.BOTH, expand=True)
        
        hist_text = tk.Text(hist_frame, wrap=tk.WORD, font=self.text_font,
                           bg="#2F3B5C", fg=self.colors["foreground"],
                           insertbackground=self.colors["foreground"],
                           relief=tk.FLAT)
        hist_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(hist_frame, command=hist_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        hist_text.config(yscrollcommand=scrollbar.set)
        
        # Add history content with styling
        hist_text.tag_configure("header", font=self.header_font, foreground=self.colors["accent2"])
        hist_text.tag_configure("subheader", font=self.header_font, foreground=self.colors["accent3"])
        hist_text.tag_configure("normal", font=self.text_font)
        hist_text.tag_configure("separator", font=self.text_font, foreground=self.colors["accent1"])
        
        hist_text.insert(tk.END, "HISTORIAL COMPLETO DE PARTIDAS\n", "header")
        hist_text.insert(tk.END, "="*50 + "\n\n", "separator")
        
        for i, partida in enumerate(self.historial_partidas, 1):
            hist_text.insert(tk.END, f"Partida #{i}:\n", "subheader")
            hist_text.insert(tk.END, f"{partida}\n\n", "normal")
            hist_text.insert(tk.END, "-"*40 + "\n\n", "separator")
        
        # Button frame
        button_frame = ttk.Frame(hist_container)
        button_frame.pack(pady=10)
        
        # Export button with styling
        export_button = tk.Button(
            button_frame, 
            text="EXPORTAR HISTORIAL", 
            command=lambda: self.exportar_historial(self.historial_partidas),
            font=self.text_font,
            bg=self.colors["accent3"], 
            fg=self.colors["foreground"],
            activebackground=self.darken_color(self.colors["accent3"]),
            activeforeground=self.colors["foreground"],
            relief=tk.FLAT, 
            borderwidth=0, 
            padx=15, 
            pady=8
        )
        export_button.pack()
        
        # Add hover effect
        export_button.bind("<Enter>", lambda e, b=export_button, c=self.colors["accent3"]: self.on_hover(b, c))
        export_button.bind("<Leave>", lambda e, b=export_button, c=self.colors["accent3"]: self.on_leave(b, c))

    def exportar_historial(self, historial):
        """Export history to a text file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Guardar historial como"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write("HISTORIAL DE PARTIDAS HABBO\n")
                    file.write("="*50 + "\n\n")
                    
                    for i, partida in enumerate(historial, 1):
                        file.write(f"Partida #{i}:\n{partida}\n\n")
                        file.write("-"*40 + "\n\n")
                        
                self.mostrar_mensaje_exito("Éxito", f"Historial exportado a {filename}")
            except Exception as e:
                self.mostrar_mensaje_error("Error", f"Error al exportar historial: {str(e)}")

    def importar_saldos(self):
        """Import balances from a text file"""
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
                    
                    # Try to extract saldos from the file if it follows the format
                    try:
                        lines = data.split('\n')
                        for line in lines:
                            if "Inter (Z0):" in line:
                                value = float(line.split(":")[1].strip())
                                self.saldo_z0.set(value)
                            elif "Jugador 1 (Z1):" in line:
                                value = float(line.split(":")[1].strip())
                                self.saldo_z1.set(value)
                            elif "Jugador 2 (Z2):" in line:
                                value = float(line.split(":")[1].strip())
                                self.saldo_z2.set(value)
                    except:
                        # If extraction fails, just keep the text in the notepad
                        pass
                        
                self.mostrar_mensaje_exito("Importación", "Archivo importado correctamente.")
            except Exception as e:
                self.mostrar_mensaje_error("Error", f"Error al importar archivo: {str(e)}")

    def exportar_saldos(self):
        """Export current balances to a text file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Guardar saldos como"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"SALDOS ACTUALES HABBO:\n\n")
                    file.write(f"Inter (Z0): {self.saldo_z0.get()}\n")
                    file.write(f"Jugador 1 (Z1): {self.saldo_z1.get()}\n")
                    file.write(f"Jugador 2 (Z2): {self.saldo_z2.get()}\n")
                    
                    if self.historial_partidas:
                        file.write(f"\n{'='*20}\n")
                        file.write(f"ÚLTIMAS PARTIDAS:\n")
                        
                        for partida in self.historial_partidas[-5:]:
                            file.write(f"\n{partida}\n")
                            
                self.mostrar_mensaje_exito("Éxito", f"Saldos exportados a {filename}")
            except Exception as e:
                self.mostrar_mensaje_error("Error", f"Error al exportar archivo: {str(e)}")
    
    def guardar_notas_personales(self):
        """Save personal notes to a text file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Guardar notas como"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(self.personal_notepad.get("1.0", tk.END))
                self.mostrar_mensaje_exito("Éxito", f"Notas guardadas en {filename}")
            except Exception as e:
                self.mostrar_mensaje_error("Error", f"Error al guardar notas: {str(e)}")
    
    def cargar_notas_personales(self):
        """Load personal notes from a text file"""
        filename = filedialog.askopenfilename(
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
            title="Abrir archivo de notas"
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    self.personal_notepad.delete("1.0", tk.END)
                    self.personal_notepad.insert(tk.END, file.read())
                self.mostrar_mensaje_exito("Carga Exitosa", f"Notas cargadas desde {filename}")
            except Exception as e:
                self.mostrar_mensaje_error("Error", f"Error al cargar notas: {str(e)}")
                
    # Custom styled message boxes
    def mostrar_mensaje_error(self, titulo, mensaje):
        """Display styled error message"""
        self.mostrar_mensaje_personalizado(titulo, mensaje, "#FF5F5D")
        
    def mostrar_mensaje_exito(self, titulo, mensaje):
        """Display styled success message"""
        self.mostrar_mensaje_personalizado(titulo, mensaje, "#06D6A0")
        
    def mostrar_mensaje_info(self, titulo, mensaje):
        """Display styled info message"""
        self.mostrar_mensaje_personalizado(titulo, mensaje, "#3BBFEF")
        
    def mostrar_mensaje_confirmacion(self, titulo, mensaje):
        """Display styled confirmation dialog"""
        # Create custom dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(titulo)
        dialog.geometry("400x220")
        dialog.configure(bg=self.colors["panel"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Add message
        message_label = tk.Label(dialog, text=mensaje, font=self.text_font,
                               bg=self.colors["panel"], fg=self.colors["foreground"],
                               wraplength=350, justify=tk.CENTER)
        message_label.pack(pady=(20, 30), padx=20)
        
        # Add buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        result = [False]  # Use list to store result
        
        # Yes button
        yes_button = tk.Button(
            button_frame, text="SÍ", font=self.text_font,
            bg=self.colors["accent4"], fg=self.colors["foreground"],
            activebackground=self.darken_color(self.colors["accent4"]),
            activeforeground=self.colors["foreground"],
            relief=tk.FLAT, borderwidth=0, padx=15, pady=8,
            command=lambda: [result.append(True), dialog.destroy()]
        )
        yes_button.grid(row=0, column=0, padx=5, sticky="e")
        
        # No button
        no_button = tk.Button(
            button_frame, text="NO", font=self.text_font,
            bg=self.colors["accent1"], fg=self.colors["foreground"],
            activebackground=self.darken_color(self.colors["accent1"]),
            activeforeground=self.colors["foreground"],
            relief=tk.FLAT, borderwidth=0, padx=15, pady=8,
            command=lambda: dialog.destroy()
        )
        no_button.grid(row=0, column=1, padx=5, sticky="w")
        
        # Add hover effects
        yes_button.bind("<Enter>", lambda e, b=yes_button, c=self.colors["accent4"]: self.on_hover(b, c))
        yes_button.bind("<Leave>", lambda e, b=yes_button, c=self.colors["accent4"]: self.on_leave(b, c))
        no_button.bind("<Enter>", lambda e, b=no_button, c=self.colors["accent1"]: self.on_hover(b, c))
        no_button.bind("<Leave>", lambda e, b=no_button, c=self.colors["accent1"]: self.on_leave(b, c))
        
        # Wait for the dialog to close
        dialog.wait_window()
        return True if len(result) > 1 else False
        
    def mostrar_mensaje_personalizado(self, titulo, mensaje, color_acento):
        """Display styled custom message dialog"""
        # Create custom dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(titulo)
        dialog.geometry("400x220")
        dialog.configure(bg=self.colors["panel"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create header
        header = tk.Frame(dialog, bg=color_acento, height=10)
        header.pack(fill=tk.X)
        
        # Add title
        title_label = tk.Label(dialog, text=titulo, font=self.header_font,
                             bg=self.colors["panel"], fg=color_acento)
        title_label.pack(pady=(20, 10))
        
        # Add message
        message_label = tk.Label(dialog, text=mensaje, font=self.text_font,
                               bg=self.colors["panel"], fg=self.colors["foreground"],
                               wraplength=350, justify=tk.CENTER)
        message_label.pack(pady=10, padx=20)
        
        # Add OK button
        ok_button = tk.Button(
            dialog, text="ACEPTAR", font=self.text_font,
            bg=color_acento, fg=self.colors["foreground"],
            activebackground=self.darken_color(color_acento),
            activeforeground=self.colors["foreground"],
            relief=tk.FLAT, borderwidth=0, padx=25, pady=8,
            command=dialog.destroy
        )
        ok_button.pack(pady=20)
        
        # Add hover effect
        ok_button.bind("<Enter>", lambda e, b=ok_button, c=color_acento: self.on_hover(b, c))
        ok_button.bind("<Leave>", lambda e, b=ok_button, c=color_acento: self.on_leave(b, c))

if __name__ == "__main__":
    root = tk.Tk()
    app = CuentaApp(root)
    root.mainloop()
