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
import sys

from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for

# Permite importar os módulos Python que estão na pasta src.
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
CSV_DIR = BASE_DIR / "saida_csv"
sys.path.insert(0, str(SRC_DIR))

from csv_exporter import ExportadorCSV  # noqa: E402
from imoveis import Apartamento, Casa, Cliente, Estudio, formatar_moeda  # noqa: E402
from orcamento import ContratoImobiliario, Orcamento  # noqa: E402

app = Flask(__name__)
app.config["SECRET_KEY"] = "rm-orcamento-aluguel-dev"


@app.template_filter("moeda")
def moeda(valor: float) -> str:
    """Filtro usado no HTML para mostrar valores em reais."""
    return formatar_moeda(valor)


def texto_para_booleano(valor: str | None) -> bool:
    """Converte valor recebido do formulário para booleano."""
    return str(valor).lower() in {"s", "sim", "true", "1", "on"}


def criar_imovel_pelo_formulario(formulario) -> Apartamento | Casa | Estudio:
    """Cria o objeto do imóvel conforme a escolha feita na tela."""
    tipo_imovel = formulario.get("tipo_imovel", "").strip().lower()

    if tipo_imovel in {"apartamento", "casa"}:
        quartos = int(formulario.get("quartos", 1))
        possui_garagem = texto_para_booleano(formulario.get("garagem"))
        vagas = 1 if possui_garagem else 0

        if tipo_imovel == "apartamento":
            return Apartamento(quartos=quartos, vagas=vagas)
        return Casa(quartos=quartos, vagas=vagas)

    if tipo_imovel == "estudio":
        deseja_estacionamento = texto_para_booleano(formulario.get("estacionamento_estudio"))
        vagas_estudio = int(formulario.get("vagas_estudio") or 0) if deseja_estacionamento else 0
        return Estudio(vagas=vagas_estudio)

    raise ValueError("Tipo de imóvel inválido. Escolha apartamento, casa ou estúdio.")


@app.get("/")
def index():
    """Exibe o formulário principal."""
    return render_template("index.html")


@app.post("/calcular")
def calcular():
    """Recebe os dados do formulário, calcula o orçamento e gera o CSV."""
    try:
        nome_cliente = request.form.get("nome_cliente", "").strip()
        if not nome_cliente:
            raise ValueError("Informe o nome do cliente.")

        possui_criancas = texto_para_booleano(request.form.get("possui_criancas"))
        cliente = Cliente(nome=nome_cliente, possui_criancas=possui_criancas)

        imovel = criar_imovel_pelo_formulario(request.form)
        parcelas_contrato = int(request.form.get("parcelas_contrato", 1))
        contrato = ContratoImobiliario(parcelas=parcelas_contrato)
        orcamento = Orcamento(cliente=cliente, imovel=imovel, contrato=contrato)

        nome_arquivo = f"orcamento_rm_web_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        caminho_csv = CSV_DIR / nome_arquivo
        ExportadorCSV.salvar(orcamento, caminho_csv)

        return render_template(
            "resultado.html",
            cliente=cliente,
            imovel=imovel,
            contrato=contrato,
            orcamento=orcamento,
            itens=imovel.calcular_itens(cliente),
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
