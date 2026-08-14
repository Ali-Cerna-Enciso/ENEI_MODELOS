import pandas as pd
import streamlit as st
from joblib import load
from pathlib import Path

from formulario import observacion

# Cargar el modelo de clasificación (pipeline completo: transformaciones + modelo)
clasificador = load(Path(__file__).parent / "modelos" / "clasificador_informalidad.joblib")

st.markdown(
    "<h2 style='text-align:center;'>Modelo de Clasificación: Informalidad Laboral</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; color:#888;'>Probabilidad de que un asalariado tenga "
    "empleo informal (ENAHO 2023). 1 = Informal, 0 = Formal.</p>",
    unsafe_allow_html=True,
)

# Formulario centrado + botón
_, mid, _ = st.columns([1, 5, 1])
with mid:
    obs, pulsado = observacion()

if pulsado:
    # El pipeline contiene todas las transformaciones: solo hay que predecir
    probs = clasificador.predict_proba(obs)
    pred = clasificador.predict(obs)[0]
    prob_formal = float(probs[0][0])
    prob_informal = float(probs[0][1])

    etiqueta = "INFORMAL" if pred == 1 else "FORMAL"
    color = "#f04e2e" if pred == 1 else "#1fa352"

    _, res, _ = st.columns([1, 5, 1])
    with res:
        with st.container(border=True):
            st.markdown("**Resultado de la predicción**")
            st.markdown(
                f"<div style='text-align:center; font-size:38px; font-weight:700; "
                f"color:{color};'>{etiqueta}</div>",
                unsafe_allow_html=True,
            )
            m1, m2 = st.columns(2)
            m1.metric("Probabilidad Formal", f"{prob_formal:.1%}")
            m2.metric("Probabilidad Informal", f"{prob_informal:.1%}")
            st.progress(prob_informal)
            st.caption("Barra: probabilidad de que el empleo sea informal.")
