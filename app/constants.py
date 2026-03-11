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
    "accent1":    "#FF6B8A",    # Pink/red — danger, reset (more vivid)
    "accent2":    "#7EC8E3",    # Steel blue — info, historial
    "accent3":    "#FFAA65",    # Orange-peach — IO, game amount
    "accent4":    "#7FD99A",    # Mint green — success
    "danger":     "#FF6B8A",    # Negative balance indicator
    # Player-specific colors
    "inter":      "#C084FC",    # Purple — Inter  (more vivid)
    "z1":         "#67E8F9",    # Cyan — Z1 (more vivid)
    "z2":         "#FB7185",    # Rose/red — Z2 (more vivid)
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
