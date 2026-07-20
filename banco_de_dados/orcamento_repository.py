"""Repositório SQLite para manter o histórico dos orçamentos."""

import sqlite3
from pathlib import Path

from modelos import Orcamento


class OrcamentoRepository:
    def __init__(self, caminho: str | Path = "dados/orcamentos.db") -> None:
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self._criar_tabela()

    def _conectar(self) -> sqlite3.Connection:
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        return conexao

    def _criar_tabela(self) -> None:
        with self._conectar() as conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS orcamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente TEXT NOT NULL,
                    possui_criancas INTEGER NOT NULL,
                    tipo_imovel TEXT NOT NULL,
                    quartos INTEGER NOT NULL,
                    vagas INTEGER NOT NULL,
                    aluguel_mensal REAL NOT NULL,
                    parcelas_contrato INTEGER NOT NULL,
                    total_primeiro_ano REAL NOT NULL,
                    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def salvar(self, orcamento: Orcamento) -> int:
        with self._conectar() as conexao:
            cursor = conexao.execute(
                """INSERT INTO orcamentos
                (cliente, possui_criancas, tipo_imovel, quartos, vagas, aluguel_mensal, parcelas_contrato, total_primeiro_ano)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (orcamento.cliente.nome, int(orcamento.cliente.possui_criancas), orcamento.imovel.tipo,
                 orcamento.imovel.quartos, orcamento.imovel.vagas, orcamento.aluguel_mensal,
                 orcamento.contrato.parcelas, orcamento.total_primeiro_ano()),
            )
            return int(cursor.lastrowid)

    def listar(self) -> list[dict]:
        with self._conectar() as conexao:
            return [dict(linha) for linha in conexao.execute("SELECT * FROM orcamentos ORDER BY id DESC")]
