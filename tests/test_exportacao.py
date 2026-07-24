import csv
from io import StringIO

from services import CalculoService, ExportService


def test_csv_possui_cabecalho_e_doze_registros_em_centavos():
    orcamento = CalculoService.processar_orcamento(
        "Cliente Teste", False, "Apartamento", 2, 1, 5
    )
    conteudo = ExportService.gerar_csv(orcamento).decode("utf-8-sig")
    linhas = list(csv.DictReader(StringIO(conteudo), delimiter=";"))

    assert len(linhas) == 12
    assert list(linhas[0]) == [
        "numero_mes",
        "aluguel_centavos",
        "contrato_centavos",
        "total_mes_centavos",
    ]
    assert linhas[0] == {
        "numero_mes": "1",
        "aluguel_centavos": "114000",
        "contrato_centavos": "40000",
        "total_mes_centavos": "154000",
    }
    assert linhas[5]["contrato_centavos"] == "0"
