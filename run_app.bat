@echo off
cd /d %~dp0

REM Fuerza el directorio raíz del proyecto como PYTHONPATH
set PYTHONPATH=%CD%

call venv\Scripts\activate
python -m app.main
pause
