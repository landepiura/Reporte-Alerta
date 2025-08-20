# archivo: app_streamlit_alertas.py

import streamlit as st
import pandas as pd

# === 0. Ruta del archivo (relativa, ya no C:\...) ===
ruta_reporte = "reportealerta.xlsx"

# === 1. Leer archivo Excel ===
df = pd.read_excel(ruta_reporte)

# === 2. Calcular diferencia PIM - devengado acumulado ===
if 'devengado_acumulado_mes_anterior' in df.columns and 'mto_pim' in df.columns:
    df['diferencia'] = df['mto_pim'] - df['devengado_acumulado_mes_anterior']

# === 3. Título ===
st.title("📊 Reporte de Alertas de Devengados")

# === 4. Filtro por Unidad Ejecutora ===
ue_filtrado = st.multiselect(
    "Selecciona Unidad Ejecutora:",
    options=df['UE_alertas'].unique(),
    default=df['UE_alertas'].unique()
)

df_filtrado = df[df['UE_alertas'].isin(ue_filtrado)]

# === 5. Mostrar tabla ===
st.subheader("Tabla de alertas")
st.dataframe(df_filtrado)

# === 6. Estadísticas resumen ===
st.subheader("Resumen por Unidad Ejecutora")
resumen = df_filtrado.groupby('UE_alertas')[['mto_pim', 'devengado_acumulado_mes_anterior', 'diferencia']].sum()
st.dataframe(resumen)

# === 7. Gráfico de barras de diferencia ===
st.subheader("Diferencia PIM - Devengado acumulado")
st.bar_chart(resumen['diferencia'])
