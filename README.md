# ACO + SSA + RBF + MongoDB

Proyecto academico de biooptimizacion integrado con MongoDB.

## Despliegue de la capa de datos en MongoDB local

MongoDB almacena las corridas; el codigo Python se ejecuta como aplicacion cliente.

1. Instala dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

2. Verifica MongoDB:

```powershell
Get-Service MongoDB
Start-Service MongoDB
mongosh "mongodb://localhost:27017"
```

3. Inicializa la base y los indices:

```powershell
python scripts/init_mongodb.py --seed-sample
```

Se usa:
- URI: `mongodb://localhost:27017`
- Base: `biooptimization`
- Coleccion: `runs`

4. Ejecuta una prueba real:

```powershell
python scripts/run_rbf_experiments.py --quick
```

5. Ejecuta las 10 semillas:

```powershell
python scripts/run_rbf_experiments.py
```

## Verificacion en mongosh

```javascript
use biooptimization
show collections
db.runs.find().sort({created_at: -1}).limit(5)
db.runs.countDocuments()
db.runs.find({algorithm: "ssa_rbf"}).sort({"metrics.rmse": 1}).limit(1)
```

La rama incluye el inicializador `scripts/init_mongodb.py` y una capa Mongo con indices para algoritmo/fecha, experimento/semilla/algoritmo y RMSE.
