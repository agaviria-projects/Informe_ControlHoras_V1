import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import pandas as pd

from app.data.repository import buscar_registros


def exportar_a_excel(parent):
    try:
        # Trae todo
        rows = buscar_registros(cedula=None, nombre=None, placa=None)

        if not rows:
            messagebox.showwarning("Atención", "No hay registros para exportar.", parent=parent)
            return

        # Ajusta a las 9 columnas base del grid
        data = []
        for r in rows:
            r = list(r)
            data.append(r[:9])  # id..created_at

        cols = ["id", "cedula", "nombre", "placa", "fecha", "kilometro", "horas_trabajadas", "valor_hora_extra", "created_at"]
        df = pd.DataFrame(data, columns=cols)

        # Carpeta reports en raíz del proyecto
        base_dir = Path(__file__).resolve().parents[2]
        reports_dir = base_dir / "reports"
        reports_dir.mkdir(exist_ok=True)

        out = reports_dir / "reporte_control_horas.xlsx"
        df.to_excel(out, index=False)

        messagebox.showinfo("Éxito", f"Archivo generado:\n{out}", parent=parent)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error:\n{e}", parent=parent)
