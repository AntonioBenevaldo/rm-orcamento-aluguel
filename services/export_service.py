import pandas as pd

from models import Orcamento
from utils import moeda_br


class ExportService:
    @staticmethod
    def criar_dataframe(orcamento: Orcamento) -> pd.DataFrame:
        """Cria a tabela exibida na interface, formatada em reais."""
        linhas = [
            {
                "Mês": linha["numero_mes"],
                "Aluguel": moeda_br(linha["aluguel_centavos"]),
                "Parcela do contrato": moeda_br(linha["contrato_centavos"]),
                "Total do mês": moeda_br(linha["total_mes_centavos"]),
            }
            for linha in orcamento.cronograma()
        ]
        return pd.DataFrame(linhas)

    @classmethod
    def gerar_csv(cls, orcamento: Orcamento) -> bytes:
        """Exporta os valores exatos em centavos, sem recalcular o orçamento."""
        dataframe = pd.DataFrame(orcamento.cronograma())
        texto = dataframe.to_csv(index=False, sep=";", encoding="utf-8")
        return texto.encode("utf-8-sig")

    @staticmethod
    def gerar_csv_registros(registros: list[dict]) -> bytes:
        texto = pd.DataFrame(registros).to_csv(index=False, sep=";", encoding="utf-8")
        return texto.encode("utf-8-sig")
