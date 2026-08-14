import pandas as pd
import streamlit as st
from joblib import load
from pathlib import Path

# Cargar el modelo de clasificación (pipeline completo: transformaciones + modelo)
clasificador = load(Path(__file__).parent / "modelos" / "clasificador_informalidad.joblib")

# Opciones de los campos categóricos (valores = los mismos con los que se entrenó)
SEXO = [("Hombre", "1"), ("Mujer", "2")]
PARENTESCO = ["Jefe", "Conyuge", "Hijo", "Otro_familiar"]
NIVEL_EDUC = [
    ("Sin nivel", "1"), ("Inicial", "2"), ("Primaria incompleta", "3"), ("Primaria completa", "4"),
    ("Secundaria incompleta", "5"), ("Secundaria completa", "6"),
    ("Sup. no univ. incompleta", "7"), ("Sup. no univ. completa", "8"),
    ("Sup. univ. incompleta", "9"), ("Sup. univ. completa", "10"),
    ("Maestria/Doctorado", "11"), ("Basica especial", "12"),
]
LENGUA = ["Castellano", "Quechua", "Aimara", "Otra_nativa", "Extranjera_otra"]
DOMINIO = [
    ("Costa Norte", "1"), ("Costa Centro", "2"), ("Costa Sur", "3"), ("Sierra Norte", "4"),
    ("Sierra Centro", "5"), ("Sierra Sur", "6"), ("Selva", "7"), ("Lima Metropolitana", "8"),
]
AREA = [("Urbano", "1"), ("Rural", "0")]
CAMPO = ["Sin_carrera", "Educacion", "Ciencias", "Admin_Contab_Derecho", "Computacion_Informatica",
         "Ingenieria_Tecnicas", "Agropecuaria", "Salud", "Artes_Otras"]

# App
st.title("Modelo de Clasificación: Informalidad Laboral")
st.markdown("##### Probabilidad de que un asalariado tenga empleo informal (ENAHO 2023). 1 = Informal, 0 = Formal.")

st.sidebar.header("Campos a Evaluar")

edad = st.sidebar.number_input("**Edad (14 a 98)**", min_value=14, max_value=98, value=30)
sexo = st.sidebar.selectbox("**Sexo**", [o[0] for o in SEXO])
parentesco = st.sidebar.selectbox("**Parentesco**", PARENTESCO)
nivel = st.sidebar.selectbox("**Nivel educativo**", [o[0] for o in NIVEL_EDUC])
lengua = st.sidebar.selectbox("**Lengua materna**", LENGUA)
dominio = st.sidebar.selectbox("**Dominio geográfico**", [o[0] for o in DOMINIO])
area = st.sidebar.selectbox("**Área**", [o[0] for o in AREA])
campo = st.sidebar.selectbox("**Campo de estudio**", CAMPO)

if st.sidebar.button("Predecir"):
    obs = pd.DataFrame([{
        "edad": int(edad),
        "sexo": dict(SEXO)[sexo],
        "parentesco": parentesco,
        "nivel_educ": dict(NIVEL_EDUC)[nivel],
        "lengua_materna": lengua,
        "dominio": dict(DOMINIO)[dominio],
        "area": dict(AREA)[area],
        "campo_estudio": campo,
    }])

    st.write("**Datos de entrada:**")
    st.write(obs)

    # El pipeline contiene todas las transformaciones: solo hay que predecir
    probs = clasificador.predict_proba(obs)
    pred = clasificador.predict(obs)[0]

    if pred == 1:
        resultado = "INFORMAL"
        color = "orange"
    else:
        resultado = "FORMAL"
        color = "green"
    st.markdown(f'<p style="font-size: 40px; color: {color};">Condición estimada: {resultado}</p>',
                unsafe_allow_html=True)

    st.write("**Probabilidades:**")
    prob_df = pd.DataFrame({
        "Formal": [round(float(probs[0][0]), 4)],
        "Informal": [round(float(probs[0][1]), 4)],
    })
    st.write(prob_df)

if st.sidebar.button("Resetear"):
    st.rerun()
