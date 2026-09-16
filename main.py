"""Main entry point for the SDSS genetic algorithms pipeline."""

from __future__ import annotations

import json
from pathlib import Path

from src.config import FEATURE_COLUMNS, RANDOM_STATE
from src.data_loader import load_dataset, summarize_dataset
from src.feature_selection.ga import run_feature_selection_ga
from src.hyperparameters.ga import run_hyperparameter_ga
from src.clustering.ga import run_clustering_ga


def print_banner() -> None:
    """Print a banner for the genetic algorithms project."""
    print("=" * 49)
    print("ALGORITMOS GENÉTICOS - SDSS")
    print("=" * 49)


def main() -> None:
    """Run the dataset validation, feature selection, hyperparameter tuning, and clustering pipeline."""
    print_banner()

    dataset_path = Path(__file__).resolve().parent / "data" / "sdss_sample.csv"
    print("[1/3] Validación del dataset")
    df = load_dataset(dataset_path)
    summary = summarize_dataset(df)
    print(f"Rows: {summary['rows']}, Columns: {summary['columns']}")
    print(f"Classes: {summary['class_counts']}")

    print("\n[2/3] Selección de características")
    feature_metrics = run_feature_selection_ga(df, output_dir="outputs/feature_selection")
    print(f"Mejores variables: {feature_metrics['best_features']}")
    print(f"Accuracy: {feature_metrics['accuracy']:.4f}")

    print("\n[3/3] Optimización de hiperparámetros")
    hp_metrics = run_hyperparameter_ga(df, output_dir="outputs/hyperparameters")
    print(f"Mejor alpha: {hp_metrics['best_alpha']:.6f}")
    print(f"MSE: {hp_metrics['mse']:.6f}")
    print(f"R²: {hp_metrics['r2']:.6f}")

    print("\n[4/4] Clustering evolutivo")
    cluster_metrics = run_clustering_ga(df, output_dir="outputs/clustering")
    print(f"SSE AG: {cluster_metrics['genetic_sse']:.6f}")
    print(f"SSE KMeans: {cluster_metrics['kmeans_sse']:.6f}")

    summary_payload = {
        "feature_selection": feature_metrics,
        "hyperparameters": hp_metrics,
        "clustering": cluster_metrics,
    }
    Path("outputs").mkdir(exist_ok=True)
    (Path("outputs") / "summary.json").write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    print("\nProceso finalizado.")
    print("Resultados guardados en outputs/")


if __name__ == "__main__":
    main()
