# ACO + SSA + RBF + MongoDB

Proyecto académico construido y validado para la actividad de optimización bioinspirada.

## Contenido
- ACO para TSP.
- SSA para Rastrigin.
- RBF base.
- SSA-RBF para optimizar M, sigma y lambda.
- MongoDB para registrar corridas.
- 10 semillas configuradas para el experimento principal.
- 5 pruebas automáticas.
- Notebook de análisis.
- docker-compose para MongoDB.

El archivo `biooptimization_project.zip` contiene el proyecto completo validado.

Validación realizada:
- 5/5 pruebas aprobadas.
- ACO ejecuta correctamente.
- SSA ejecuta correctamente.
- RBF vs SSA-RBF ejecuta correctamente en modo rápido.

MongoDB esperado:
`mongodb://localhost:27017`
Base: `biooptimization`
Colección: `runs`
