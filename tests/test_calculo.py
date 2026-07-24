import pytest

from models import Apartamento, Casa, Cliente, Contrato, Estudio
from services import CalculoService


@pytest.mark.parametrize(
    ("tipo", "possui_criancas", "quartos", "vagas", "parcelas", "esperado"),
    [
        ("Apartamento", False, 2, 1, 5, 114_000),
        ("Casa", True, 2, 1, 4, 145_000),
        ("Estúdio", False, 1, 4, 2, 157_000),
    ],
)
def test_cenarios_oficiais_em_centavos(
    tipo, possui_criancas, quartos, vagas, parcelas, esperado
):
    orcamento = CalculoService.processar_orcamento(
        "Cliente Teste",
        possui_criancas,
        tipo,
        quartos,
        vagas,
        parcelas,
    )
    assert orcamento.aluguel_mensal_centavos == esperado
    assert orcamento.total_primeiro_ano_centavos == esperado * 12 + 200_000


def test_desconto_aplica_somente_ao_apartamento_sem_criancas():
    sem_criancas = Cliente("Ana Teste", False)
    com_criancas = Cliente("Bruno Teste", True)
    apartamento = Apartamento(quartos=1, vagas=0)
    casa = Casa(quartos=1, vagas=0)

    assert apartamento.calcular_aluguel_centavos(sem_criancas) == 66_500
    assert apartamento.calcular_aluguel_centavos(com_criancas) == 70_000
    assert casa.calcular_aluguel_centavos(sem_criancas) == 90_000


def test_estudio_rejeita_uma_vaga():
    with pytest.raises(ValueError, match="zero vagas ou, no mínimo, duas"):
        Estudio(vagas=1)


@pytest.mark.parametrize("parcelas", [0, 6])
def test_contrato_rejeita_parcelamento_fora_do_limite(parcelas):
    with pytest.raises(ValueError, match="entre uma e cinco"):
        Contrato(parcelas)


def test_contrato_distribui_restos_de_centavos_sem_perder_valor():
    contrato = Contrato(3)
    assert contrato.parcelas_centavos == (66_667, 66_667, 66_666)
    assert sum(contrato.parcelas_centavos) == 200_000


def test_cronograma_tem_doze_meses_e_contrato_exato():
    orcamento = CalculoService.processar_orcamento(
        "Cliente Teste", True, "Casa", 1, 0, 3
    )
    cronograma = orcamento.cronograma()

    assert len(cronograma) == 12
    assert [linha["numero_mes"] for linha in cronograma] == list(range(1, 13))
    assert sum(linha["contrato_centavos"] for linha in cronograma) == 200_000
    assert all(linha["contrato_centavos"] == 0 for linha in cronograma[3:])
    assert sum(linha["total_mes_centavos"] for linha in cronograma) == (
        orcamento.total_primeiro_ano_centavos
    )
