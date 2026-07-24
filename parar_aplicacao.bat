@echo off
title Imobiliaria RM - Encerrar aplicacao
powershell -NoProfile -Command "$processo = Get-NetTCPConnection -LocalPort 8501 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty OwningProcess; if ($processo) { Stop-Process -Id $processo; Write-Host 'Aplicacao encerrada.' } else { Write-Host 'A aplicacao nao esta em execucao.' }"
pause
