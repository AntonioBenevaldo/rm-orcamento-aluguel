import pytest

from servicos import OrcamentoService


@pytest.mark.parametrize(
    ("dados", "aluguel", "parcela"),
    [
        ({"nome_cliente": "Ana", "possui_criancas": "nao", "tipo_imovel": "apartamento", "quartos": 2, "garagem": "sim", "parcelas_contrato": 5}, 1140.0, 400.0),
        ({"nome_cliente": "Bruno", "possui_criancas": "sim", "tipo_imovel": "casa", "quartos": 2, "garagem": "sim", "parcelas_contrato": 4}, 1450.0, 500.0),
        ({"nome_cliente": "Carla", "possui_criancas": "nao", "tipo_imovel": "estudio", "estacionamento_estudio": "sim", "vagas_estudio": 4, "parcelas_contrato": 2}, 1570.0, 1000.0),
    ],
)
def test_cenarios_do_trabalho(dados, aluguel, parcela):
    orcamento = OrcamentoService.criar(dados)
    assert orcamento.aluguel_mensal == aluguel
    assert orcamento.contrato.valor_parcela == parcela
    assert len(orcamento.gerar_cronograma_12_meses()) == 12


def test_parcelamento_do_contrato_deve_ser_de_um_a_cinco():
    with pytest.raises(ValueError):
        OrcamentoService.criar({"nome_cliente": "Teste", "tipo_imovel": "casa", "parcelas_contrato": 6})
