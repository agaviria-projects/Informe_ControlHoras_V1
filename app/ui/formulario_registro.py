import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

from app.data.repository import crear_registro
from app.ui.widgets.calendario_selector import seleccionar_fecha, FESTIVOS


def abrir_formulario_registro(parent):
    parent.withdraw()

    ventana = tk.Toplevel(parent)
    ventana.withdraw()
    ventana.title("Nuevo Registro - Control de Horas")
    ventana.geometry("520x610")
    ventana.resizable(False, False)
    ventana.grab_set()

    ventana.update_idletasks()
    ancho = 520
    alto = 610
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana.deiconify()

    # ================================
    # COLORES
    # ================================
    COLOR_VERDE = "#1f7a4d"
    COLOR_FONDO = "#f2f2f2"
    COLOR_BORDE = "#d9d9d9"

    BTN_GUARDAR_BG = "#1f7a4d"
    BTN_GUARDAR_HOVER = "#16633e"
    BTN_SALIR_BG = "#6f6f6f"
    BTN_SALIR_HOVER = "#5b5b5b"

    ventana.configure(bg=COLOR_FONDO)

    # ================================
    # FUENTES
    # ================================
    FONT_HEADER = ("Segoe UI", 12, "bold")
    FONT_LABEL  = ("Segoe UI", 11, "bold")
    FONT_INPUT  = ("Segoe UI", 11)
    FONT_BTN    = ("Segoe UI", 11, "bold")

    # ================================
    # ttk style (combobox)
    # ================================
    style = ttk.Style()
    try:
        style.theme_use("vista")
    except Exception:
        try:
            style.theme_use("clam")
        except Exception:
            pass

    style.configure(
        "Modern.TCombobox",
        font=FONT_INPUT,
        padding=(6, 6, 6, 6)
    )

    # ================================
    # HEADER
    # ================================
    header = tk.Frame(ventana, bg=COLOR_VERDE, height=52)
    header.pack(fill="x")

    tk.Label(
        header,
        text="NUEVO REGISTRO",
        bg=COLOR_VERDE,
        fg="white",
        font=FONT_HEADER
    ).pack(pady=14)

    # ================================
    # CARD
    # ================================
    card = tk.Frame(
        ventana,
        bg=COLOR_FONDO,
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    )
    card.pack(padx=22, pady=18, fill="x")

    form_frame = tk.Frame(card, bg=COLOR_FONDO)
    form_frame.pack(padx=18, pady=18, fill="x")

    form_frame.grid_columnconfigure(0, weight=0)
    form_frame.grid_columnconfigure(1, weight=1)
    form_frame.grid_columnconfigure(2, weight=0)

    entries = []

    # ================================
    # MAYÚSCULAS
    # ================================
    var_nombre = tk.StringVar()
    var_placa = tk.StringVar()
    var_zona = tk.StringVar()

    def _forzar_mayusculas(var: tk.StringVar):
        v = var.get()
        up = v.upper()
        if v != up:
            var.set(up)

    var_nombre.trace_add("write", lambda *args: _forzar_mayusculas(var_nombre))
    var_placa.trace_add("write", lambda *args: _forzar_mayusculas(var_placa))

    # ================================
    # CAMPOS
    # ================================
    def campo(label, fila, textvariable=None):
        tk.Label(
            form_frame,
            text=label,
            bg=COLOR_FONDO,
            anchor="w",
            font=FONT_LABEL
        ).grid(row=fila, column=0, sticky="w", pady=8, padx=(0, 12))

        entry = tk.Entry(
            form_frame,
            font=FONT_INPUT,
            textvariable=textvariable,
            relief="solid",
            bd=1,
            highlightthickness=0,
            bg="white"
        )
        entry.grid(row=fila, column=1, sticky="ew", pady=8, ipady=6)
        entries.append(entry)
        return entry

    def campo_combo(label, fila, values, textvariable=None):
        tk.Label(
            form_frame,
            text=label,
            bg=COLOR_FONDO,
            anchor="w",
            font=FONT_LABEL
        ).grid(row=fila, column=0, sticky="w", pady=8, padx=(0, 12))

        combo = ttk.Combobox(
            form_frame,
            state="readonly",
            values=values,
            textvariable=textvariable,
            style="Modern.TCombobox"
        )
        combo.grid(row=fila, column=1, sticky="ew", pady=8, ipady=2)
        entries.append(combo)
        return combo

    entry_cedula = campo("Cédula", 0)
    entry_nombre = campo("Nombre", 1, textvariable=var_nombre)
    entry_placa  = campo("Placa", 2, textvariable=var_placa)

    ZONAS = ["METROPOLITANA SUR", "SUROESTE", "ORIENTE", "OCCIDENTE", "NORDESTE"]
    combo_zona = campo_combo("Zona", 3, ZONAS, textvariable=var_zona)

    entry_fecha = campo("Fecha (YYYY-MM-DD)", 4)

    btn_cal = tk.Button(
        form_frame,
        text="📅",
        width=3,
        font=("Segoe UI", 11),
        bg="white",
        fg="black",
        relief="solid",
        bd=1,
        command=lambda: seleccionar_fecha(ventana, entry_fecha)
    )
    btn_cal.grid(row=4, column=2, padx=(10, 0), pady=8, sticky="w", ipady=2)

    entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))

    entry_km    = campo("Kilómetros", 5)
    entry_horas = campo("Horas trabajadas", 6)
    entry_valor = campo("Valor hora extra", 7)

    # ================================
    # LIMPIAR
    # ================================
    def limpiar_campos():
        for w in entries:
            if isinstance(w, tk.Entry):
                w.delete(0, tk.END)
            else:
                try:
                    w.set("")
                except Exception:
                    pass

        entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        entry_cedula.focus_set()

    # ================================
    # GUARDAR
    # ================================
    def guardar():
        try:
            if not entry_cedula.get().strip():
                raise ValueError("La cédula es obligatoria.")
            if not entry_nombre.get().strip():
                raise ValueError("El nombre es obligatorio.")
            if not entry_placa.get().strip():
                raise ValueError("La placa es obligatoria.")
            if not combo_zona.get().strip():
                raise ValueError("La zona es obligatoria.")
            if not entry_fecha.get().strip():
                raise ValueError("La fecha es obligatoria.")

            datetime.strptime(entry_fecha.get().strip(), "%Y-%m-%d")

            data = {
                "cedula": entry_cedula.get().strip(),
                "nombre": entry_nombre.get().strip().upper(),
                "placa": entry_placa.get().strip().upper(),
                "zona": combo_zona.get().strip(),
                "fecha": entry_fecha.get().strip(),
                "kilometro": float(entry_km.get()) if entry_km.get().strip() else None,
                "horas_trabajadas": float(entry_horas.get()) if entry_horas.get().strip() else None,
                "valor_hora_extra": float(entry_valor.get()) if entry_valor.get().strip() else None,
            }

            crear_registro(data)
            messagebox.showinfo("Éxito", "Registro guardado correctamente.", parent=ventana)
            limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=ventana)

    # ================================
    # CERRAR
    # ================================
    def cerrar():
        ventana.destroy()
        parent.deiconify()

    ventana.protocol("WM_DELETE_WINDOW", cerrar)

    # ================================
    # ENTER: avanza por campos y al final guarda
    # ================================
    def focus_siguiente(event, index):
        try:
            entries[index + 1].focus_set()
        except IndexError:
            guardar()

    for i, widget in enumerate(entries):
        widget.bind("<Return>", lambda e, idx=i: focus_siguiente(e, idx))

    # ================================
    # BOTONES (estilo igual a menú principal)
    # ================================
    footer = tk.Frame(ventana, bg=COLOR_FONDO)
    footer.pack(side="bottom", fill="x", pady=(0, 14))

    footer_inner = tk.Frame(footer, bg=COLOR_FONDO)
    footer_inner.pack()

    def _hover(btn, bg):
        btn.configure(bg=bg)

    btn_guardar = tk.Button(
        footer_inner,
        text="Guardar",
        command=guardar,
        font=FONT_BTN,
        bg=BTN_GUARDAR_BG,
        fg="white",
        activebackground=BTN_GUARDAR_HOVER,
        activeforeground="white",
        relief="flat",
        bd=0,
        width=18,
        height=2,
        cursor="hand2"
    )
    btn_guardar.pack(side="left", padx=14)

    btn_salir = tk.Button(
        footer_inner,
        text="Salir",
        command=cerrar,
        font=FONT_BTN,
        bg=BTN_SALIR_BG,
        fg="white",
        activebackground=BTN_SALIR_HOVER,
        activeforeground="white",
        relief="flat",
        bd=0,
        width=18,
        height=2,
        cursor="hand2"
    )
    btn_salir.pack(side="left", padx=14)

    # Hover (igual que menú principal)
    btn_guardar.bind("<Enter>", lambda e: _hover(btn_guardar, BTN_GUARDAR_HOVER))
    btn_guardar.bind("<Leave>", lambda e: _hover(btn_guardar, BTN_GUARDAR_BG))

    btn_salir.bind("<Enter>", lambda e: _hover(btn_salir, BTN_SALIR_HOVER))
    btn_salir.bind("<Leave>", lambda e: _hover(btn_salir, BTN_SALIR_BG))

    entry_cedula.focus_set()
