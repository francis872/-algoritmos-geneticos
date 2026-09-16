# Algoritmos Genéticos para SDSS

## Introducción

Este proyecto implementa un pipeline completo basado en algoritmos genéticos para resolver tres problemas de optimización sobre el dataset astronómico SDSS:

1. Selección de características para clasificar objetos astronómicos.
2. Optimización del hiperparámetro alpha de una regresión Ridge.
3. Clustering evolutivo con centroides dinámicos.

La solución está organizada en módulos, reutiliza utilidades de preprocessing y genera artefactos reales en la carpeta `outputs/`.

## Dataset

El archivo principal es `data/sdss_sample.csv` y contiene variables astronómicas como:

- `u`
- `g`
- `r`
- `i`
- `z`
- `redshift`
- `class`

Además, pueden existir otras columnas auxiliares como `snr_r` y `extinction_r`, pero los ejercicios principales usan exactamente las variables especificadas en la consigna.

## Problemas de optimización

### 1. Feature Selection

Se busca seleccionar el mejor subconjunto de características entre `u`, `g`, `r`, `i`, `z` y `redshift` para predecir la clase `class` con un `KNeighborsClassifier` con `n_neighbors=5`.

### 2. Hyperparameter Optimization

Se optimiza `alpha` para la regresión `Ridge`, usando `u, g, r, i, z` como variables predictoras y `redshift` como salida. La función objetivo es:

`fitness = 1 / (MSE + epsilon)`

con `epsilon = 1e-8`.

### 3. Evolutionary Clustering

Se busca ubicar 3 centroides sobre `u, g, r, i, z` minimizando la suma de errores cuadráticos intra-cluster (SSE):

`fitness = 1 / (SSE + epsilon)`

La salida se compara frente a un modelo `KMeans(n_clusters=3, random_state=42)`.

## Qué es un cromosoma en cada problema

### Feature selection

Un cromosoma es un vector binario de longitud 6, de la forma:

`[1, 0, 1, 1, 0, 1]`

Cada posición representa `u, g, r, i, z, redshift` y un 1 activa una variable.

### Hyperparameters

Un cromosoma es un vector real con un solo gen:

`[alpha]`

El valor se mantiene en el rango `[1e-4, 100.0]`.

### Clustering

Un cromosoma contiene 15 genes reales, representando 3 centroides con 5 coordenadas cada uno:

`[c1_u, c1_g, c1_r, c1_i, c1_z, c2_u, ..., c3_z]`

## Fitness

### Feature Selection

`fitness = accuracy`

### Hyperparameters

`fitness = 1 / (MSE + epsilon)`

### Clustering

`fitness = 1 / (SSE + epsilon)`

## Operadores genéticos

Los tres algoritmos implementan operadores manuales sin bibliotecas automáticas:

- Selección por torneo.
- Cruce de un punto para individuos binarios.
- Cruce aritmético para individuos reales.
- Mutación bit-flip para genes binarios.
- Mutación gaussiana para genes reales.
- Elitismo para conservar los mejores individuos.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Tests

```bash
pytest -v
```

## Docker

> Requisito: Docker Desktop debe estar ejecutándose en Windows antes de construir o ejecutar el contenedor.

Construcción:

```bash
docker build -t sdss-ga .
```

Ejecución local:

```bash
docker run --rm sdss-ga
```

Persistir los resultados generados en `outputs/` en el host:

```bash
docker run --rm -v "${PWD}/outputs:/app/outputs" sdss-ga
```

En PowerShell:

```powershell
docker run --rm -v "${PWD}/outputs:/app/outputs" sdss-ga
```

Comando exacto recomendado para este proyecto:

```powershell
cd "c:\Users\Usuario\OneDrive\Escritorio\algorimos geneticos\algoritmos-geneticos-sdss"
docker build -t sdss-ga .
docker run --rm -v "${PWD}\outputs:/app/outputs" sdss-ga
```

Este flujo genera los artefactos del proyecto en la carpeta `outputs/` del equipo local, manteniendo la ejecución reproducible y lista para entregar como actividad universitaria.

## Jenkins

El `Jenkinsfile` incluye las etapas:

- Checkout
- Install Dependencies
- Tests
- Run Genetic Algorithms
- Archive Artifacts

## Outputs

Los archivos generados incluyen:

- `outputs/feature_selection/metrics.json`
- `outputs/feature_selection/convergence.csv`
- `outputs/feature_selection/convergence.png`
- `outputs/feature_selection/confusion_matrix.png`
- `outputs/hyperparameters/metrics.json`
- `outputs/hyperparameters/convergence.csv`
- `outputs/hyperparameters/convergence.png`
- `outputs/clustering/metrics.json`
- `outputs/clustering/convergence.csv`
- `outputs/clustering/genetic_clusters.png`
- `outputs/clustering/kmeans_clusters.png`
- `outputs/clustering/real_classes.png`
- `outputs/summary.json`

## Reproducibilidad

El proyecto usa una semilla global `RANDOM_STATE = 42` para garantizar resultados reproduibles en numpy, Python y modelos de scikit-learn.

---

## Estructura del proyecto

```text
algoritmos-geneticos-sdss/
├── data/
├── src/
├── tests/
├── outputs/
├── main.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── README.md
├── .gitignore
├── .dockerignore
└── .venv/
```
