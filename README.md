# Da21 Habbo Inter

¡Bienvenido a Da21 Habbo Inter!

Aplicación de escritorio desarrollada en Python con Tkinter para llevar el registro de saldos y partidas entre un intermediario (Inter) y dos jugadores (Z1, Z2) en juegos estilo Habbo.

## Funcionalidades

- Nombres personalizables para el Inter y cada jugador
- Registro de saldos en tiempo real con actualización automática según el resultado
- Tres modos de pago: **Créditos Habbo**, **Dinero Real** (con selector de moneda) y **USDT**
- Selector de moneda con todas las divisas ISO 4217 (~160 monedas)
- Cálculo automático de propina según el monto jugado
- Historial completo de partidas con timestamp y método de pago
- Autosave automático al cerrar/resetear (se restaura al reabrir)
- Exportación e importación de saldos e historial en `.txt`
- Bloc de notas personal con guardado y carga desde archivo
- Interfaz oscura moderna con efectos hover en botones

## Estructura del proyecto

```
Da21-Habbo-Inter/
├── main.py
├── pyproject.toml
├── .gitignore
└── app/
    ├── constants.py           # Colores, monedas, strings globales
    ├── models/
    │   ├── game_state.py      # Dataclass GameState
    │   └── tip_calculator.py  # Cálculo de propinas
    ├── services/
    │   └── persistence.py     # Autosave (carga/guarda JSON)
    └── ui/
        ├── theme.py           # Fuentes y estilos ttk
        ├── widgets.py         # Factory functions de widgets
        ├── dialogs.py         # Diálogos y ventana de historial
        ├── app.py             # Orquestador principal
        └── panels/
            ├── controls_panel.py  # Panel izquierdo (saldos, juego, acciones)
            └── notepad_panel.py   # Panel derecho (notepad + notas personales)
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

> Requiere Python 3.10 o superior. No tiene dependencias externas (solo stdlib).

## Uso

```bash
python main.py
```

1. Editá los nombres del Inter, Jugador 1 y Jugador 2 directamente en los campos de la interfaz
2. Ingresá los saldos iniciales de cada uno
3. Seleccioná el tipo de pago:
   - Sin marcar → **Créditos Habbo** (tabla de propinas fija)
   - **Dinero Real** → elegí la moneda en el selector (COP por defecto)
   - **USDT** → propina calculada en dólares
4. Ingresá el monto del juego y presioná **Z1 GANA** o **Z2 GANA**
5. Usá **HISTORIAL** para ver y exportar todas las partidas
6. Usá **EXPORTAR SALDOS** para guardar el estado actual en un `.txt`

## Foto

![Habbo Da21](https://i.imgur.com/pYbbNuz.png)

## Video Explicativo

[Ver en YouTube](https://www.youtube.com/watch?v=hJH18hSmNsw&t=23s&ab_channel=Wembie)

## Contribución

Las contribuciones son bienvenidas. Si encontrás algún error o tenés alguna sugerencia, abrí un issue o enviá un pull request.

## Donaciones

Cualquier donación es voluntaria y muy apreciada. ¡Podés contactarme en Telegram como **@Soy_Acos**!

## Créditos

Desarrollado por **_Acos_ / Wembie**.
