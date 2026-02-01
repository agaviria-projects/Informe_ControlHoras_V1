import sys
from pathlib import Path

# =========================
# MODO DEMO (ocultar columnas internas)
# =========================
DEMO_OCULTAR_COLUMNAS = True
COLUMNAS_OCULTAS_DEMO = {"id", "created_at", "updated_at", "deleted"}

# ============================================================
# FIX PATH (para que "import app..." funcione desde /tools)
# ============================================================
BASE_DIR = Path(__file__).resolve().parents[1]  # .../Informe_ControlHoras_V1
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.data.db import get_connection  # noqa: E402


BLOQUEADAS = (
    "DROP ",
    "DELETE ",
    "TRUNCATE ",
    "ALTER TABLE registros DROP",
)


def es_peligrosa(sql: str) -> bool:
    sql_upper = sql.upper().strip()
    return any(sql_upper.startswith(x) for x in BLOQUEADAS)

def imprimir_resultados(cursor, rows):
    if not rows:
        print("⚠️ Sin resultados.")
        return

    columnas_full = [desc[0] for desc in cursor.description]

    # Filtrar columnas si está activo el modo demo
    if DEMO_OCULTAR_COLUMNAS:
        idx_visibles = [i for i, c in enumerate(columnas_full) if c not in COLUMNAS_OCULTAS_DEMO]
        columnas = [columnas_full[i] for i in idx_visibles]
    else:
        idx_visibles = list(range(len(columnas_full)))
        columnas = columnas_full


    def _fmt(v, col_name=""):
        if v is None:
            return ""
        s = str(v)

        # Formato bonito para fechas ISO (created_at / updated_at)
        if col_name in ("created_at", "updated_at"):
            # 2026-01-31T18:32:29.010568  ->  2026-01-31 18:32:29
            if "T" in s:
                s = s.replace("T", " ")
            if "." in s:
                s = s.split(".", 1)[0]
            # limitar a 19 chars: YYYY-MM-DD HH:MM:SS
            s = s[:19]

        # Evitar columnas kilométricas si algo se alarga (excepto 'file')
        if col_name != "file" and len(s) > 40:
            s = s[:37] + "..."

        return s

     # Aplicar formato SOLO a las columnas visibles (modo demo)
    filas_fmt = []
    for fila in rows:
        fila_vis = []
        for pos, idx in enumerate(idx_visibles):
            col_name = columnas[pos]
            fila_vis.append(_fmt(fila[idx], col_name))
        filas_fmt.append(fila_vis)

    # calcular ancho real por columna (con valores ya formateados)
    anchos = []
    for i, col in enumerate(columnas):
        max_len = len(col)
        for fila in filas_fmt:
            max_len = max(max_len, len(fila[i]))
        anchos.append(max_len + 2)

    def linea():
        print("+" + "+".join("-" * a for a in anchos) + "+")

    linea()
    print("|" + "|".join(columnas[i].center(anchos[i]) for i in range(len(columnas))) + "|")
    linea()

    for fila in filas_fmt:
        print("|" + "|".join(fila[i].ljust(anchos[i]) for i in range(len(columnas))) + "|")

    linea()
    print(f"📊 Filas: {len(rows)}\n")


def main():
    print("\n🟢 CONSOLA SQL – SQLite (Modo Seguro)")
    print("Escribe SQL y presiona ENTER")
    print("Escribe 'exit' para salir\n")

    conn = get_connection()
    cursor = conn.cursor()

    while True:
        try:
            sql = input("SQL> ").strip()

            if not sql:
                continue

            if sql.lower() in ("exit", "quit"):
                print("👋 Cerrando consola SQL.")
                break

            if es_peligrosa(sql):
                print("⛔ Comando bloqueado por seguridad.")
                continue

            cursor.execute(sql)

            if sql.lower().startswith("select") or sql.lower().startswith("pragma"):
                rows = cursor.fetchall()
                imprimir_resultados(cursor, rows)
            else:
                conn.commit()
                print("✅ Comando ejecutado correctamente.")

        except Exception as e:
            print("❌ Error:", e)

    conn.close()


if __name__ == "__main__":
    main()
