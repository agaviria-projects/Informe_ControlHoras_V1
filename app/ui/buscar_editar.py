import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from app.data.repository import buscar_registros, actualizar_registro, eliminar_registro


def abrir_buscar_editar(parent):
    parent.withdraw()

    ventana = tk.Toplevel(parent)
    ventana.withdraw()
    ventana.title("Buscar / Editar registros - Control de Horas")
    ventana.geometry("1300x550")
    ventana.resizable(True, True)
    ventana.grab_set()

    COLOR_VERDE = "#1f7a4d"
    COLOR_FONDO = "#f2f2f2"
    ventana.configure(bg=COLOR_FONDO)

    ventana.update_idletasks()
    ancho = 1300
    alto = 550
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)-80
    if y < 0:
     y = 0
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    ventana.deiconify()
    ventana.lift()
    ventana.focus_force()

    def _cerrar_y_restaurar_parent():
        try:
            try:
                ventana.grab_release()
            except Exception:
                pass
            ventana.destroy()
        finally:
            try:
                parent.deiconify()
                parent.lift()
                parent.focus_force()
            except Exception:
                pass

    ventana.protocol("WM_DELETE_WINDOW", _cerrar_y_restaurar_parent)

    header = tk.Frame(ventana, bg=COLOR_VERDE, height=45)
    header.pack(fill="x")

    tk.Label(
        header,
        text="BUSCAR / EDITAR REGISTROS",
        bg=COLOR_VERDE,
        fg="white",
        font=("Segoe UI", 11, "bold")
    ).pack(padx=20, pady=10)

    filtros = tk.Frame(ventana, bg=COLOR_FONDO)
    filtros.pack(fill="x", padx=14, pady=(12, 6))

    tk.Label(filtros, text="Cédula:", bg=COLOR_FONDO, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w")
    entry_cedula = tk.Entry(filtros, width=18)
    entry_cedula.grid(row=0, column=1, padx=(6, 14), pady=4)

    tk.Label(filtros, text="Nombre:", bg=COLOR_FONDO, font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w")
    entry_nombre = tk.Entry(filtros, width=22)
    entry_nombre.grid(row=0, column=3, padx=(6, 14), pady=4)

    tk.Label(filtros, text="Placa:", bg=COLOR_FONDO, font=("Segoe UI", 9, "bold")).grid(row=0, column=4, sticky="w")
    entry_placa = tk.Entry(filtros, width=12)
    entry_placa.grid(row=0, column=5, padx=(6, 14), pady=4)

    tk.Label(filtros, text="Zona:", bg=COLOR_FONDO, font=("Segoe UI", 9, "bold")).grid(row=0, column=6, sticky="w")
    entry_zona = tk.Entry(filtros, width=18)
    entry_zona.grid(row=0, column=7, padx=(6, 14), pady=4)

    lbl_total = tk.Label(filtros, text="Total: 0", bg=COLOR_FONDO, fg="#0d3b2e", font=("Segoe UI", 9, "bold"))
    lbl_total.grid(row=0, column=8, sticky="e", padx=(10, 0))
    filtros.grid_columnconfigure(8, weight=1)

    grid_frame = tk.Frame(ventana, bg=COLOR_FONDO)
    grid_frame.pack(fill="both", expand=True, padx=14, pady=10)

    columnas = (
        "id", "cedula", "nombre", "placa","zona", "fecha",
        "kilometro", "horas_trabajadas", "valor_hora_extra", "created_at"
    )

    tree = ttk.Treeview(grid_frame, columns=columnas, show="headings", height=14)
    tree.pack(side="left", fill="both", expand=True)

    vsb = ttk.Scrollbar(grid_frame, orient="vertical", command=tree.yview)
    vsb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vsb.set)

    tree.heading("id", text="ID")
    tree.heading("cedula", text="Cédula")
    tree.heading("nombre", text="Nombre")
    tree.heading("placa", text="Placa")
    tree.heading("zona", text="Zona")
    tree.heading("fecha", text="Fecha")
    tree.heading("kilometro", text="KM")
    tree.heading("horas_trabajadas", text="Horas")
    tree.heading("valor_hora_extra", text="Valor H.E.")
    tree.heading("created_at", text="Creado")

    tree.column("id", width=55, anchor="center")
    tree.column("cedula", width=110, anchor="w")
    tree.column("nombre", width=220, anchor="w")
    tree.column("placa", width=80, anchor="center")
    tree.column("zona", width=170, anchor="center")
    tree.column("fecha", width=110, anchor="center")
    tree.column("kilometro", width=80, anchor="e")
    tree.column("horas_trabajadas", width=90, anchor="e")
    tree.column("valor_hora_extra", width=110, anchor="e")
    tree.column("created_at", width=200, anchor="center")

    def limpiar_tree():
        for item in tree.get_children():
            tree.delete(item)

    def cargar_datos():
        limpiar_tree()

        cedula = entry_cedula.get().strip() or None
        nombre = entry_nombre.get().strip() or None
        placa = entry_placa.get().strip() or None
        zona = entry_zona.get().strip() or None

        rows = buscar_registros(cedula=cedula, nombre=nombre, placa=placa,zona=zona)

        count = 0
        for r in rows:
            r = list(r)

            base = (
                r[0],   # id
                r[1],   # cedula
                r[2],   # nombre
                r[3],   # placa
                r[11],  # zona  ✅ (al final)
                r[4],   # fecha ✅
                r[5],   # kilometro
                r[6],   # horas_trabajadas
                r[7],   # valor_hora_extra
                r[8],   # created_at
            )

            tree.insert("", "end", values=base)
            count += 1
            
        lbl_total.config(text=f"Total: {count}")

    def limpiar_filtros():
        entry_cedula.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_placa.delete(0, tk.END)
        entry_zona.delete(0, tk.END)
        cargar_datos()

    def eliminar_desde_fila():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un registro para eliminar.", parent=ventana)
            return

        vals = tree.item(sel[0], "values")
        id_registro = int(vals[0])

        ok = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Seguro que deseas eliminar el registro ID {id_registro}?\n\nEsta acción no se puede deshacer.",
            parent=ventana
        )
        if not ok:
            return

        try:
            eliminar_registro(id_registro)
            messagebox.showinfo("Éxito", f"Registro ID {id_registro} eliminado.", parent=ventana)
            cargar_datos()
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{ex}", parent=ventana)

    def abrir_editor_desde_fila():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un registro para editar.", parent=ventana)
            return

        vals = tree.item(sel[0], "values")
        id_registro = int(vals[0])

        edit = tk.Toplevel(ventana)
        edit.transient(ventana)
        edit.grab_set()
        edit.title(f"Editar registro ID {id_registro}")
        edit.geometry("480x420")
        edit.resizable(False, False)
        edit.configure(bg=COLOR_FONDO)

        head2 = tk.Frame(edit, bg=COLOR_VERDE, height=45)
        head2.pack(fill="x")
        tk.Label(head2, text="EDITAR REGISTRO", bg=COLOR_VERDE, fg="white",
                 font=("Segoe UI", 11, "bold")).pack(pady=10)

        frm = tk.Frame(edit, bg=COLOR_FONDO)
        frm.pack(padx=24, pady=18, fill="x")

        def fila(label, valor, i):
            tk.Label(frm, text=label, bg=COLOR_FONDO, font=("Segoe UI", 9, "bold")).grid(row=i, column=0, sticky="w", pady=6)
            e = tk.Entry(frm, width=30)
            e.grid(row=i, column=1, pady=6)
            if valor is not None:
                e.insert(0, str(valor))
            return e

        e_ced = fila("Cédula", vals[1], 0)
        e_nom = fila("Nombre", vals[2], 1)
        e_pla = fila("Placa", vals[3], 2)
        e_zon = fila("Zona", vals[4], 3)
        e_fec = fila("Fecha (YYYY-MM-DD)", vals[5], 4)
        e_km  = fila("Kilómetros", vals[6], 5)
        e_hor = fila("Horas trabajadas", vals[7], 6)
        e_val = fila("Valor hora extra", vals[8], 7)

        entries = [e_ced, e_nom, e_pla,e_zon, e_fec, e_km, e_hor, e_val]

        def focus_sig(event, idx):
            try:
                entries[idx + 1].focus_set()
            except IndexError:
                btn_save.focus_set()

        for i, ent in enumerate(entries):
            ent.bind("<Return>", lambda ev, idx=i: focus_sig(ev, idx))

        def guardar_cambios():
            try:
                if not e_ced.get().strip():
                    raise ValueError("La cédula es obligatoria.")
                if not e_nom.get().strip():
                    raise ValueError("El nombre es obligatorio.")
                if not e_pla.get().strip():
                    raise ValueError("La placa es obligatoria.")
                if not e_zon.get().strip():
                    raise ValueError("La zona es obligatoria.")

                datetime.strptime(e_fec.get().strip(), "%Y-%m-%d")

                data = {
                    "cedula": e_ced.get().strip(),
                    "nombre": e_nom.get().strip().upper(),
                    "placa": e_pla.get().strip().upper(),
                    "zona": e_zon.get().strip(),
                    "fecha": e_fec.get().strip(),
                    "kilometro": float(e_km.get()) if e_km.get().strip() else None,
                    "horas_trabajadas": float(e_hor.get()) if e_hor.get().strip() else None,
                    "valor_hora_extra": float(e_val.get()) if e_val.get().strip() else None,
                }

                actualizar_registro(id_registro, data)
                messagebox.showinfo("Éxito", "Registro actualizado correctamente.", parent=edit)
                edit.destroy()
                cargar_datos()

            except ValueError as ex:
                messagebox.showerror("Error de validación", str(ex), parent=edit)
            except Exception as ex:
                messagebox.showerror("Error", f"Ocurrió un error:\n{ex}", parent=edit)

        btns2 = tk.Frame(edit, bg=COLOR_FONDO)
        btns2.pack(pady=12)

        btn_save = tk.Button(btns2, text="Guardar cambios", width=16, bg=COLOR_VERDE, fg="white",
                             font=("Segoe UI", 10, "bold"), command=guardar_cambios)
        btn_save.pack(side="left", padx=10)
        btn_save.bind("<Return>", lambda e: guardar_cambios())

        tk.Button(btns2, text="Cerrar", width=12, bg="#888888", fg="white",
                  font=("Segoe UI", 10), command=edit.destroy).pack(side="left", padx=10)

        e_ced.focus_set()

    tree.bind("<Double-1>", lambda e: abrir_editor_desde_fila())
    tree.bind("<Delete>", lambda e: eliminar_desde_fila())

    acciones = tk.Frame(ventana, bg=COLOR_FONDO)
    acciones.pack(fill="x", padx=14, pady=(0, 14))

    tk.Button(
        acciones, text="Buscar", width=12, bg=COLOR_VERDE, fg="white",
        font=("Segoe UI", 10, "bold"), command=cargar_datos
    ).pack(side="left", padx=(0, 10))

    tk.Button(
        acciones, text="Limpiar", width=12, bg="#888888", fg="white",
        font=("Segoe UI", 10), command=limpiar_filtros
    ).pack(side="left", padx=(0, 10))

    tk.Button(
        acciones, text="Editar seleccionado", width=16, bg="#0d3b2e", fg="white",
        font=("Segoe UI", 10, "bold"), command=abrir_editor_desde_fila
    ).pack(side="left", padx=(0, 10))

    tk.Button(
        acciones, text="Eliminar seleccionado", width=18, bg="#b03a2e", fg="white",
        font=("Segoe UI", 10, "bold"), command=eliminar_desde_fila
    ).pack(side="left", padx=(0, 10))

    tk.Button(
        acciones, text="Cerrar", width=12, bg="#8b2c1f", fg="white",
        font=("Segoe UI", 10, "bold"), command=_cerrar_y_restaurar_parent
    ).pack(side="right")

    entry_cedula.bind("<Return>", lambda e: cargar_datos())
    entry_nombre.bind("<Return>", lambda e: cargar_datos())
    entry_placa.bind("<Return>", lambda e: cargar_datos())
    entry_zona.bind("<Return>", lambda e: cargar_datos())

    try:
        cargar_datos()
    except Exception as ex:
        messagebox.showerror(
            "Error al cargar registros",
            f"No se pudo cargar la información inicial.\n\nDetalle:\n{ex}",
            parent=ventana
        )
        _cerrar_y_restaurar_parent()
