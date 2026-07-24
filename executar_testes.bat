@echo off
cd /d "%~dp0"
title Imobiliaria RM - Testes
echo.
echo ==========================================
echo  TESTES DO ORCAMENTO IMOBILIARIO R.M
echo ==========================================
echo.
python -m pytest -v
echo.
pause
