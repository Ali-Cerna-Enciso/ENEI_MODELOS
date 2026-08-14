import streamlit as st
from pathlib import Path

# Entrada única para Streamlit Cloud: selector de modelo arriba (centrado)
# y la app elegida debajo, con el formulario y el resultado en el centro.

st.set_page_config(page_title="ENAHO 2023 — Modelos ML", layout="wide")

_, h, _ = st.columns([1, 4, 1])
with h:
    st.markdown(
        "<h1 style='text-align:center; margin-bottom:0;'>ENAHO 2023 — Modelos ML</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; color:#888;'>Ingreso laboral e informalidad · "
        "curso ML en producción (ENEI/INEI)</p>",
        unsafe_allow_html=True,
    )
    modelo = st.segmented_control(
        "Modelo",
        options=["Regresión de ingreso", "Clasificación de informalidad"],
        default="Regresión de ingreso",
        label_visibility="collapsed",
        width="stretch",
    )
if modelo is None:
    modelo = "Regresión de ingreso"

ARCHIVOS = {
    "Regresión de ingreso": "app_regresion.py",
    "Clasificación de informalidad": "app_clasificacion.py",
}

ruta_app = Path(__file__).parent / ARCHIVOS[modelo]
codigo = compile(ruta_app.read_text(encoding="utf-8"), str(ruta_app), "exec")
exec(codigo, {"__file__": str(ruta_app), "__name__": "__main__"})
