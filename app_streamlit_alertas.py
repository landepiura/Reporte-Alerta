# archivo: app_streamlit_alertas.py

import streamlit as st
import pandas as pd

# === 0. Ruta del archivo (relativa, ya no C:\...) ===
ruta_reporte = "reportealerta.xlsx"

# === 1. Leer archivo Excel ===
df = pd.read_excel(ruta_reporte)
