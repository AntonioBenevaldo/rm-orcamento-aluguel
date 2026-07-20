from pathlib import Path

from models import Orcamento
from .connection import DB_PATH, conectar, inicializar_banco


def _centavos(valor: float) -> int: return round(valor * 100)


def salvar_orcamento(orcamento: Orcamento, caminho: str | Path = DB_PATH) -> int:
    inicializar_banco(caminho)
    with conectar(caminho) as db:
        cliente_id = db.execute("INSERT INTO clientes(nome, possui_criancas) VALUES (?, ?)", (orcamento.cliente.nome, int(orcamento.cliente.possui_criancas))).lastrowid
        imovel_id = db.execute("INSERT INTO imoveis(tipo, valor_base_centavos, quantidade_quartos, quantidade_vagas) VALUES (?, ?, ?, ?)", (orcamento.imovel.tipo, _centavos(orcamento.imovel.valor_base), orcamento.imovel.quartos, orcamento.imovel.vagas)).lastrowid
        contrato_id = db.execute("INSERT INTO contratos(valor_total_centavos, quantidade_parcelas, valor_parcela_centavos) VALUES (?, ?, ?)", (_centavos(orcamento.contrato.valor_total), orcamento.contrato.quantidade_parcelas, _centavos(orcamento.contrato.valor_parcela))).lastrowid
        orcamento_id = db.execute("INSERT INTO orcamentos(cliente_id, imovel_id, contrato_id, aluguel_mensal_centavos, total_primeiro_ano_centavos) VALUES (?, ?, ?, ?, ?)", (cliente_id, imovel_id, contrato_id, _centavos(orcamento.aluguel_mensal), _centavos(orcamento.total_primeiro_ano))).lastrowid
        db.executemany("INSERT INTO itens_orcamento(orcamento_id, descricao, tipo, valor_centavos, ordem) VALUES (?, ?, ?, ?, ?)", [(orcamento_id, item.descricao, item.tipo, _centavos(item.valor), ordem) for ordem, item in enumerate(orcamento.itens, 1)])
        db.executemany("INSERT INTO parcelas_orcamento(orcamento_id, numero_mes, aluguel_centavos, contrato_centavos, total_mes_centavos) VALUES (?, ?, ?, ?, ?)", [(orcamento_id, linha["mes"], _centavos(linha["aluguel"]), _centavos(linha["contrato"]), _centavos(linha["total"])) for linha in orcamento.cronograma()])
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
        resultado["itens"] = [dict(x) for x in db.execute("SELECT descricao, tipo, valor_centavos / 100.0 AS valor FROM itens_orcamento WHERE orcamento_id = ? ORDER BY ordem", (orcamento_id,))]
        resultado["parcelas"] = [dict(x) for x in db.execute("SELECT numero_mes AS mes, aluguel_centavos / 100.0 AS aluguel, contrato_centavos / 100.0 AS contrato, total_mes_centavos / 100.0 AS total FROM parcelas_orcamento WHERE orcamento_id = ? ORDER BY numero_mes", (orcamento_id,))]
        return resultado


def obter_indicadores(caminho: str | Path = DB_PATH) -> dict:
    inicializar_banco(caminho)
    with conectar(caminho) as db:
        row = db.execute("SELECT COUNT(*) quantidade, COUNT(DISTINCT cliente_id) clientes, COALESCE(AVG(aluguel_mensal_centavos), 0) / 100.0 aluguel_medio, COALESCE(SUM(total_primeiro_ano_centavos), 0) / 100.0 valor_total FROM orcamentos").fetchone()
        return dict(row)
