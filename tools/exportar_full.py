import sys
from pathlib import Path
import pandas as pd

# ============================================================
# FIX PATH (para que "import app..." funcione desde /tools)
# ============================================================
BASE_DIR = Path(__file__).resolve().parents[1]  # .../Informe_ControlHoras_V1
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.data.db import get_connection  # noqa: E402


def main():
    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
          id,
          cedula,
          nombre,
          placa,
          zona,
          fecha,
          kilometro,
          horas_trabajadas,
          valor_hora_extra,
          created_at,
          updated_at
        FROM registros
        ORDER BY id;
        """,
        conn,
    )

    reports_dir = BASE_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)

    out = reports_dir / "export_bd_completa.xlsx"
    df.to_excel(out, index=False)

    print("✅ OK ->", out)


if __name__ == "__main__":
    main()
