"""Custom styled dialog windows."""
import tkinter as tk
from tkinter import ttk

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
