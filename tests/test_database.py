import sqlite3

import pytest

from database.connection import conectar
from models import ParcelaOrcamento


def criar_orcamento_exemplo(calculo_service):
    return calculo_service.criar_orcamento(
        nome_cliente="Cliente Teste",
        possui_criancas=False,
        tipo_imovel="Apartamento",
        quantidade_quartos=2,
        quantidade_vagas=1,
        parcelas_contrato=5,
    )


def test_persistencia_e_integridade_referencial(calculo_service, repositorio):
    orcamento = criar_orcamento_exemplo(calculo_service)
    orcamento_id = repositorio.salvar(orcamento)
    dados = repositorio.buscar_por_id(orcamento_id)

    assert dados is not None
    assert dados["resumo"]["aluguel_mensal_centavos"] == 114_000
    assert len(dados["itens"]) == 4
    assert len(dados["parcelas"]) == 12

    with conectar(repositorio.caminho_banco) as conexao:
        violacoes = conexao.execute("PRAGMA foreign_key_check").fetchall()
    assert violacoes == []


def test_pragma_integrity_check(calculo_service, repositorio):
    repositorio.salvar(criar_orcamento_exemplo(calculo_service))
    with conectar(repositorio.caminho_banco) as conexao:
        resultado = conexao.execute("PRAGMA integrity_check").fetchone()[0]
    assert resultado == "ok"


def test_transacao_impede_registro_parcial(calculo_service, repositorio):
    orcamento = criar_orcamento_exemplo(calculo_service)
    ultima = orcamento.parcelas[-1]
    orcamento.parcelas[-1] = ParcelaOrcamento(
        numero_mes=11,
        aluguel_centavos=ultima.aluguel_centavos,
        contrato_centavos=ultima.contrato_centavos,
        total_mes_centavos=ultima.total_mes_centavos,
    )

    with pytest.raises(sqlite3.IntegrityError):
        repositorio.salvar(orcamento)

    assert all(quantidade == 0 for quantidade in repositorio.contar_tabelas().values())
