import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk
from datetime import datetime
from app.ui.formulario_registro import abrir_formulario_registro
from app.ui.buscar_editar import abrir_buscar_editar
from app.ui.exportar_excel import exportar_a_excel



def iniciar_app():
    root = tk.Tk()
    root.title("Control de Horas - V1")
    root.geometry("520x520")
    root.resizable(False, False)

    # ================================
    # COLORES CORPORATIVOS
    # ================================
    COLOR_VERDE = "#1f7a4d"
    COLOR_BOTON = "#1f7a4d"
    COLOR_BOTON_HOVER = "#249d63"
    COLOR_SALIR = "#8b2c1f"
    COLOR_SALIR_HOVER = "#b03a2e"
    COLOR_FONDO = "#f2f2f2"

    root.configure(bg=COLOR_FONDO)

    # ================================
    # HEADER SUPERIOR
    # ================================
    header = tk.Frame(root, bg=COLOR_VERDE, height=50)
    header.pack(fill="x")

    lbl_titulo = tk.Label(
        header,
        text="CONTROL DE HORAS",
        bg=COLOR_VERDE,
        fg="white",
        font=("Segoe UI", 12, "bold")
    )
    lbl_titulo.pack(side="left", padx=20)

    lbl_hora = tk.Label(
        header,
        bg=COLOR_VERDE,
        fg="white",
        font=("Segoe UI", 10)
    )
    lbl_hora.pack(side="right", padx=20)

    def actualizar_hora():
        lbl_hora.config(text=datetime.now().strftime("%I:%M:%S %p"))
        root.after(1000, actualizar_hora)

    actualizar_hora()

    # ================================
    # SECCIÓN LOGO + EMPRESA
    # ================================
    empresa_frame = tk.Frame(root, bg=COLOR_FONDO)
    empresa_frame.pack(pady=25)

    base_dir = Path(__file__).resolve().parents[2]
    logo_path = base_dir / "assets" / "logo.png"

    logo_img = Image.open(logo_path)
    logo_img = logo_img.resize((60, 60))
    logo_tk = ImageTk.PhotoImage(logo_img)

    lbl_logo = tk.Label(empresa_frame, image=logo_tk, bg=COLOR_FONDO)
    lbl_logo.image = logo_tk  # mantener referencia
    lbl_logo.pack(side="left", padx=10)

    lbl_empresa = tk.Label(
        empresa_frame,
        text="ELITE Ingenieros S.A.S.",
        bg=COLOR_FONDO,
        fg="#0d3b2e",
        font=("Segoe UI", 14, "bold")
    )
    lbl_empresa.pack(side="left")

    # ================================
    # BOTONES PRINCIPALES
    # ================================
    def info(msg):
        messagebox.showinfo("Información", msg)

    botones_frame = tk.Frame(root, bg=COLOR_FONDO)
    botones_frame.pack(pady=10)

    def crear_boton(texto, comando, color_base, color_hover):
        btn = tk.Button(
            botones_frame,
            text=texto,
            width=30,
            height=2,
            bg=color_base,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="raised",
            bd=2,
            cursor="hand2",
            activebackground=color_hover,
            activeforeground="white",
            command=comando
        )

        # Hover (entra)
        def on_enter(e):
            btn.config(
                bg=color_hover,
                relief="raised",
                bd=3
            )

        # Hover (sale)
        def on_leave(e):
            btn.config(
                bg=color_base,
                relief="raised",
                bd=2
            )

        # Click presionado
        def on_press(e):
            btn.config(relief="sunken", bd=2)

        # Click soltado
        def on_release(e):
            btn.config(relief="raised", bd=3)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<ButtonPress-1>", on_press)
        btn.bind("<ButtonRelease-1>", on_release)

        return btn

    crear_boton(
        "Nuevo registro",
        lambda: abrir_formulario_registro(root),
        COLOR_BOTON,
        COLOR_BOTON_HOVER
    ).pack(pady=6)


    crear_boton(
        "Buscar / Editar registros",
        lambda: abrir_buscar_editar(root),
        COLOR_BOTON,
        "#249d63"
    ).pack(pady=6)

    crear_boton(
        "Exportar a Excel",
         lambda: exportar_a_excel(root),
        COLOR_BOTON,
        "#249d63"
    ).pack(pady=6)

    crear_boton(
        "Ver Dashboard",
        lambda: info("Dashboard (Paso 13)"),
        COLOR_BOTON,
        "#249d63"
    ).pack(pady=6)

    crear_boton(
        "Salir",
        root.quit,
        COLOR_SALIR,
        "#b03a2e"
    ).pack(pady=20)

    # ================================
    # FOOTER
    # ================================
    footer = tk.Frame(root, bg="#dddddd", height=30)
    footer.pack(fill="x", side="bottom")

    lbl_footer = tk.Label(
        footer,
        text="© 2026 Elite Ingenieros S.A.S.  |  Esperando acción del usuario...",
        bg="#dddddd",
        fg="#333333",
        font=("Segoe UI", 9)
    )
    lbl_footer.pack(pady=5)

    root.mainloop()
