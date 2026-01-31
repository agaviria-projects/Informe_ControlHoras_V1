import os
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
    root.withdraw()  # ✅ ocultar mientras se configura (evita “salto”)

    root.title("Control de Horas - V1")
    root.geometry("520x610")  # ✅ ALTURA igual al formulario
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
    COLOR_ICON_BG = "#eaeaea"  # fondo suave del icono (puedes dejarlo como el fondo también)

    root.configure(bg=COLOR_FONDO)

    # ================================
    # RUTAS
    # ================================
    base_dir = Path(__file__).resolve().parents[2]
    logo_path = base_dir / "assets" / "logo.png"
    folder_icon_path = base_dir / "assets" / "folder_open.png"  # ✅ aquí va tu icono real
    reports_dir = base_dir / "reports"
    excel_out = reports_dir / "reporte_control_horas.xlsx"

    # ================================
    # ICONO APP (NO revienta si falta)
    # ================================
    try:
        icon_img = Image.open(logo_path).resize((64, 64))
        icon_tk = ImageTk.PhotoImage(icon_img)
        root.iconphoto(True, icon_tk)
        root._icon_ref = icon_tk
    except Exception:
        pass

    # ================================
    # CENTRAR VENTANA PRINCIPAL
    # ================================
    root.update_idletasks()
    ancho = 520
    alto = 610
    x = (root.winfo_screenwidth() // 2) - (ancho // 2)
    y = (root.winfo_screenheight() // 2) - (alto // 2)
    root.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ================================
    # TOPMOST 1 SEGUNDO
    # ================================
    def _topmost_temporal():
        try:
            root.attributes("-topmost", True)
            root.update()
            root.after(1000, lambda: root.attributes("-topmost", False))
        except Exception:
            pass

    root.deiconify()
    root.lift()
    root.focus_force()
    _topmost_temporal()

    # ================================
    # HEADER
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
    lbl_titulo.place(relx=0.5, rely=0.5, anchor="center")

    lbl_hora = tk.Label(
        header,
        bg=COLOR_VERDE,
        fg="white",
        font=("Segoe UI", 10, "bold")
    )
    lbl_hora.place(relx=1.0, rely=0.5, anchor="e", x=-20)

    def actualizar_hora():
        lbl_hora.config(text=datetime.now().strftime("%I:%M:%S %p"))
        root.after(1000, actualizar_hora)

    actualizar_hora()

    # ================================
    # LOGO + EMPRESA
    # ================================
    empresa_frame = tk.Frame(root, bg=COLOR_FONDO)
    empresa_frame.pack(pady=25)

    try:
        logo_img = Image.open(logo_path).resize((60, 60))
        logo_tk = ImageTk.PhotoImage(logo_img)
        lbl_logo = tk.Label(empresa_frame, image=logo_tk, bg=COLOR_FONDO)
        lbl_logo.image = logo_tk
        lbl_logo.pack(side="left", padx=10)
    except Exception:
        pass

    lbl_empresa = tk.Label(
        empresa_frame,
        text="ELITE Ingenieros S.A.S.",
        bg=COLOR_FONDO,
        fg="#000403",
        font=("Segoe UI", 14, "bold")
    )
    lbl_empresa.pack(side="left")

    # ================================
    # UTILIDADES
    # ================================
    def info(msg):
        messagebox.showinfo("Información", msg)

    def abrir_excel_o_carpeta():
        try:
            reports_dir.mkdir(exist_ok=True)
            if excel_out.exists():
                os.startfile(str(excel_out))      # ✅ abre el Excel directo
            else:
                os.startfile(str(reports_dir))    # ✅ abre la carpeta si no existe aún
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo abrir:\n{ex}", parent=root)

    # Cargar icono real (si existe)
    folder_icon_tk = None
    try:
        img = Image.open(folder_icon_path).convert("RGBA").resize((20, 20))
        folder_icon_tk = ImageTk.PhotoImage(img)
        root._folder_icon_ref = folder_icon_tk  # ✅ evitar garbage collector
    except Exception:
        folder_icon_tk = None

    # ================================
    # BOTONES (MISMA GRILLA = TODO ALINEADO)
    # ================================
    botones_frame = tk.Frame(root, bg=COLOR_FONDO)
    botones_frame.pack(pady=10)

    # Grilla interna para mantener alineación perfecta
    menu = tk.Frame(botones_frame, bg=COLOR_FONDO)
    menu.pack()

    # Col 0 = botón grande / Col 1 = icono (o placeholder)
    menu.grid_columnconfigure(0, weight=0)
    menu.grid_columnconfigure(1, weight=0)

    def crear_boton_grande(parent, texto, comando, color_base, color_hover):
        btn = tk.Button(
            parent,
            text=texto,
            width=30,
            height=2,
            bg=color_base,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="raised",
            bd=2,
            cursor="hand2",
            activebackground=color_hover,
            activeforeground="white",
            command=comando
        )

        def on_enter(e):
            btn.config(bg=color_hover, bd=3)

        def on_leave(e):
            btn.config(bg=color_base, bd=2)

        def on_press(e):
            btn.config(relief="sunken", bd=2)

        def on_release(e):
            btn.config(relief="raised", bd=3)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<ButtonPress-1>", on_press)
        btn.bind("<ButtonRelease-1>", on_release)

        return btn

    def placeholder_icon(parent):
        # espacio “vacío” para que las filas sin icono queden alineadas
        ph = tk.Label(parent, text="", bg=COLOR_FONDO, width=3)
        return ph

    # --- Fila 0
    b0 = crear_boton_grande(menu, "Nuevo registro", lambda: abrir_formulario_registro(root), COLOR_BOTON, COLOR_BOTON_HOVER)
    b0.grid(row=0, column=0, pady=6, padx=(0, 10), sticky="w")
    placeholder_icon(menu).grid(row=0, column=1, pady=6, sticky="w")

    # --- Fila 1
    b1 = crear_boton_grande(menu, "Buscar / Editar registros", lambda: abrir_buscar_editar(root), COLOR_BOTON, COLOR_BOTON_HOVER)
    b1.grid(row=1, column=0, pady=6, padx=(0, 10), sticky="w")
    placeholder_icon(menu).grid(row=1, column=1, pady=6, sticky="w")

    # --- Fila 2 (Export + icono real)
    b2 = crear_boton_grande(menu, "Exportar a Excel", lambda: exportar_a_excel(root), COLOR_BOTON, COLOR_BOTON_HOVER)
    b2.grid(row=2, column=0, pady=6, padx=(0, 10), sticky="w")

    if folder_icon_tk is not None:
        btn_icon = tk.Button(
            menu,
            image=folder_icon_tk,
            bg=COLOR_FONDO,           # ✅ se integra con el fondo (más pro)
            activebackground=COLOR_FONDO,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=abrir_excel_o_carpeta
        )
    else:
        # Fallback si no hay PNG: un botón discreto con texto
        btn_icon = tk.Button(
            menu,
            text="Abrir",
            width=5,
            bg=COLOR_ICON_BG,
            fg="#000000",
            font=("Segoe UI", 9, "bold"),
            relief="raised",
            bd=1,
            cursor="hand2",
            command=abrir_excel_o_carpeta
        )

    btn_icon.grid(row=2, column=1, pady=6, sticky="w")

    # --- Fila 3
    b3 = crear_boton_grande(menu, "Ver Dashboard", lambda: info("Dashboard (Paso 13)"), COLOR_BOTON, COLOR_BOTON_HOVER)
    b3.grid(row=3, column=0, pady=6, padx=(0, 10), sticky="w")
    placeholder_icon(menu).grid(row=3, column=1, pady=6, sticky="w")

    # --- Fila 4 (Salir)
    b4 = crear_boton_grande(menu, "Salir", root.quit, COLOR_SALIR, COLOR_SALIR_HOVER)
    b4.grid(row=4, column=0, pady=(20, 0), padx=(0, 10), sticky="w")
    placeholder_icon(menu).grid(row=4, column=1, pady=(20, 0), sticky="w")

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
