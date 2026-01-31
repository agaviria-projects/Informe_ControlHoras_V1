import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from app.data.repository import crear_registro


def abrir_formulario_registro(parent):
    parent.withdraw()

    ventana = tk.Toplevel(parent)
    ventana.withdraw()              # ① ocultar
    ventana.title("Nuevo Registro - Control de Horas")
    ventana.geometry("480x520")
    ventana.resizable(False, False)
    ventana.grab_set()

    # colores / widgets / frames …

    ventana.update_idletasks()       # ② calcular tamaño
    ancho = 480
    alto = 520
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    ventana.deiconify()              # ③ mostrar SIN parpadeo

    COLOR_VERDE = "#1f7a4d"
    COLOR_FONDO = "#f2f2f2"
    ventana.configure(bg=COLOR_FONDO)

    # ================================
    # CENTRAR VENTANA EN PANTALLA
    # ================================
    ventana.update_idletasks()
    ancho = 480
    alto = 520
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ================================
    # HEADER
    # ================================
    header = tk.Frame(ventana, bg=COLOR_VERDE, height=45)
    header.pack(fill="x")

    tk.Label(
        header,
        text="NUEVO REGISTRO",
        bg=COLOR_VERDE,
        fg="white",
        font=("Segoe UI", 11, "bold")
    ).pack(pady=10)

    # ================================
    # FORMULARIO
    # ================================
    form_frame = tk.Frame(ventana, bg=COLOR_FONDO)
    form_frame.pack(padx=30, pady=20, fill="x")

    entries = []

    # ============================================================
    # NUEVO: variables para forzar MAYÚSCULAS mientras escribe
    # ============================================================
    var_nombre = tk.StringVar()
    var_placa = tk.StringVar()

    def _forzar_mayusculas(var: tk.StringVar):
        v = var.get()
        up = v.upper()
        if v != up:
            var.set(up)

    # Cuando cambie el texto, lo convertimos a mayúsculas
    var_nombre.trace_add("write", lambda *args: _forzar_mayusculas(var_nombre))
    var_placa.trace_add("write", lambda *args: _forzar_mayusculas(var_placa))

    def campo(label, fila, textvariable=None):
        tk.Label(
            form_frame,
            text=label,
            bg=COLOR_FONDO,
            anchor="w",
            font=("Segoe UI", 9, "bold")
        ).grid(row=fila, column=0, sticky="w", pady=6)

        entry = tk.Entry(form_frame, width=30, textvariable=textvariable)
        entry.grid(row=fila, column=1, pady=6)
        entries.append(entry)
        return entry

    entry_cedula = campo("Cédula", 0)
    entry_nombre = campo("Nombre", 1, textvariable=var_nombre)  # ✅ ahora fuerza mayúsculas
    entry_placa = campo("Placa", 2, textvariable=var_placa)     # ✅ ahora fuerza mayúsculas
    entry_fecha = campo("Fecha (YYYY-MM-DD)", 3)
    entry_km = campo("Kilómetros", 4)
    entry_horas = campo("Horas trabajadas", 5)
    entry_valor = campo("Valor hora extra", 6)

    entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))

    # ================================
    # NAVEGACIÓN CON ENTER
    # ================================
    def focus_siguiente(event, index):
        try:
            entries[index + 1].focus_set()
        except IndexError:
            btn_guardar.focus_set()

    for i, entry in enumerate(entries):
        entry.bind("<Return>", lambda e, idx=i: focus_siguiente(e, idx))

    # ================================
    # LIMPIAR CAMPOS
    # ================================
    def limpiar_campos():
        for e in entries:
            e.delete(0, tk.END)
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

            datetime.strptime(entry_fecha.get(), "%Y-%m-%d")

            data = {
                "cedula": entry_cedula.get().strip(),
                "nombre": entry_nombre.get().strip().upper(),  # se mantiene
                "placa": entry_placa.get().strip().upper(),    # se mantiene
                "fecha": entry_fecha.get().strip(),
                "kilometro": float(entry_km.get()) if entry_km.get() else None,
                "horas_trabajadas": float(entry_horas.get()) if entry_horas.get() else None,
                "valor_hora_extra": float(entry_valor.get()) if entry_valor.get() else None,
            }

            crear_registro(data)

            messagebox.showinfo(
                "Éxito",
                "Registro guardado correctamente.",
                parent=ventana
            )

            limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=ventana)

    # ================================
    # CIERRE CONTROLADO
    # ================================
    def cerrar():
        ventana.destroy()
        parent.deiconify()  # 👈 vuelve a mostrar la principal

    ventana.protocol("WM_DELETE_WINDOW", cerrar)

    # ================================
    # BOTONES
    # ================================
    botones = tk.Frame(ventana, bg=COLOR_FONDO)
    botones.pack(pady=20)

    btn_guardar = tk.Button(
        botones,
        text="Guardar",
        width=15,
        bg=COLOR_VERDE,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        command=guardar
    )
    btn_guardar.pack(side="left", padx=10)

    tk.Button(
        botones,
        text="Salir",
        width=15,
        bg="#888888",
        fg="white",
        font=("Segoe UI", 10),
        command=cerrar
    ).pack(side="left", padx=10)

    entry_cedula.focus_set()
