import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date

try:
    # Opcional: si tienes tkcalendar instalado, se verá como calendario real
    from tkcalendar import Calendar
except Exception:
    Calendar = None


# ============================================================
# FESTIVOS (ejemplo) -> agrega/ajusta los que necesites
# ============================================================
FESTIVOS = {
    # 2026
    date(2026, 1, 1), date(2026, 1, 12), date(2026, 3, 23), date(2026, 4, 2), date(2026, 4, 3),
    date(2026, 5, 1), date(2026, 5, 18), date(2026, 6, 8), date(2026, 6, 15), date(2026, 6, 29),
    date(2026, 7, 20), date(2026, 8, 7), date(2026, 8, 17), date(2026, 10, 12), date(2026, 11, 2),
    date(2026, 11, 16), date(2026, 12, 8), date(2026, 12, 25),

    # 2027
    date(2027, 1, 1), date(2027, 1, 11), date(2027, 3, 22), date(2027, 4, 1), date(2027, 4, 2),
    date(2027, 5, 1), date(2027, 5, 24), date(2027, 6, 14), date(2027, 6, 21), date(2027, 7, 20),
    date(2027, 8, 7), date(2027, 8, 16), date(2027, 10, 18), date(2027, 11, 1), date(2027, 11, 15),
    date(2027, 12, 8), date(2027, 12, 25),

    # 2028
    date(2028, 1, 1), date(2028, 1, 10), date(2028, 3, 20), date(2028, 4, 13), date(2028, 4, 14),
    date(2028, 5, 1), date(2028, 5, 29), date(2028, 6, 19), date(2028, 6, 26), date(2028, 7, 20),
    date(2028, 8, 7), date(2028, 8, 21), date(2028, 10, 16), date(2028, 11, 6), date(2028, 11, 13),
    date(2028, 12, 8), date(2028, 12, 25),
}


def seleccionar_fecha(parent, entry_target=None, formato="%Y-%m-%d", initial_date=None, festivos=None):
    """
    Abre un selector de fecha.
    - Si entry_target se pasa, escribe ahí la fecha elegida.
    - Retorna el string de fecha en el formato indicado o None si cancelan.

    Recomendado:
      pip install tkcalendar babel
    """

    fecha_seleccionada = {"value": None}

    # Si no pasan festivos, usamos los del módulo
    if festivos is None:
        festivos = FESTIVOS

    win = tk.Toplevel(parent)
    win.title("Seleccionar fecha")
    win.resizable(False, False)
    win.grab_set()

    # Centrar ventana
    win.update_idletasks()
    w, h = 340, 340 if Calendar else 180
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

    frame = tk.Frame(win, padx=12, pady=12)
    frame.pack(fill="both", expand=True)

    # Fecha inicial
    if initial_date:
        try:
            base = datetime.strptime(initial_date, formato)
        except Exception:
            base = datetime.now()
    else:
        base = datetime.now()

    if Calendar:
        # ============================================================
        # CALENDARIO EN ESPAÑOL + LUNES PRIMERO
        # ============================================================
        # locale="es_ES" -> meses/días en español (requiere babel)
        # firstweekday="monday" -> Lun ... Dom
        try:
            cal = Calendar(
                frame,
                selectmode="day",
                year=base.year,
                month=base.month,
                day=base.day,
                date_pattern="y-mm-dd",  # YYYY-MM-DD
                locale="es_ES",
                firstweekday="monday"
            )
        except Exception:
            # Si falla locale (por falta de babel), cae a default
            cal = Calendar(
                frame,
                selectmode="day",
                year=base.year,
                month=base.month,
                day=base.day,
                date_pattern="y-mm-dd",
                firstweekday="monday"
            )

        cal.pack(pady=(0, 10))

        # ============================================================
        # FESTIVOS EN ROJO
        # ============================================================
        try:
            cal.tag_config("festivo", background="#d32f2f", foreground="white")
            for f in festivos:
                # f debe ser datetime.date
                if isinstance(f, date):
                    cal.calevent_create(f, "Festivo", "festivo")
        except Exception:
            # Si algo falla en tags/eventos, no rompemos el selector
            pass

        def confirmar():
            val = cal.get_date()  # YYYY-MM-DD (por date_pattern)
            try:
                datetime.strptime(val, "%Y-%m-%d")
            except Exception:
                messagebox.showerror("Error", "Fecha inválida.", parent=win)
                return

            fecha_seleccionada["value"] = val
            if entry_target is not None:
                entry_target.delete(0, tk.END)
                entry_target.insert(0, val)
            win.destroy()

    else:
        # Fallback: sin tkcalendar, entrada manual
        tk.Label(
            frame,
            text="No se encontró 'tkcalendar'.\nEscribe la fecha (YYYY-MM-DD):"
        ).pack(pady=(0, 8))

        e = tk.Entry(frame, width=20)
        e.pack()
        e.insert(0, base.strftime("%Y-%m-%d"))

        def confirmar():
            val = e.get().strip()
            try:
                datetime.strptime(val, "%Y-%m-%d")
            except Exception:
                messagebox.showerror("Error", "Formato inválido. Use YYYY-MM-DD.", parent=win)
                return

            fecha_seleccionada["value"] = val
            if entry_target is not None:
                entry_target.delete(0, tk.END)
                entry_target.insert(0, val)
            win.destroy()

    botones = tk.Frame(frame)
    botones.pack(pady=10)

    tk.Button(botones, text="Aceptar", width=12, command=confirmar).pack(side="left", padx=6)
    tk.Button(botones, text="Cancelar", width=12, command=win.destroy).pack(side="left", padx=6)

    parent.wait_window(win)
    return fecha_seleccionada["value"]
