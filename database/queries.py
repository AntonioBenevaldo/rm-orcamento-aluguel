from pathlib import Path

from models import Orcamento
from .connection import DB_PATH, conectar, inicializar_banco


def salvar_orcamento(orcamento: Orcamento, caminho: str | Path = DB_PATH) -> int:
    """Persiste o agregado completo em uma única transação atômica."""
    inicializar_banco(caminho)
    with conectar(caminho) as db:
        cliente_id = db.execute(
            "INSERT INTO clientes(nome, possui_criancas) VALUES (?, ?)",
            (orcamento.cliente.nome, int(orcamento.cliente.possui_criancas)),
        ).lastrowid
        imovel_id = db.execute(
            """INSERT INTO imoveis(
                tipo, valor_base_centavos, quantidade_quartos, quantidade_vagas
            ) VALUES (?, ?, ?, ?)""",
            (
                orcamento.imovel.tipo,
                orcamento.imovel.valor_base_centavos,
                orcamento.imovel.quartos,
                orcamento.imovel.vagas,
            ),
        ).lastrowid
        contrato_id = db.execute(
            """INSERT INTO contratos(
                valor_total_centavos, quantidade_parcelas, valor_parcela_centavos
            ) VALUES (?, ?, ?)""",
            (
                orcamento.contrato.valor_total_centavos,
                orcamento.contrato.quantidade_parcelas,
                orcamento.contrato.valor_parcela_centavos,
            ),
        ).lastrowid
        orcamento_id = db.execute(
            """INSERT INTO orcamentos(
                cliente_id, imovel_id, contrato_id,
                aluguel_mensal_centavos, total_primeiro_ano_centavos
            ) VALUES (?, ?, ?, ?, ?)""",
            (
                cliente_id,
                imovel_id,
                contrato_id,
                orcamento.aluguel_mensal_centavos,
                orcamento.total_primeiro_ano_centavos,
            ),
        ).lastrowid
        db.executemany(
            """INSERT INTO itens_orcamento(
                orcamento_id, descricao, tipo, valor_centavos, ordem
            ) VALUES (?, ?, ?, ?, ?)""",
            [
                (
                    orcamento_id,
                    item.descricao,
                    item.tipo,
                    item.valor_centavos,
                    ordem,
                )
                for ordem, item in enumerate(orcamento.itens, 1)
            ],
        )
        db.executemany(
            """INSERT INTO parcelas_orcamento(
                orcamento_id, numero_mes, aluguel_centavos,
                contrato_centavos, total_mes_centavos
            ) VALUES (?, ?, ?, ?, ?)""",
            [
                (
                    orcamento_id,
                    linha["numero_mes"],
                    linha["aluguel_centavos"],
                    linha["contrato_centavos"],
                    linha["total_mes_centavos"],
                )
                for linha in orcamento.cronograma()
            ],
        )
        return int(orcamento_id)


def listar_orcamentos(limite: int | None = None, caminho: str | Path = DB_PATH) -> list[dict]:
    inicializar_banco(caminho)
    sql = "SELECT * FROM vw_orcamentos_resumo ORDER BY id DESC" + (" LIMIT ?" if limite else "")
    with conectar(caminho) as db:
        linhas = db.execute(sql, (limite,) if limite else ()).fetchall()
        return [dict(linha) for linha in linhas]


def obter_orcamento(orcamento_id: int, caminho: str | Path = DB_PATH) -> dict | None:
    inicializar_banco(caminho)
    with conectar(caminho) as db:
        resumo = db.execute("SELECT * FROM vw_orcamentos_resumo WHERE id = ?", (orcamento_id,)).fetchone()
        if not resumo: return None
        resultado = dict(resumo)
        resultado["itens"] = [
            dict(x)
            for x in db.execute(
                """SELECT descricao, tipo, valor_centavos
                FROM itens_orcamento
                WHERE orcamento_id = ?
                ORDER BY ordem""",
                (orcamento_id,),
            )
        ]
        resultado["parcelas"] = [
            dict(x)
            for x in db.execute(
                """SELECT numero_mes, aluguel_centavos,
                    contrato_centavos, total_mes_centavos
                FROM parcelas_orcamento
                WHERE orcamento_id = ?
                ORDER BY numero_mes""",
                (orcamento_id,),
            )
        ]
        return resultado


def obter_indicadores(caminho: str | Path = DB_PATH) -> dict:
    inicializar_banco(caminho)
    with conectar(caminho) as db:
        row = db.execute(
            """SELECT
                COUNT(*) AS quantidade,
                COUNT(DISTINCT cliente_id) AS clientes,
                CAST(COALESCE(AVG(aluguel_mensal_centavos), 0) AS INTEGER)
                    AS aluguel_medio_centavos,
                COALESCE(SUM(total_primeiro_ano_centavos), 0)
                    AS valor_total_centavos
            FROM orcamentos"""
        ).fetchone()
        return dict(row)
