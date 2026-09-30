if (!(Test-Path ".\main.py")) { & ".\setup_project.ps1" }
if (!(Test-Path ".\.venv")) { python -m venv .venv }
& ".\.venv\Scripts\Activate.ps1"
python -m pip install -r requirements.txt
python main.py
