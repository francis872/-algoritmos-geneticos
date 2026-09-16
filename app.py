from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd
import streamlit as st

from src.config import FEATURE_COLUMNS, GENERATIONS, MUTATION_RATE, POPULATION_SIZE, TARGET_COLUMN
from src.data_loader import load_dataset, summarize_dataset
from src.feature_selection.ga import run_feature_selection_ga
from src.hyperparameters.ga import run_hyperparameter_ga
from src.clustering.ga import run_clustering_ga


DATASET_PATH = Path(__file__).resolve().parent / "data" / "sdss_sample.csv"
OUTPUTS_DIR = Path(__file__).resolve().parent / "outputs"


@st.cache_data
def load_data() -> pd.DataFrame:
    return load_dataset(DATASET_PATH)


@st.cache_data
def get_summary(df: pd.DataFrame) -> dict:
    return summarize_dataset(df)


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def render_image_if_exists(path: Path, caption: str) -> None:
    if path.exists():
        st.image(str(path), caption=caption, width="stretch")


def render_generation_animation(history_path: Path, metric_name: str, title: str) -> None:
    if not history_path.exists():
        return

    history = pd.read_csv(history_path)
    if history.empty:
        return

    max_generation = int(history["generation"].max())
    selected_generation = st.slider(
        f"Generación para {title}",
        min_value=1,
        max_value=max_generation,
        value=max_generation,
        step=1,
        key=f"slider_{metric_name}",
    )

    current_history = history.iloc[:selected_generation]
    chart_slot = st.empty()
    chart_slot.line_chart(current_history[["best_fitness", "average_fitness"]], use_container_width=True)
    st.progress(selected_generation / max_generation)
    st.caption(f"Generación {selected_generation}/{max_generation}: mejor fitness = {current_history['best_fitness'].iloc[-1]:.4f}")

    if st.button(f"Reproducir evolución {title}", key=f"animate_{metric_name}"):
        animation_slot = st.empty()
        for step in range(1, max_generation + 1):
            partial = history.iloc[:step]
            animation_slot.line_chart(partial[["best_fitness", "average_fitness"]], use_container_width=True)
            animation_slot.progress(step / max_generation)
            animation_slot.caption(f"Evolución {step}/{max_generation}")
            time.sleep(0.18)


st.set_page_config(page_title="GA SDSS Dashboard", page_icon="🚀", layout="wide")

if "run_pipeline" not in st.session_state:
    st.session_state.run_pipeline = False

if "feature_metrics" not in st.session_state:
    st.session_state.feature_metrics = {}
if "hp_metrics" not in st.session_state:
    st.session_state.hp_metrics = {}
if "cluster_metrics" not in st.session_state:
    st.session_state.cluster_metrics = {}


def execute_pipeline(df: pd.DataFrame):
    population_size = st.session_state.get("population_size", POPULATION_SIZE)
    mutation_rate = st.session_state.get("mutation_rate", MUTATION_RATE)
    generations = st.session_state.get("generations", GENERATIONS)

    with st.spinner("Ejecutando algoritmo de selección de características..."):
        st.session_state.feature_metrics = run_feature_selection_ga(
            df,
            output_dir=OUTPUTS_DIR / "feature_selection",
            population_size=population_size,
            mutation_rate=mutation_rate,
            generations=generations,
        )
    st.success("Selección de características finalizada.")

    with st.spinner("Ejecutando optimización de hiperparámetros..."):
        st.session_state.hp_metrics = run_hyperparameter_ga(
            df,
            output_dir=OUTPUTS_DIR / "hyperparameters",
            population_size=population_size,
            mutation_rate=mutation_rate,
            generations=generations,
        )
    st.success("Optimización de hiperparámetros finalizada.")

    with st.spinner("Ejecutando clustering evolutivo..."):
        st.session_state.cluster_metrics = run_clustering_ga(
            df,
            output_dir=OUTPUTS_DIR / "clustering",
            population_size=population_size,
            mutation_rate=mutation_rate,
            generations=generations,
        )
    st.success("Clustering evolutivo finalizado.")

    st.session_state.run_pipeline = False


st.title("Algoritmos Genéticos para datos astronómicos SDSS")
st.caption("Visualiza la evolución y los resultados de cada algoritmo genético.")

with st.sidebar:
    st.header("Proyecto")
    st.write("Dataset: SDSS sample")
    st.write("Ruta: data/sdss_sample.csv")
    st.markdown("---")
    st.write("Este dashboard ejecuta los tres algoritmos desarrollados: selección de rasgos, ajuste de hiperparámetros y clustering evolutivo.")

    st.subheader("Parámetros del experimento")
    population_size = st.slider("Tamaño de población", 10, 120, POPULATION_SIZE, 5)
    mutation_rate = st.slider("Tasa de mutación", 0.01, 0.4, MUTATION_RATE, 0.01)
    generations = st.slider("Número de generaciones", 10, 150, GENERATIONS, 10)

    st.markdown("---")
    if st.button("Ejecutar pipeline completo", type="primary", key="run_full_pipeline"):
        st.session_state.run_pipeline = True
        st.session_state.population_size = population_size
        st.session_state.mutation_rate = mutation_rate
        st.session_state.generations = generations


df = load_data()
summary = get_summary(df)

col1, col2, col3 = st.columns(3)
col1.metric("Filas", summary["rows"])
col2.metric("Columnas", summary["columns"])
col3.metric("Clases", len(summary["class_counts"]))

st.subheader("Distribución de clases")
st.dataframe(pd.DataFrame(summary["class_counts"].items(), columns=["Clase", "Cantidad"]))

with st.expander("Variables disponibles"):
    st.write(FEATURE_COLUMNS)

if st.session_state.run_pipeline:
    execute_pipeline(df)
else:
    st.session_state.feature_metrics = load_json(OUTPUTS_DIR / "feature_selection" / "metrics.json")
    st.session_state.hp_metrics = load_json(OUTPUTS_DIR / "hyperparameters" / "metrics.json")
    st.session_state.cluster_metrics = load_json(OUTPUTS_DIR / "clustering" / "metrics.json")

feature_metrics = st.session_state.feature_metrics
hp_metrics = st.session_state.hp_metrics
cluster_metrics = st.session_state.cluster_metrics

st.markdown("---")

feature_tab, hyper_tab, cluster_tab, explain_tab = st.tabs(["Selección", "Hiperparámetros", "Clustering", "Vista explicada"])

with explain_tab:
    st.subheader("Qué está haciendo cada algoritmo")
    st.markdown(
        """
        ### 1) Selección de características
        Un cromosoma binario decide qué variables del conjunto SDSS se usan para clasificar estrellas, galaxias o cuásares. Cada generación mantiene los mejores cromosomas, combina individuos y aplica mutación para mejorar la precisión y reducir dimensionalidad.

        ### 2) Optimización de hiperparámetros
        Aquí se busca el mejor valor del parámetro alpha de una regresión Ridge. Cada individuo representa un valor posible y el algoritmo evoluciona hacia el que minimiza el error y maximiza el coeficiente de determinación.

        ### 3) Clustering evolutivo
        Los centroides se mueven a lo largo de generaciones para agrupar datos similares. Se compara con K-Means para ver si la búsqueda evolutiva encuentra particiones competitivas sin depender solo de una inicialización puntual.
        """
    )
    st.info("La idea principal es que la evolución artificial imita la selección natural: mejoran los individuos con mejor fitness, se combinan, y se exploran soluciones nuevas para encontrar una aproximación útil al problema.")

with feature_tab:
    if feature_metrics:
        st.subheader("Resultados de selección de características")
        st.metric("Precisión", round(float(feature_metrics.get("accuracy", 0.0)), 4))
        st.write("Mejores variables:", feature_metrics.get("best_features", []))
        render_generation_animation(OUTPUTS_DIR / "feature_selection" / "convergence.csv", "feature", "Selección de características")
        render_image_if_exists(OUTPUTS_DIR / "feature_selection" / "convergence.png", "Convergencia del GA")
        render_image_if_exists(OUTPUTS_DIR / "feature_selection" / "confusion_matrix.png", "Matriz de confusión")
    else:
        st.info("Todavía no hay resultados. Pulsa 'Ejecutar pipeline completo'.")

with hyper_tab:
    if hp_metrics:
        st.subheader("Optimización de alpha")
        col1, col2, col3 = st.columns(3)
        col1.metric("Mejor alpha", round(float(hp_metrics.get("best_alpha", 0.0)), 6))
        col2.metric("MSE", round(float(hp_metrics.get("mse", 0.0)), 6))
        col3.metric("R²", round(float(hp_metrics.get("r2", 0.0)), 6))
        render_generation_animation(OUTPUTS_DIR / "hyperparameters" / "convergence.csv", "hyper", "Optimización de hiperparámetros")
        render_image_if_exists(OUTPUTS_DIR / "hyperparameters" / "convergence.png", "Convergencia de hiperparámetros")
    else:
        st.info("Todavía no hay resultados. Pulsa 'Ejecutar pipeline completo'.")

with cluster_tab:
    if cluster_metrics:
        st.subheader("Comparación de clustering")
        col1, col2 = st.columns(2)
        col1.metric("SSE GA", round(float(cluster_metrics.get("genetic_sse", 0.0)), 6))
        col2.metric("SSE KMeans", round(float(cluster_metrics.get("kmeans_sse", 0.0)), 6))
        render_generation_animation(OUTPUTS_DIR / "clustering" / "convergence.csv", "cluster", "Clustering evolutivo")
        render_image_if_exists(OUTPUTS_DIR / "clustering" / "genetic_clusters.png", "Clustering evolutivo")
        render_image_if_exists(OUTPUTS_DIR / "clustering" / "kmeans_clusters.png", "KMeans")
        render_image_if_exists(OUTPUTS_DIR / "clustering" / "real_classes.png", "Clases reales")
    else:
        st.info("Todavía no hay resultados. Pulsa 'Ejecutar pipeline completo'.")

st.markdown("---")
st.subheader("Resumen del pipeline")
if feature_metrics or hp_metrics or cluster_metrics:
    summary_payload = {
        "feature_selection": feature_metrics,
        "hyperparameters": hp_metrics,
        "clustering": cluster_metrics,
    }
    st.json(summary_payload)
else:
    st.info("Ejecuta el pipeline para obtener métricas finales.")
