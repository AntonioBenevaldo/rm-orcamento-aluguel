@echo off
cd /d "%~dp0"
title Imobiliaria RM - Aplicacao
echo.
echo ==========================================
echo  SISTEMA DE ORCAMENTO IMOBILIARIO R.M
echo ==========================================
echo.
echo Iniciando a aplicacao...
echo Quando terminar, pressione Ctrl+C.
echo.
python -m streamlit run app.py
pause
