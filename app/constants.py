AUTOSAVE_FILE = "da21_autosave.json"

NOTES_PLACEHOLDER = (
    "Escribe tus notas personales aquí...\n\n"
    "Puedes guardar y cargar tus notas con los botones de abajo."
)

COLORS: dict[str, str] = {
    # Base surfaces
    "background": "#111120",    # Deep dark navy
    "foreground": "#E2E8F8",    # Clean white text
    "panel":      "#191930",    # Panel bg — slightly blue-dark
    "card":       "#22223E",    # Inner card — clearly distinct from panel
    "input":      "#0E0E22",    # Input fields — deepest
    "border":     "#2E2E58",    # Borders — visible but subtle
    "highlight":  "#252545",    # Hover/selection
    "muted":      "#7878A0",    # Muted text
    # Accent colors
    "accent1":    "#F43F5E",    # Rose/red — danger, reset
    "accent2":    "#3B82F6",    # Blue — info, historial, cargar notas
    "accent3":    "#F97316",    # Orange — IO, game amount
    "accent4":    "#16A34A",    # Green — success, guardar notas
    "danger":     "#F43F5E",    # Negative balance indicator
    # Player-specific colors
    "inter":      "#A855F7",    # Purple — Inter
    "z1":         "#0891B2",    # Dark cyan — Z1 (legible con blanco)
    "z2":         "#E11D48",    # Deep rose — Z2
}

CURRENCIES: list[str] = [
    "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN",
    "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL",
    "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF", "CLP", "CNY",
    "COP", "CRC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP",
    "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD",
    "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR",
    "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF",
    "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD",
    "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR",
    "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD",
    "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON",
    "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP",
    "SOS", "SRD", "SSP", "STN", "SYP", "SZL", "THB", "TJS", "TMT", "TND",
    "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU", "UZS",
    "VES", "VND", "VUV", "WST", "XAF", "XCD", "XOF", "XPF", "YER", "ZAR",
    "ZMW", "ZWL",
]
