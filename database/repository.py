from pathlib import Path

from config import DATABASE_PATH
from models import Orcamento

from .connection import conectar, inicializar_banco


class OrcamentoRepository:
    def __init__(self, caminho_banco: str | Path = DATABASE_PATH) -> None:
        self.caminho_banco = Path(caminho_banco)
        inicializar_banco(self.caminho_banco)

    def salvar(self, orcamento: Orcamento) -> int:
        """Salva todo o agregado em uma única transação atômica."""
        with conectar(self.caminho_banco) as conexao:
            cliente_id = conexao.execute(
                """
                INSERT INTO clientes (nome, possui_criancas, criado_em)
                VALUES (?, ?, ?)
                """,
                (orcamento.cliente.nome, int(orcamento.cliente.possui_criancas), orcamento.criado_em),
            ).lastrowid

            imovel_id = conexao.execute(
                """
                INSERT INTO imoveis
                    (tipo, valor_base_centavos, quantidade_quartos, quantidade_vagas, criado_em)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    orcamento.imovel.tipo,
                    orcamento.imovel.valor_base_centavos,
                    orcamento.imovel.quantidade_quartos,
                    orcamento.imovel.quantidade_vagas,
                    orcamento.criado_em,
                ),
            ).lastrowid

            contrato_id = conexao.execute(
                """
                INSERT INTO contratos
                    (valor_total_centavos, quantidade_parcelas, valor_parcela_centavos, criado_em)
                VALUES (?, ?, ?, ?)
                """,
                (
                    orcamento.contrato.valor_total_centavos,
                    orcamento.contrato.quantidade_parcelas,
                    orcamento.contrato.valor_parcela_referencia_centavos,
                    orcamento.criado_em,
                ),
            ).lastrowid

            orcamento_id = conexao.execute(
                """
                INSERT INTO orcamentos
                    (cliente_id, imovel_id, contrato_id, aluguel_mensal_centavos,
                     total_primeiro_ano_centavos, status, criado_em)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cliente_id,
                    imovel_id,
                    contrato_id,
                    orcamento.aluguel_mensal_centavos,
                    orcamento.total_primeiro_ano_centavos,
                    orcamento.status,
                    orcamento.criado_em,
                ),
            ).lastrowid

            conexao.executemany(
                """
                INSERT INTO itens_orcamento
                    (orcamento_id, descricao, tipo, valor_centavos, ordem)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (orcamento_id, item.descricao, item.tipo, item.valor_centavos, item.ordem)
                    for item in orcamento.itens
                ],
            )

            conexao.executemany(
                """
                INSERT INTO parcelas_orcamento
                    (orcamento_id, numero_mes, aluguel_centavos, contrato_centavos, total_mes_centavos)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (
                        orcamento_id,
                        parcela.numero_mes,
                        parcela.aluguel_centavos,
                        parcela.contrato_centavos,
                        parcela.total_mes_centavos,
                    )
                    for parcela in orcamento.parcelas
                ],
            )

        orcamento.id = int(orcamento_id)
        return int(orcamento_id)

    def listar_resumo(self) -> list[dict]:
        with conectar(self.caminho_banco) as conexao:
            linhas = conexao.execute(
                "SELECT * FROM vw_orcamentos_resumo ORDER BY id DESC"
            ).fetchall()
        return [dict(linha) for linha in linhas]

    def buscar_por_id(self, orcamento_id: int) -> dict | None:
        with conectar(self.caminho_banco) as conexao:
            resumo = conexao.execute(
                "SELECT * FROM vw_orcamentos_resumo WHERE id = ?", (orcamento_id,)
            ).fetchone()
            if resumo is None:
                return None
            itens = conexao.execute(
                """
                SELECT descricao, tipo, valor_centavos, ordem
                FROM itens_orcamento
                WHERE orcamento_id = ?
                ORDER BY ordem
                """,
                (orcamento_id,),
            ).fetchall()
            parcelas = conexao.execute(
                """
                SELECT numero_mes, aluguel_centavos, contrato_centavos, total_mes_centavos
                FROM parcelas_orcamento
                WHERE orcamento_id = ?
                ORDER BY numero_mes
                """,
                (orcamento_id,),
            ).fetchall()
        return {
            "resumo": dict(resumo),
            "itens": [dict(item) for item in itens],
            "parcelas": [dict(parcela) for parcela in parcelas],
        }

    def estatisticas(self) -> dict:
        with conectar(self.caminho_banco) as conexao:
            linha = conexao.execute(
                """
                SELECT
                    COUNT(*) AS quantidade,
                    COALESCE(SUM(total_primeiro_ano_centavos), 0) AS total_primeiro_ano_centavos,
                    COALESCE(AVG(aluguel_mensal_centavos), 0) AS media_aluguel_centavos
                FROM orcamentos
                WHERE status = 'GERADO'
                """
            ).fetchone()
        return dict(linha)

    def contar_tabelas(self) -> dict[str, int]:
        tabelas = [
            "clientes",
            "imoveis",
            "contratos",
            "orcamentos",
            "itens_orcamento",
            "parcelas_orcamento",
        ]
        with conectar(self.caminho_banco) as conexao:
            return {
                tabela: int(conexao.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0])
                for tabela in tabelas
            }
