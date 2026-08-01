@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo O ambiente virtual ainda nao existe.
    echo Execute primeiro o arquivo INSTALAR.bat.
    pause
    exit /b 1
)

call ".venv\Scripts\activate.bat"
python -m streamlit run app.py

if errorlevel 1 (
    echo.
    echo A aplicacao foi encerrada com erro.
    pause
)
