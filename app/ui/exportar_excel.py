import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import pandas as pd

from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

from app.data.repository import buscar_registros


def exportar_a_excel(parent):
    try:
        # ======================================================
        # 1) OBTENER TODOS LOS REGISTROS
        # ======================================================
        rows = buscar_registros(cedula=None, nombre=None, placa=None)

        if not rows:
            messagebox.showwarning(
                "Atención",
                "No hay registros para exportar.",
                parent=parent
            )
            return

        # ======================================================
        # 2) DATOS SOLO PARA EL USUARIO (SIN id / created_at)
        # ======================================================
        data = []
        for r in rows:
            data.append([
                r[1],  # cedula
                r[2],  # nombre
                r[3],  # placa
                r[4],  # fecha
                r[5],  # kilometro
                r[6],  # horas_trabajadas
                r[7],  # valor_hora_extra
            ])

        columnas = [
            "Cédula",
            "Nombre",
            "Placa",
            "Fecha",
            "Kilómetros",
            "Horas trabajadas",
            "Valor Hora Extra",
        ]

        df = pd.DataFrame(data, columns=columnas)

        # ======================================================
        # 3) RUTA /reports
        # ======================================================
        base_dir = Path(__file__).resolve().parents[2]
        reports_dir = base_dir / "reports"
        reports_dir.mkdir(exist_ok=True)

        out = reports_dir / "reporte_control_horas.xlsx"

        # ======================================================
        # 4) EXPORTAR DATAFRAME
        # ======================================================
        df.to_excel(out, index=False)

        # ======================================================
        # 5) CONVERTIR A TABLA ESTRUCTURADA
        # ======================================================
        wb = load_workbook(out)
        ws = wb.active

        last_row = ws.max_row
        last_col = ws.max_column

        col_letter = chr(64 + last_col)
        table_ref = f"A1:{col_letter}{last_row}"

        tabla = Table(
            displayName="TablaControlHoras",
            ref=table_ref
        )

        estilo = TableStyleInfo(
            name="TableStyleMedium9",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False
        )

        tabla.tableStyleInfo = estilo
        ws.add_table(tabla)

        wb.save(out)

        # ======================================================
        # 6) MENSAJE FINAL
        # ======================================================
        messagebox.showinfo(
            "Éxito",
            f"Excel generado como tabla estructurada:\n{out}",
            parent=parent
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Ocurrió un error:\n{e}",
            parent=parent
        )

