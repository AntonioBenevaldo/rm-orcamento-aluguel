import io

import pandas as pd

from services import ExportService


def test_exportacao_csv_com_doze_registros(calculo_service):
    orcamento = calculo_service.criar_orcamento(
        nome_cliente="Cliente Teste",
        possui_criancas=False,
        tipo_imovel="Apartamento",
        quantidade_quartos=2,
        quantidade_vagas=1,
        parcelas_contrato=5,
    )
    conteudo = ExportService.gerar_csv_bytes(orcamento.parcelas)
    dataframe = pd.read_csv(io.BytesIO(conteudo), sep=";")

    assert list(dataframe.columns) == ExportService.COLUNAS
    assert len(dataframe) == 12
    assert dataframe.loc[0, "total_mes_centavos"] == 154_000
    assert dataframe.loc[11, "total_mes_centavos"] == 114_000
