from collections.abc import Iterable
from io import StringIO

import pandas as pd

from models import ParcelaOrcamento


class ExportService:
    COLUNAS = ["numero_mes", "aluguel_centavos", "contrato_centavos", "total_mes_centavos"]

    @classmethod
    def criar_dataframe(cls, parcelas: Iterable[ParcelaOrcamento | dict]) -> pd.DataFrame:
        registros = []
        for parcela in parcelas:
            if isinstance(parcela, dict):
                registros.append({coluna: int(parcela[coluna]) for coluna in cls.COLUNAS})
            else:
                registros.append(
                    {
                        "numero_mes": parcela.numero_mes,
                        "aluguel_centavos": parcela.aluguel_centavos,
                        "contrato_centavos": parcela.contrato_centavos,
                        "total_mes_centavos": parcela.total_mes_centavos,
                    }
                )
        dataframe = pd.DataFrame(registros, columns=cls.COLUNAS)
        if len(dataframe) != 12:
            raise ValueError("A exportação exige exatamente 12 registros mensais.")
        return dataframe

    @classmethod
    def gerar_csv_bytes(cls, parcelas: Iterable[ParcelaOrcamento | dict]) -> bytes:
        dataframe = cls.criar_dataframe(parcelas)
        buffer = StringIO()
        dataframe.to_csv(buffer, index=False, sep=";", lineterminator="\n")
        return ("﻿" + buffer.getvalue()).encode("utf-8")
