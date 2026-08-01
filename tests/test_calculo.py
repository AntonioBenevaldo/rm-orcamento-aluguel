import pytest


def test_apartamento_completo_sem_criancas(calculo_service):
    orcamento = calculo_service.criar_orcamento(
        nome_cliente="Cliente Teste",
        possui_criancas=False,
        tipo_imovel="Apartamento",
        quantidade_quartos=2,
        quantidade_vagas=1,
        parcelas_contrato=5,
    )
    assert orcamento.aluguel_mensal_centavos == 114_000


def test_casa_com_dois_quartos_e_garagem(calculo_service):
    orcamento = calculo_service.criar_orcamento(
        nome_cliente="Cliente Teste",
        possui_criancas=False,
        tipo_imovel="Casa",
        quantidade_quartos=2,
        quantidade_vagas=1,
        parcelas_contrato=5,
    )
    assert orcamento.aluguel_mensal_centavos == 145_000


def test_estudio_com_quatro_vagas(calculo_service):
    orcamento = calculo_service.criar_orcamento(
        nome_cliente="Cliente Teste",
        possui_criancas=True,
        tipo_imovel="Estúdio",
        quantidade_quartos=0,
        quantidade_vagas=4,
        parcelas_contrato=5,
    )
    assert orcamento.aluguel_mensal_centavos == 157_000


def test_contrato_em_cinco_parcelas(calculo_service):
    orcamento = calculo_service.criar_orcamento(
        nome_cliente="Cliente Teste",
        possui_criancas=False,
        tipo_imovel="Apartamento",
        quantidade_quartos=2,
        quantidade_vagas=1,
        parcelas_contrato=5,
    )
    assert [p.contrato_centavos for p in orcamento.parcelas[:5]] == [40_000] * 5
    assert sum(p.contrato_centavos for p in orcamento.parcelas) == 200_000


def test_cronograma_anual_tem_doze_meses(calculo_service):
    orcamento = calculo_service.criar_orcamento(
        nome_cliente="Cliente Teste",
        possui_criancas=False,
        tipo_imovel="Apartamento",
        quantidade_quartos=2,
        quantidade_vagas=1,
        parcelas_contrato=5,
    )
    assert len(orcamento.parcelas) == 12
    assert orcamento.total_primeiro_ano_centavos == 1_568_000


def test_estudio_rejeita_uma_vaga(calculo_service):
    with pytest.raises(ValueError, match="zero vaga ou pelo menos duas"):
        calculo_service.criar_orcamento(
            nome_cliente="Cliente Teste",
            possui_criancas=True,
            tipo_imovel="Estúdio",
            quantidade_quartos=0,
            quantidade_vagas=1,
            parcelas_contrato=5,
        )


def test_contrato_em_tres_parcelas_preserva_total(calculo_service):
    orcamento = calculo_service.criar_orcamento(
        nome_cliente="Cliente Teste",
        possui_criancas=True,
        tipo_imovel="Casa",
        quantidade_quartos=1,
        quantidade_vagas=0,
        parcelas_contrato=3,
    )
    assert [p.contrato_centavos for p in orcamento.parcelas[:3]] == [66_667, 66_667, 66_666]
    assert sum(p.contrato_centavos for p in orcamento.parcelas) == 200_000


@pytest.mark.parametrize(
    "campo, valor, mensagem",
    [
        ("tipo_imovel", None, "Selecione apartamento, casa ou estúdio"),
        ("quantidade_quartos", 1.5, "quantidade de quartos deve ser um número inteiro"),
        ("quantidade_vagas", True, "quantidade de vagas deve ser um número inteiro"),
        ("parcelas_contrato", 2.5, "quantidade de parcelas deve ser um número inteiro"),
    ],
)
def test_rejeita_tipos_de_entrada_invalidos(calculo_service, campo, valor, mensagem):
    dados = {
        "nome_cliente": "Cliente Teste",
        "possui_criancas": False,
        "tipo_imovel": "Apartamento",
        "quantidade_quartos": 1,
        "quantidade_vagas": 0,
        "parcelas_contrato": 5,
    }
    dados[campo] = valor

    with pytest.raises(ValueError, match=mensagem):
        calculo_service.criar_orcamento(**dados)
