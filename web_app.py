"""Interface web do projeto Orçamento de Aluguel - Imobiliária R.M.

Execute na pasta raiz do projeto:
    pip install -r requirements.txt
    python web_app.py

Depois acesse no navegador:
    http://127.0.0.1:5000
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for

BASE_DIR = Path(__file__).resolve().parent
CSV_DIR = BASE_DIR / "saida_csv"

from banco_de_dados import OrcamentoRepository
from servicos import OrcamentoService
from utilitarios import formatar_moeda
from utilitarios.exportador_csv import exportar_csv

app = Flask(__name__)
app.config["SECRET_KEY"] = "rm-orcamento-aluguel-dev"


@app.template_filter("moeda")
def moeda(valor: float) -> str:
    """Filtro usado no HTML para mostrar valores em reais."""
    return formatar_moeda(valor)


@app.get("/")
def index():
    """Exibe o formulário principal."""
    return render_template("index.html")


@app.post("/calcular")
def calcular():
    """Recebe os dados do formulário, calcula o orçamento e gera o CSV."""
    try:
        orcamento = OrcamentoService.criar(request.form.to_dict())
        OrcamentoRepository(BASE_DIR / "dados" / "orcamentos.db").salvar(orcamento)

        nome_arquivo = f"orcamento_rm_web_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        caminho_csv = CSV_DIR / nome_arquivo
        exportar_csv(orcamento, caminho_csv)

        return render_template(
            "resultado.html",
            cliente=orcamento.cliente,
            imovel=orcamento.imovel,
            contrato=orcamento.contrato,
            orcamento=orcamento,
            itens=orcamento.imovel.calcular_itens(orcamento.cliente),
            cronograma=orcamento.gerar_cronograma_12_meses(),
            nome_arquivo=nome_arquivo,
        )
    except ValueError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("index"))
    except Exception as erro:  # Proteção geral para evitar tela quebrada.
        flash(f"Erro inesperado: {erro}", "erro")
        return redirect(url_for("index"))


@app.get("/download/<nome_arquivo>")
def download_csv(nome_arquivo: str):
    """Permite baixar o CSV gerado pela interface web."""
    return send_from_directory(CSV_DIR, nome_arquivo, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
