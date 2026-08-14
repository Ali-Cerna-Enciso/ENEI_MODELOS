import numpy as np
import pandas as pd
import streamlit as st
from joblib import load
from pathlib import Path

from formulario import observacion

# Cargar el modelo de regresión (pipeline completo: transformaciones + modelo)
regressor = load(Path(__file__).parent / "modelos" / "regresor_ingreso.joblib")

st.markdown(
    "<h2 style='text-align:center;'>Modelo de Regresión: Ingreso Anual</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; color:#888;'>Predicción del ingreso anual del "
    "trabajo principal (ENAHO 2023, Módulo 05).</p>",
    unsafe_allow_html=True,
)

# Formulario centrado + botón
_, mid, _ = st.columns([1, 5, 1])
with mid:
    obs, pulsado = observacion()

if pulsado:
    # El pipeline contiene todas las transformaciones: solo hay que predecir
    pred_log = regressor.predict(obs)
    pred_anual = np.expm1(pred_log)[0]

    _, res, _ = st.columns([1, 5, 1])
    with res:
        with st.container(border=True):
            st.markdown("**Resultado de la predicción**")
            st.markdown(
                f"<div style='text-align:center; font-size:38px; font-weight:700; "
                f"color:#1fa352;'>S/ {pred_anual:,.2f}</div>",
                unsafe_allow_html=True,
            )
            st.caption("Ingreso neto anual del trabajo principal (ENAHO i524a1).")
            c1, c2 = st.columns(2)
            c1.caption("Equivalente mensual aprox.")
            c2.markdown(
                f"<div style='text-align:right; font-size:18px; font-weight:600;'>"
                f"S/ {pred_anual / 12:,.2f}</div>",
                unsafe_allow_html=True,
            )
