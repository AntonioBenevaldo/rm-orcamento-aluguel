from io import BytesIO

import pandas as pd

from models import Orcamento


class ExportService:
    @staticmethod
    def criar_dataframe(orcamento: Orcamento) -> pd.DataFrame:
        return pd.DataFrame(orcamento.cronograma()).rename(columns={"mes": "Mês", "aluguel": "Aluguel", "contrato": "Parcela do contrato", "total": "Total do mês"})

    @classmethod
    def gerar_csv(cls, orcamento: Orcamento) -> bytes:
        return cls.criar_dataframe(orcamento).to_csv(index=False, sep=";", decimal=",", encoding="utf-8-sig").encode("utf-8-sig")

    @staticmethod
    def gerar_csv_registros(registros: list[dict]) -> bytes:
        return pd.DataFrame(registros).to_csv(index=False, sep=";", decimal=",", encoding="utf-8-sig").encode("utf-8-sig")
