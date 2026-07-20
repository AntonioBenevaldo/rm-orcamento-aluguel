"""Exportação do cronograma de cobrança para CSV."""

import csv
from pathlib import Path

from modelos import Orcamento


def exportar_csv(orcamento: Orcamento, caminho: str | Path) -> Path:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["mes", "aluguel_mensal", "parcela_contrato", "total_mes"], delimiter=";")
        escritor.writeheader()
        for linha in orcamento.gerar_cronograma_12_meses():
            escritor.writerow({chave: str(valor).replace(".", ",") if chave != "mes" else valor for chave, valor in linha.items()})
    return destino
