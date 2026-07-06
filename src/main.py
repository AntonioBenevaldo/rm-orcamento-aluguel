"""Aplicação principal - Orçamento de Aluguel R.M.

Execute pelo terminal:
    python main.py

A aplicação usa orientação a objetos para calcular o orçamento de aluguel
mensal e permite gerar um arquivo CSV com as 12 parcelas do orçamento.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from csv_exporter import ExportadorCSV
from imoveis import Apartamento, Casa, Cliente, Estudio
from orcamento import ContratoImobiliario, Orcamento


def ler_texto(mensagem: str) -> str:
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Informe um valor válido.")


def ler_inteiro(mensagem: str, opcoes_validas: set[int] | None = None, minimo: int | None = None) -> int:
    while True:
        try:
            valor = int(input(mensagem).strip())
            if opcoes_validas is not None and valor not in opcoes_validas:
                print(f"Opção inválida. Escolha uma das opções: {sorted(opcoes_validas)}")
                continue
            if minimo is not None and valor < minimo:
                print(f"Valor inválido. Informe um número maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Digite apenas números inteiros.")


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in {"s", "sim"}:
            return True
        if resposta in {"n", "nao", "não"}:
            return False
        print("Resposta inválida. Digite S para sim ou N para não.")


def criar_imovel():
    print("\nTipos de imóvel disponíveis:")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    tipo = ler_inteiro("Escolha o tipo de imóvel: ", {1, 2, 3})

    if tipo == 1:
        quartos = ler_inteiro("Quantidade de quartos do apartamento (1 ou 2): ", {1, 2})
        possui_garagem = ler_sim_nao("Deseja incluir vaga de garagem por R$ 300,00? (S/N): ")
        return Apartamento(quartos=quartos, vagas=1 if possui_garagem else 0)

    if tipo == 2:
        quartos = ler_inteiro("Quantidade de quartos da casa (1 ou 2): ", {1, 2})
        possui_garagem = ler_sim_nao("Deseja incluir vaga de garagem por R$ 300,00? (S/N): ")
        return Casa(quartos=quartos, vagas=1 if possui_garagem else 0)

    print("Para estúdio, o pacote de estacionamento começa com 2 vagas por R$ 250,00.")
    deseja_vagas = ler_sim_nao("Deseja incluir estacionamento no estúdio? (S/N): ")
    if deseja_vagas:
        vagas = ler_inteiro("Quantidade de vagas de estacionamento (mínimo 2): ", minimo=2)
    else:
        vagas = 0
    return Estudio(vagas=vagas)


def main() -> None:
    print("\nSISTEMA DE ORÇAMENTO DE ALUGUEL - IMOBILIÁRIA R.M")
    print("=" * 60)

    nome_cliente = ler_texto("Nome do cliente: ")
    possui_criancas = ler_sim_nao("O cliente possui crianças? (S/N): ")
    cliente = Cliente(nome=nome_cliente, possui_criancas=possui_criancas)

    imovel = criar_imovel()
    parcelas_contrato = ler_inteiro("Parcelas do contrato imobiliário de R$ 2.000,00 (1 a 5): ", {1, 2, 3, 4, 5})
    contrato = ContratoImobiliario(parcelas=parcelas_contrato)

    orcamento = Orcamento(cliente=cliente, imovel=imovel, contrato=contrato)
    print("\n" + orcamento.resumo_texto())

    gerar_csv = ler_sim_nao("\nDeseja gerar o CSV com as 12 parcelas? (S/N): ")
    if gerar_csv:
        nome_arquivo = f"orcamento_rm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        caminho = Path.cwd() / nome_arquivo
        ExportadorCSV.salvar(orcamento, caminho)
        print(f"Arquivo CSV gerado com sucesso: {caminho}")

    print("\nAplicação finalizada.")


if __name__ == "__main__":
    main()
