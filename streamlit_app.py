import streamlit as st
from pathlib import Path

# Entrada única para Streamlit Cloud: elige entre los dos modelos del proyecto.
# Reutiliza las apps de la raíz (misma lógica de formulario y predicción).

st.set_page_config(page_title="ENAHO 2023 — Modelos ML", layout="wide")

st.sidebar.markdown("## ENAHO 2023 — Modelos ML")
modelo = st.sidebar.radio(
    "Selecciona el modelo",
    ["Regresión de ingreso", "Clasificación de informalidad"],
)

ARCHIVOS = {
    "Regresión de ingreso": "app_regresion.py",
    "Clasificación de informalidad": "app_clasificacion.py",
}

ruta_app = Path(__file__).parent / ARCHIVOS[modelo]
codigo = compile(ruta_app.read_text(encoding="utf-8"), str(ruta_app), "exec")
exec(codigo, {"__file__": str(ruta_app), "__name__": "__main__"})
