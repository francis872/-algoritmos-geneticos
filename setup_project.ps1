Write-Host "Preparando BioOptimization Lab..." -ForegroundColor Cyan
if (!(Test-Path ".\biooptimization_project.zip")) { throw "No se encontro biooptimization_project.zip" }
Expand-Archive ".\biooptimization_project.zip" -DestinationPath "." -Force
if (!(Test-Path ".\.env") -and (Test-Path ".\.env.example")) { Copy-Item ".\.env.example" ".\.env" }
Write-Host "Proyecto actualizado en la carpeta actual." -ForegroundColor Green
Write-Host "Siguiente paso: python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; python main.py"
