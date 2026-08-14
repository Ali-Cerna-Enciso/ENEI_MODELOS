# ENAHO 2023 — Modelos de Regresión y Clasificación

Proyecto del curso "ML en producción" (ENEI/INEI): dos modelos sobre la ENAHO 2023 a nivel de persona (asalariados, 25 232 filas):

- **Regresión:** ingreso anual del trabajo principal (`y_reg = log1p(i524a1)`).
- **Clasificación:** informalidad laboral (`y_clasif`: 1 informal / 0 formal).

Ambos usan los mismos 8 predictores sociodemográficos: edad, sexo, parentesco, nivel educativo, lengua materna, dominio, área y campo de estudio. Sin variables de empleo/ingreso (leakage).

## Cómo funciona (flujo simple)

```
notebooks/  →  entrenan el modelo en Colab  →  descargan .joblib
modelos/    →  se colocan los .joblib descargados
apps (raíz) →  cargan el .joblib y predicen con el formulario
```

## Métricas alcanzadas (test, 20% de 25 232; reproducibles con `omp_test/metricas_2026-08-14/metricas.py`)

**Regresión — ingreso anual (Gradient Boosting, ganador por MAPE):**

| Métrica | Train | Test |
|---|---|---|
| R² (log) | 0.4805 | 0.4783 |
| RMSE (log) | 0.6411 | 0.6487 |
| MAE (log) | 0.4693 | 0.4749 |
| RMSE (soles/año) | S/ 12 748.56 | S/ 12 951.42 |
| MAPE (soles) | 67.6 % | 68.9 % |

**Clasificación — informalidad (XGBoost, ganador por AUC):**

| Métrica | Train | Test |
|---|---|---|
| Accuracy | 0.7683 | 0.7597 |
| ROC-AUC | 0.8439 | 0.8373 |

Confusión (test): Formal → 1 327 bien / 720 mal; Informal → 2 507 bien / 493 mal.
Por clase (test): Formal precision 0.73 / recall 0.65; Informal precision 0.78 / recall 0.84; macro-F1 0.75.

1. **Entrenar (Colab):** abre `notebooks/01_regresion_ingreso.ipynb` o `notebooks/02_clasificacion_informalidad.ipynb`, monta la carpeta compartida `CODIGOS_ENAPRES/BASE_ENAHO/2023` y ejecuta todo. Al final descarga el modelo (`regresor_ingreso.joblib` / `clasificador_informalidad.joblib`).
2. **Colocar el modelo:** pega el `.joblib` en la carpeta `modelos/` (mismo nombre).
3. **Ver la app (local):**
   ```
   python -m venv venv
   .\venv\Scripts\activate          # Windows
   pip install -r requirements.txt
   streamlit run streamlit_app.py   # entrada única (elige modelo en el sidebar)
   ```
4. **Desplegar en Streamlit Cloud (web):**
   - Sube este repo a GitHub (privado o público).
   - En [share.streamlit.io](https://share.streamlit.io) → **Create app** → pega la URL del repo.
   - Repo: `tu-usuario/ENEI_MODELOS` · Branch: `master` · **Main file path: `streamlit_app.py`**.
   - **Advanced settings → Python version: 3.12** (requerido por `xgboost==3.4.0`; con 3.11 falla la instalación).
   - **Deploy** → primera vez autoriza la GitHub App de Streamlit para acceder al repo privado.
   - URL pública: `https://tu-usuario-enei-modelos.streamlit.app`.

## Carpetas

| Carpeta | Qué es |
|---|---|
| `notebooks/` | Los 2 Jupyter (uno por modelo): carga de datos, descriptiva, pre-comprobaciones, entrenamiento, métricas y guardado del modelo |
| `modelos/` | Modelos entrenados `.joblib` (los descargados de Colab) |
| `app_regresion.py` / `app_clasificacion.py` | Las 2 apps Streamlit (una por modelo) |
| `streamlit_app.py` | Entrada única para Streamlit Cloud: elige modelo en el sidebar |
| `requirements.txt` | Librerías con versión fija |
| `data/raw/2023/` | Base ENAHO 2023 en `.sav` (mod02, mod03, mod05) — la misma que está en la carpeta compartida de Drive |

## Notas

- Los notebooks son **autocontenidos**: reproducen todo el pipeline (merge → filtros → derivaciones → modelo) desde los `.sav`.
- Los modelos en `modelos/` son **pipelines completos** (transformaciones + modelo): la app solo hace `load()` y `predict()` con los 8 campos en crudo.
- **Versiones:** los modelos se entrenan en Colab con `scikit-learn 1.6.1`; el `requirements.txt` usa la misma versión para que la app cargue los `.joblib` sin errores. No cambiar la versión de sklearn.
- La app se ejecuta con `streamlit run app_*.py` (no con `python`).
