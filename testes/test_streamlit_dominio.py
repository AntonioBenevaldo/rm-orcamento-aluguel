import sqlite3

import pytest

from database.connection import inicializar_banco
from database.queries import obter_orcamento, salvar_orcamento
from services import CalculoService, ExportService


@pytest.mark.parametrize("tipo,criancas,quartos,vagas,parcelas,aluguel", [
    ("Apartamento", False, 2, 1, 5, 1140.0),
    ("Casa", True, 2, 1, 4, 1450.0),
    ("Estúdio", False, 1, 4, 2, 1570.0),
])
def test_regras_oficiais(tipo, criancas, quartos, vagas, parcelas, aluguel):
    orcamento = CalculoService.processar_orcamento("Cliente Teste", criancas, tipo, quartos, vagas, parcelas)
    assert orcamento.aluguel_mensal == aluguel
    assert len(orcamento.cronograma()) == 12
    assert orcamento.total_primeiro_ano == aluguel * 12 + 2000


def test_persistencia_fisica_completa(tmp_path):
    banco = tmp_path / "teste.db"
    inicializar_banco(banco)
    orcamento = CalculoService.processar_orcamento("Ana Silva", False, "Apartamento", 2, 1, 5)
    codigo = salvar_orcamento(orcamento, banco)
    detalhe = obter_orcamento(codigo, banco)
    assert detalhe["aluguel_mensal"] == 1140.0
    assert len(detalhe["itens"]) == 4
    assert len(detalhe["parcelas"]) == 12
    with sqlite3.connect(banco) as db:
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
        assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"


def test_csv_tem_doze_meses():
    orcamento = CalculoService.processar_orcamento("João Lima", True, "Casa", 1, 0, 3)
    csv = ExportService.gerar_csv(orcamento).decode("utf-8-sig")
    assert len(csv.strip().splitlines()) == 13
    assert "Parcela do contrato" in csv
