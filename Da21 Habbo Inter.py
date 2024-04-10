import tkinter as tk
from tkinter import messagebox, filedialog

class CuentaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación para Intear (HABBO)")

        self.saldo_z0 = tk.DoubleVar()
        self.saldo_z1 = tk.DoubleVar()
        self.saldo_z2 = tk.DoubleVar()
        self.juego_var = tk.DoubleVar()
        self.dinero_real_var = tk.BooleanVar()
        self.usdt_var = tk.BooleanVar()  # Variable para controlar si se usa USDT
        self.historial_partidas = []  # Historial de partidas
        self.saldos_iniciales = {}  # Saldo inicial de cada jugador

        self.create_widgets()
        self.create_notepad()

    def create_widgets(self):
        tk.Label(self.root, text="Saldo Inter (Z0):").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.root, text="Saldo Jugador 1 (Z1):").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.root, text="Saldo Jugador 2 (Z2):").grid(row=2, column=0, padx=10, pady=5)

        self.saldo_z0.set(0.0)
        self.saldo_z1.set(0.0)
        self.saldo_z2.set(0.0)

        self.saldo_z0_entry = tk.Entry(self.root, textvariable=self.saldo_z0)
        self.saldo_z0_entry.grid(row=0, column=1, padx=10, pady=5)
        self.saldo_z1_entry = tk.Entry(self.root, textvariable=self.saldo_z1)
        self.saldo_z1_entry.grid(row=1, column=1, padx=10, pady=5)
        self.saldo_z2_entry = tk.Entry(self.root, textvariable=self.saldo_z2)
        self.saldo_z2_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Monto del juego:").grid(row=3, column=0, padx=10, pady=5)
        self.juego_entry = tk.Entry(self.root, textvariable=self.juego_var)
        self.juego_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Dinero Real:").grid(row=6, column=0, padx=10, pady=5)
        self.dinero_real_checkbox = tk.Checkbutton(self.root, variable=self.dinero_real_var, text="Activado", command=self.check_checkbox)
        self.dinero_real_checkbox.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(self.root, text="USDT:").grid(row=7, column=0, padx=10, pady=5)
        self.usdt_checkbox = tk.Checkbutton(self.root, variable=self.usdt_var, text="Activado", command=self.check_checkbox)
        self.usdt_checkbox.grid(row=7, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Z1 gana", command=lambda: self.actualizar_saldos("z1")).grid(row=4, column=0, padx=10, pady=5)
        tk.Button(self.root, text="Z2 gana", command=lambda: self.actualizar_saldos("z2")).grid(row=4, column=1, padx=10, pady=5)
        
        tk.Button(self.root, text="Historial", command=self.mostrar_historial).grid(row=5, columnspan=2, padx=10, pady=5)

        tk.Button(self.root, text="Reset", command=self.resetear).grid(row=8, columnspan=2, padx=10, pady=5)

        buttons_frame = tk.Frame(self.root)
        buttons_frame.grid(row=9, column=2, padx=10, pady=5)
        
        tk.Button(buttons_frame, text="Importar saldos", command=self.importar_saldos).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Exportar saldos", command=self.exportar_saldos).pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.root, text="Developed By _Acos_ / Wembie").grid(row=9, column=0, columnspan=2)

    def create_notepad(self):
        self.notepad_frame = tk.Frame(self.root)
        self.notepad_frame.grid(row=0, column=2, rowspan=8, padx=10, pady=5, sticky="nsew")

        self.notepad = tk.Text(self.notepad_frame, height=10, width=30)
        self.notepad.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        scrollbar = tk.Scrollbar(self.notepad_frame, command=self.notepad.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.notepad.config(yscrollcommand=scrollbar.set)

        # Título del bloc de notas
        tk.Label(self.notepad_frame, text="SALDOS", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="n")

    def check_checkbox(self):
        # Verifica qué opción está seleccionada y desactiva la otra opción
        if self.dinero_real_var.get():
            self.usdt_var.set(False)
        elif self.usdt_var.get():
            self.dinero_real_var.set(False)

    def actualizar_saldos(self, ganador):
        monto_juego = self.juego_var.get()
        if self.usdt_var.get():  # Si se usa USDT
            if monto_juego < 1.0:
                messagebox.showerror("Error", "El monto del juego debe ser al menos 1 USDT.")
                return
            propina = self.calcular_propina_usdt(monto_juego)
        else:
            if monto_juego < 5.0:
                messagebox.showerror("Error", "El monto del juego debe ser al menos 5 créditos.")
                return
            if self.dinero_real_var.get():
                propina = round(monto_juego * 0.1, 2)
            else:
                propina = self.calcular_propina(monto_juego)

        saldo_z0_inicial = self.saldo_z0.get()
        saldo_z1_inicial = self.saldo_z1.get()
        saldo_z2_inicial = self.saldo_z2.get()

        if ganador == "z1":
            self.saldo_z0.set(round(self.saldo_z0.get() + propina, 2))
            self.saldo_z1.set(round(self.saldo_z1.get() + monto_juego - propina, 2))
        elif ganador == "z2":
            self.saldo_z0.set(round(self.saldo_z0.get() + propina, 2))
            self.saldo_z2.set(round(self.saldo_z2.get() + monto_juego - propina, 2))

        # Restar el monto apostado al jugador que pierde
        if ganador == "z1":
            self.saldo_z2.set(round(self.saldo_z2.get() - monto_juego, 2))
        elif ganador == "z2":
            self.saldo_z1.set(round(self.saldo_z1.get() - monto_juego, 2))

        # Agregar la partida al historial
        self.historial_partidas.append(f"Juego: {ganador}, Monto: {monto_juego}, Propina: {propina}, "
                                       f"Saldo Inicial Z0: {saldo_z0_inicial}, Saldo Inicial Z1: {saldo_z1_inicial}, "
                                       f"Saldo Inicial Z2: {saldo_z2_inicial}")

    def calcular_propina(self, monto_juego):
        if 5.0 <= monto_juego <= 9.0:
            return 2.0
        elif 10.0 <= monto_juego <= 14.0:
            return 3.0
        elif 15.0 <= monto_juego <= 19.0:
            return 4.0
        elif 20.0 <= monto_juego <= 25.0:
            return 5.0
        elif 26.0 <= monto_juego <= 30.0:
            return 6.0
        elif 31.0 <= monto_juego <= 35.0:
            return 7.0
        elif 36.0 <= monto_juego <= 40.0:
            return 8.0
        elif 41.0 <= monto_juego <= 49.0:
            return 9.0
        elif 50.0 <= monto_juego <= 99.0:
            return 10.0
        elif 100.0 <= monto_juego <= 149.0:
            return 20.0
        elif 150.0 <= monto_juego <= 499.0:
            return 30.0
        else:
            return round(50.0 * (monto_juego // 500.0), 2)

    def calcular_propina_usdt(self, monto_juego):
        if 1.0 <= monto_juego <= 9.99:
            return 0.5
        else:
            return round((monto_juego // 10.0), 2)

    def resetear(self):
        self.saldo_z0.set(0.0)
        self.saldo_z1.set(0.0)
        self.saldo_z2.set(0.0)
        self.juego_var.set(0.0)
        self.historial_partidas.clear()  # Limpiar historial al resetear

    def mostrar_historial(self):
        messagebox.showinfo("Historial de Partidas", "\n".join(self.historial_partidas))

    def importar_saldos(self):
        filename = filedialog.askopenfilename(filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")))
        if filename:
            with open(filename, 'r') as file:
                data = file.read()
                self.notepad.delete("1.0", tk.END)
                self.notepad.insert(tk.END, data)

    def exportar_saldos(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")))
        if filename:
            data = self.notepad.get("1.0", tk.END)
            with open(filename, 'w') as file:
                file.write(data)

if __name__ == "__main__":
    root = tk.Tk()
    app = CuentaApp(root)
    root.mainloop()
