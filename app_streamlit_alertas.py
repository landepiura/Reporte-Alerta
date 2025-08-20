import streamlit as st
import pandas as pd

# === 0. Ruta del archivo (relativa) ===
ruta_reporte = "reportealerta.xlsx"

# === 1. Leer archivo Excel desde la hoja correcta ===
df = pd.read_excel(ruta_reporte, sheet_name="Sheet1")

# === 2. Normalizar nombres de columnas (evita espacios ocultos) ===
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(" ", "_")
df.columns = df.columns.str.lower()

# Ver columnas disponibles (debug)
st.write("📂 Columnas detectadas:", df.columns.tolist())

# === 3. Calcular diferencia PIM - devengado acumulado ===
if "devengado_acumulado_mes_anterior" in df.columns and "mto_pim" in df.columns:
    df["diferencia"] = df["mto_pim"] - df["devengado_acumulado_mes_anterior"]

# === 4. Título ===
st.title("📊 Reporte de Alertas de Devengados")

# === 5. Filtro por Unidad Ejecutora (columna T → ue_alertas) ===
if "ue_alertas" in df.columns:
    ue_filtrado = st.multiselect(
        "Selecciona Unidad Ejecutora:",
        options=df["ue_alertas"].unique(),
        default=df["ue_alertas"].unique()
    )

    df_filtrado = df[df["ue_alertas"].isin(ue_filtrado)]

    # === 6. Mostrar tabla ===
    st.subheader("Tabla de alertas")
    st.dataframe(df_filtrado)

    # === 7. Estadísticas resumen ===
    st.subheader("Resumen por Unidad Ejecutora")
    resumen = df_filtrado.groupby("ue_alertas")[["mto_pim", "devengado_acumulado_mes_anterior", "diferencia"]].sum()
    st.dataframe(resumen)

    # === 8. Gráfico de barras ===
    st.subheader("Diferencia PIM - Devengado acumulado")
    st.bar_chart(resumen["diferencia"])
else:
    st.error("❌ No se encontró la columna 'UE_alertas' en la hoja Sheet1.")
