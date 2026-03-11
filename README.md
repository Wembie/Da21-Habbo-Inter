# Da21 Habbo Inter

Aplicación de escritorio desarrollada en Python con Tkinter para llevar el registro de saldos y partidas entre un intermediario (Inter) y dos jugadores (Z1, Z2) en juegos estilo Habbo.

## Funcionalidades

- **Nombres personalizables** para el Inter, Z1 y Z2 (con etiquetas de rol visibles)
- **Saldos en tiempo real** — actualizados automáticamente al registrar cada partida
- **Saldo negativo** destacado en rojo automáticamente en cards y panel de resumen
- **Tres modos de pago:**
  - Sin marcar → **Créditos Habbo** (tabla de propinas fija)
  - **Dinero Real** → selector de moneda ISO 4217 (~160 divisas, por defecto COP)
  - **USDT** → propina calculada en dólares
- **Botones de victoria dinámicos** — muestran el nombre real del jugador (no "Z1/Z2")
- **Historial completo** con timestamp, ganador, método de pago, monto, propina y saldos con moneda
- **Autosave automático** en JSON — se restaura el estado completo al reabrir
- **Exportación e importación** de saldos e historial en `.txt`
- **Bloc de notas personal** con guardado y carga desde archivo
- **Interfaz oscura moderna** con tema navy-dark, cards por jugador con avatar circular y triple stripe de colores en el header

## Capturas por versión

Las capturas se guardan en la carpeta [`screenshots/`](screenshots/) del repositorio.

### Version 1

![Version 1](screenshots/Version%201.png)

---

### Version 2

![Version 2](screenshots/Version%202.png)

---

### Version 3 (Actual)

![Version 3](screenshots/Version%203.png)

---

<!-- Para agregar una nueva versión, copiá el bloque de abajo y pegalo aquí:

### Version X

![Version X](screenshots/Version%20X.png)

-->


## Estructura del proyecto

```
Da21-Habbo-Inter/
├── main.py
├── pyproject.toml
├── .gitignore
├── screenshots/               # Capturas por versión
└── app/
    ├── constants.py           # Colores (paleta navy-dark), monedas ISO 4217, strings
    ├── models/
    │   ├── game_state.py      # Dataclass GameState
    │   └── tip_calculator.py  # Cálculo de propinas (créditos y USDT)
    ├── services/
    │   └── persistence.py     # Autosave — carga/guarda JSON
    └── ui/
        ├── theme.py           # Fuentes Segoe UI / Consolas y estilos ttk
        ├── widgets.py         # RoundedButton, player_card, section_title, etc.
        ├── dialogs.py         # Diálogos personalizados y ventana de historial
        ├── app.py             # Orquestador principal (ventana, header, layout)
        └── panels/
            ├── controls_panel.py  # Panel izquierdo — jugadores, juego, pagos, acciones
            └── notepad_panel.py   # Panel derecho — resumen de saldos y notas personales
```

## Instalación

### Con UV (recomendado)

```bash
# Instalar UV si no lo tenés
pip install uv

# Clonar el repositorio
git clone https://github.com/tu-usuario/Da21-Habbo-Inter.git
cd Da21-Habbo-Inter

# Crear entorno e instalar dependencias
uv sync
```

### Con Python estándar

```bash
git clone https://github.com/tu-usuario/Da21-Habbo-Inter.git
cd Da21-Habbo-Inter
python main.py
```

> Requiere **Python 3.10+**. Sin dependencias externas (solo stdlib + tkinter).

## Uso

```bash
python main.py
```

1. Editá los **nombres** del Inter, Z1 y Z2 directamente en sus cards
2. Ingresá los **saldos iniciales** de cada jugador en el campo "Saldo"
3. Elegí el **tipo de pago**:
   - Sin marcar → Créditos Habbo
   - **Dinero Real** → seleccioná la moneda (COP por defecto)
   - **USDT** → propina automática en dólares
4. Ingresá el **monto del juego** en el campo central
5. Presioná el botón del ganador — los saldos se actualizan al instante
6. Usá **HISTORIAL** para ver todas las partidas y exportarlas a `.txt`
7. Usá **EXPORTAR SALDOS** para guardar el estado actual

### Formato del historial

```
[DD/MM/AAAA HH:MM] Ganador: Nombre (Z1)
Método: Créditos Habbo
Monto: 50.0 C
Propina: 5.0 C
Saldos [C]: Inter(Inter)=10.0, Jugador1(Z1)=40.0, Jugador2(Z2)=-50.0
```

## Video Explicativo

[Ver en YouTube](https://www.youtube.com/watch?v=hJH18hSmNsw&t=23s&ab_channel=Wembie)

## Contribución

Las contribuciones son bienvenidas. Si encontrás algún error o tenés alguna sugerencia, abrí un issue o enviá un pull request.

## Donaciones

Cualquier donación es voluntaria y muy apreciada. ¡Podés contactarme en Telegram como **@Soy_Acos**!

## Créditos

Desarrollado por **_Acos_ / Wembie**.
