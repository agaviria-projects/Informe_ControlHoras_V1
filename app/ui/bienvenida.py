import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk


def abrir_bienvenida(abrir_principal_callback):
    ventana = tk.Tk()
    ventana.withdraw()
    ventana.title("Bienvenido - Control de Horas")
    ventana.geometry("520x420")
    ventana.resizable(False, False)

    COLOR_VERDE = "#1f7a4d"
    COLOR_FONDO = "#f2f2f2"

    ventana.configure(bg=COLOR_FONDO)

    # ==============================
    # CENTRAR VENTANA
    # ==============================
    ventana.update_idletasks()
    w, h = 520, 420
    x = (ventana.winfo_screenwidth() // 2) - (w // 2)
    y = (ventana.winfo_screenheight() // 2) - (h // 2)
    ventana.geometry(f"{w}x{h}+{x}+{y}")

    # ==============================
    # LOGO
    # ==============================
    base_dir = Path(__file__).resolve().parents[2]
    logo_path = base_dir / "assets" / "logo.png"

    # ==============================
    # ICONO APP (barra de título)
    # ==============================
    try:
        icon_img = Image.open(logo_path).resize((64, 64))
        icon_tk = ImageTk.PhotoImage(icon_img)
        ventana.iconphoto(True, icon_tk)
        ventana._icon_ref = icon_tk  # evitar garbage collector
    except Exception:
        pass

    try:
        img = Image.open(logo_path).resize((120, 120))
        logo = ImageTk.PhotoImage(img)
    except Exception:
        logo = None

    if logo:
        lbl_logo = tk.Label(ventana, image=logo, bg=COLOR_FONDO)
        lbl_logo.image = logo
        lbl_logo.pack(pady=20)

    # ==============================
    # TEXTOS
    # ==============================
    tk.Label(
        ventana,
        text="ELITE Ingenieros S.A.S.",
        bg=COLOR_FONDO,
        fg="#000000",
        font=("Segoe UI", 14, "bold")
    ).pack(pady=(0, 5))

    tk.Label(
        ventana,
        text="Sistema de Control de Horas",
        bg=COLOR_FONDO,
        fg="#444444",
        font=("Segoe UI", 11)
    ).pack(pady=(0, 25))

    # ==============================
    # BOTÓN INGRESAR
    # ==============================
    def continuar():
        ventana.withdraw()  # oculta ya mismo (sin parpadeo)
        ventana.after(0, lambda: (ventana.destroy(), abrir_principal_callback()))

    btn = tk.Button(
        ventana,
        text="Ingresar",
        width=18,
        height=2,
        bg=COLOR_VERDE,
        fg="white",
        font=("Segoe UI", 11, "bold"),
        cursor="hand2",
        command=continuar
    )
    btn.pack()

    ventana.update_idletasks()
    ventana.deiconify()
    ventana.lift()
    ventana.focus_force()

    ventana.mainloop()
