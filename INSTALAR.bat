@echo off
setlocal
cd /d "%~dp0"

echo ================================================
echo Instalacao - Sistema de Orcamento Imobiliario R.M
echo ================================================

where py >nul 2>&1
if %errorlevel%==0 (
    py -m venv .venv
) else (
    python -m venv .venv
)

if not exist ".venv\Scripts\python.exe" (
    echo ERRO: nao foi possivel criar o ambiente virtual.
    pause
    exit /b 1
)

call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 goto :erro
python -m pip install -r requirements.txt
if errorlevel 1 goto :erro

echo.
echo Instalacao concluida com sucesso.
echo Execute INICIAR_SISTEMA.bat para abrir a aplicacao.
pause
exit /b 0

:erro
echo.
echo ERRO: a instalacao nao foi concluida.
echo Verifique sua conexao com a internet e a instalacao do Python.
pause
exit /b 1
