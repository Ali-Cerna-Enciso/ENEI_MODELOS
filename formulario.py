# Formulario compartido por ambas apps: los 8 campos sociodemográficos
# en una tarjeta centrada (mismos valores con los que se entrenaron los modelos).

import pandas as pd
import streamlit as st

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


def render_formulario():
    """Dibuja la tarjeta con los 8 campos en grilla de 3 columnas.

    Devuelve un dict con los valores listos para el DataFrame de predicción.
    """
    with st.container(border=True):
        st.markdown("**Datos de la persona**")
        c1, c2, c3 = st.columns(3)
        edad = c1.number_input("Edad (14 a 98)", min_value=14, max_value=98, value=30)
        sexo = c2.selectbox("Sexo", [o[0] for o in SEXO])
        parentesco = c3.selectbox("Parentesco", PARENTESCO)
        c4, c5, c6 = st.columns(3)
        nivel = c4.selectbox("Nivel educativo", [o[0] for o in NIVEL_EDUC])
        lengua = c5.selectbox("Lengua materna", LENGUA)
        dominio = c6.selectbox("Dominio geográfico", [o[0] for o in DOMINIO])
        c7, c8, _ = st.columns(3)
        area = c7.selectbox("Área", [o[0] for o in AREA])
        campo = c8.selectbox("Campo de estudio", CAMPO)
    return {
        "edad": int(edad),
        "sexo": dict(SEXO)[sexo],
        "parentesco": parentesco,
        "nivel_educ": dict(NIVEL_EDUC)[nivel],
        "lengua_materna": lengua,
        "dominio": dict(DOMINIO)[dominio],
        "area": dict(AREA)[area],
        "campo_estudio": campo,
    }


def observacion():
    """Formulario + botón Predecir centrado.

    Devuelve (obs: DataFrame | None, pulsado: bool).
    """
    valores = render_formulario()
    _, bcol, _ = st.columns([1, 2, 1])
    with bcol:
        pulsado = st.button("Predecir", type="primary", width="stretch")
    if pulsado:
        return pd.DataFrame([valores]), True
    return None, False
