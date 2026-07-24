import sqlite3

import pytest

from database.connection import conectar, inicializar_banco
from database.queries import (
    listar_orcamentos,
    obter_indicadores,
    obter_orcamento,
    salvar_orcamento,
)
from services import CalculoService


def criar_orcamento():
    return CalculoService.processar_orcamento(
        "Cliente Demonstração", False, "Apartamento", 2, 1, 5
    )


def test_modelo_fisico_e_persistencia_completa(tmp_path):
    banco = tmp_path / "imobiliaria_teste.db"
    codigo = salvar_orcamento(criar_orcamento(), banco)
    detalhe = obter_orcamento(codigo, banco)

    assert detalhe["aluguel_mensal_centavos"] == 114_000
    assert detalhe["total_primeiro_ano_centavos"] == 1_568_000
    assert len(detalhe["itens"]) == 4
    assert len(detalhe["parcelas"]) == 12
    assert listar_orcamentos(caminho=banco)[0]["id"] == codigo

    with sqlite3.connect(banco) as db:
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
        assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert db.execute("PRAGMA user_version").fetchone()[0] == 1


def test_indicadores_permanecem_em_centavos_inteiros(tmp_path):
    banco = tmp_path / "indicadores.db"
    salvar_orcamento(criar_orcamento(), banco)
    indicadores = obter_indicadores(banco)

    assert indicadores == {
        "quantidade": 1,
        "clientes": 1,
        "aluguel_medio_centavos": 114_000,
        "valor_total_centavos": 1_568_000,
    }


def test_transacao_reverte_todos_os_registros_em_caso_de_falha(tmp_path):
    banco = tmp_path / "rollback.db"
    inicializar_banco(banco)
    with conectar(banco) as db:
        db.execute(
            """CREATE TRIGGER impedir_parcelas
            BEFORE INSERT ON parcelas_orcamento
            BEGIN
                SELECT RAISE(ABORT, 'falha simulada');
            END;"""
        )

    with pytest.raises(sqlite3.IntegrityError, match="falha simulada"):
        salvar_orcamento(criar_orcamento(), banco)

    with conectar(banco) as db:
        for tabela in (
            "clientes",
            "imoveis",
            "contratos",
            "orcamentos",
            "itens_orcamento",
            "parcelas_orcamento",
        ):
            assert db.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0] == 0
