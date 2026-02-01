from datetime import datetime
from app.data.db import get_connection


# --------------------------------------------------
# CREATE
# --------------------------------------------------
def crear_registro(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO registros (
            cedula,
            nombre,
            placa,
            zona,
            fecha,
            kilometro,
            horas_trabajadas,
            valor_hora_extra,
            created_at,
            deleted
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
    """, (
        data["cedula"],
        data["nombre"],
        data["placa"],
        data.get("zona"),
        data["fecha"],
        data.get("kilometro"),
        data.get("horas_trabajadas"),
        data.get("valor_hora_extra"),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


# --------------------------------------------------
# READ (BÚSQUEDA)
# --------------------------------------------------
def buscar_registros(cedula=None, nombre=None, placa=None, zona=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            id,                 -- 0
            cedula,             -- 1
            nombre,             -- 2
            placa,              -- 3
            fecha,              -- 4
            kilometro,          -- 5
            horas_trabajadas,   -- 6
            valor_hora_extra,   -- 7
            created_at,         -- 8
            NULL as updated_at, -- 9  (dummy para mantener índices)
            deleted,            -- 10
            zona                -- 11
        FROM registros
        WHERE deleted = 0
    """
    params = []

    if cedula:
        query += " AND cedula LIKE ?"
        params.append(f"%{cedula}%")

    if nombre:
        query += " AND nombre LIKE ?"
        params.append(f"%{nombre}%")

    if placa:
        query += " AND placa LIKE ?"
        params.append(f"%{placa}%")

    if zona:
        query += " AND zona LIKE ?"
        params.append(f"%{zona}%")

    query += " ORDER BY id DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


# --------------------------------------------------
# UPDATE
# --------------------------------------------------
def actualizar_registro(id_registro: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE registros
        SET
            cedula = ?,
            nombre = ?,
            placa = ?,
            zona=?,
            fecha = ?,
            kilometro = ?,
            horas_trabajadas = ?,
            valor_hora_extra = ?,
            updated_at = ?
        WHERE id = ? AND deleted = 0
    """, (
        data["cedula"],
        data["nombre"],
        data["placa"],
        data.get("zona"),
        data["fecha"],
        data.get("kilometro"),
        data.get("horas_trabajadas"),
        data.get("valor_hora_extra"),
        datetime.now().isoformat(),
        id_registro
    ))

    conn.commit()
    conn.close()


# --------------------------------------------------
# DELETE LÓGICO
# --------------------------------------------------
def eliminar_registro(id_registro: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE registros
        SET deleted = 1,
            updated_at = ?
        WHERE id = ?
    """, (
        datetime.now().isoformat(),
        id_registro
    ))

    conn.commit()
    conn.close()
