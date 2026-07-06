"""Exportação do orçamento para arquivo CSV."""

from __future__ import annotations

import csv
from pathlib import Path

from orcamento import Orcamento


class ExportadorCSV:
    """Responsável por salvar as 12 parcelas do orçamento em CSV."""

    CABECALHO = ["mes", "aluguel_mensal", "parcela_contrato", "total_mes"]

    @staticmethod
    def salvar(orcamento: Orcamento, caminho: str | Path) -> Path:
        caminho = Path(caminho)
        caminho.parent.mkdir(parents=True, exist_ok=True)

        with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo_csv:
            escritor = csv.DictWriter(arquivo_csv, fieldnames=ExportadorCSV.CABECALHO, delimiter=";")
            escritor.writeheader()
            for linha in orcamento.gerar_cronograma_12_meses():
                escritor.writerow(
                    {
                        "mes": linha["mes"],
                        "aluguel_mensal": f"{linha['aluguel_mensal']:.2f}".replace(".", ","),
                        "parcela_contrato": f"{linha['parcela_contrato']:.2f}".replace(".", ","),
                        "total_mes": f"{linha['total_mes']:.2f}".replace(".", ","),
                    }
                )
        return caminho
