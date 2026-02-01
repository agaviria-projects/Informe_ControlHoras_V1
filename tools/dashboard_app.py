import pandas as pd
import streamlit as st

from app.data.db import get_connection

st.set_page_config(page_title="Dashboard Control de Horas", layout="wide")

@st.cache_data
def cargar_datos():
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
            created_at
        FROM registros
        WHERE deleted = 0
        """,
        conn
    )
    conn.close()

    # Tipos
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    for c in ["kilometro", "horas_trabajadas", "valor_hora_extra"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df["zona"] = df["zona"].fillna("").astype(str)
    df["placa"] = df["placa"].fillna("").astype(str)
    df["cedula"] = df["cedula"].fillna("").astype(str)

    return df

df = cargar_datos()

st.title("📊 Control de Horas - Dashboard (Demo)")

# -----------------------
# FILTROS
# -----------------------
with st.sidebar:
    st.header("Filtros")

    zonas = sorted([z for z in df["zona"].dropna().unique().tolist() if z.strip() != ""])
    zona_sel = st.multiselect("Zona", options=zonas, default=zonas)

    placa_txt = st.text_input("Buscar por Placa (contiene)", value="").strip().upper()
    cedula_txt = st.text_input("Buscar por Cédula (contiene)", value="").strip()

    min_f = df["fecha"].min()
    max_f = df["fecha"].max()
    if pd.notna(min_f) and pd.notna(max_f):
        rango = st.date_input("Rango de fechas", value=(min_f.date(), max_f.date()))
    else:
        rango = None

f = df.copy()

if zona_sel:
    f = f[f["zona"].isin(zona_sel)]

if placa_txt:
    f = f[f["placa"].str.upper().str.contains(placa_txt, na=False)]

if cedula_txt:
    f = f[f["cedula"].str.contains(cedula_txt, na=False)]

if rango and len(rango) == 2:
    ini, fin = pd.to_datetime(rango[0]), pd.to_datetime(rango[1])
    f = f[(f["fecha"] >= ini) & (f["fecha"] <= fin)]

# -----------------------
# KPIs
# -----------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Registros", int(f.shape[0]))
c2.metric("Horas trabajadas", float(f["horas_trabajadas"].fillna(0).sum()))
c3.metric("Valor hora extra (total)", float(f["valor_hora_extra"].fillna(0).sum()))
c4.metric("Placas únicas", int(f["placa"].nunique()))

st.divider()

# -----------------------
# GRÁFICAS
# -----------------------
g1, g2 = st.columns(2)

with g1:
    st.subheader("Horas por Zona")
    horas_zona = (
        f.groupby("zona", dropna=False)["horas_trabajadas"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(horas_zona)

with g2:
    st.subheader("Registros por Fecha")
    regs_fecha = (
        f.dropna(subset=["fecha"])
        .groupby(f["fecha"].dt.date)["id"]
        .count()
        .sort_index()
    )
    st.line_chart(regs_fecha)

st.subheader("Detalle")
st.dataframe(
    f.sort_values(["fecha", "zona"], ascending=[False, True]),
    use_container_width=True
)
