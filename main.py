"""Aplicação de terminal do Sistema de Orçamento Imobiliário R.M.

Execute na pasta do projeto:
    python main.py
"""

from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from database.connection import DB_PATH, inicializar_banco
from database.queries import salvar_orcamento
from services import CalculoService, ExportService
from utils import moeda_br

Entrada = Callable[[str], str]
Saida = Callable[[str], None]


def ler_texto(mensagem: str, entrada: Entrada, saida: Saida) -> str:
    while True:
        valor = entrada(mensagem).strip()
        if len(valor) >= 2:
            return valor
        saida("Informe um nome com pelo menos dois caracteres.")


def ler_opcao(
    mensagem: str,
    opcoes_validas: set[int],
    entrada: Entrada,
    saida: Saida,
) -> int:
    while True:
        try:
            valor = int(entrada(mensagem).strip())
        except ValueError:
            saida("Digite apenas o número da opção.")
            continue
        if valor in opcoes_validas:
            return valor
        saida(f"Opção inválida. Escolha: {sorted(opcoes_validas)}.")


def ler_sim_nao(mensagem: str, entrada: Entrada, saida: Saida) -> bool:
    while True:
        resposta = entrada(mensagem).strip().lower()
        if resposta in {"s", "sim"}:
            return True
        if resposta in {"n", "nao", "não"}:
            return False
        saida("Resposta inválida. Digite S para sim ou N para não.")


def coletar_dados(entrada: Entrada, saida: Saida) -> dict:
    saida("")
    saida("DADOS DO CLIENTE")
    saida("-" * 60)
    nome = ler_texto("Nome do cliente: ", entrada, saida)
    possui_criancas = ler_sim_nao(
        "O cliente possui crianças? (S/N): ", entrada, saida
    )

    saida("")
    saida("TIPO DE IMÓVEL")
    saida("1 - Apartamento")
    saida("2 - Casa")
    saida("3 - Estúdio")
    tipo_numero = ler_opcao(
        "Escolha o tipo de imóvel: ", {1, 2, 3}, entrada, saida
    )
    tipo = {1: "Apartamento", 2: "Casa", 3: "Estúdio"}[tipo_numero]

    if tipo_numero in {1, 2}:
        quartos = ler_opcao(
            "Quantidade de quartos (1 ou 2): ", {1, 2}, entrada, saida
        )
        garagem = ler_sim_nao(
            "Adicionar garagem por R$ 300,00? (S/N): ", entrada, saida
        )
        vagas = 1 if garagem else 0
    else:
        quartos = 1
        estacionamento = ler_sim_nao(
            "Adicionar estacionamento ao estúdio? (S/N): ", entrada, saida
        )
        if estacionamento:
            while True:
                try:
                    vagas = int(
                        entrada("Quantidade de vagas (mínimo 2): ").strip()
                    )
                    if vagas >= 2:
                        break
                except ValueError:
                    pass
                saida("Informe zero vagas ou uma quantidade igual ou superior a 2.")
        else:
            vagas = 0

    saida("")
    saida("CONTRATO IMOBILIÁRIO")
    parcelas = ler_opcao(
        "Parcelas do contrato de R$ 2.000,00 (1 a 5): ",
        {1, 2, 3, 4, 5},
        entrada,
        saida,
    )
    return {
        "nome": nome,
        "possui_criancas": possui_criancas,
        "tipo": tipo,
        "quartos": quartos,
        "vagas": vagas,
        "parcelas": parcelas,
    }


def exibir_orcamento(orcamento, codigo: int, saida: Saida) -> None:
    saida("")
    saida("=" * 72)
    saida(f"ORÇAMENTO Nº {codigo} - IMOBILIÁRIA R.M")
    saida("=" * 72)
    saida(f"Cliente: {orcamento.cliente.nome}")
    saida(f"Imóvel: {orcamento.imovel.tipo.title()}")
    saida(f"Quartos: {orcamento.imovel.quartos}")
    saida(f"Vagas: {orcamento.imovel.vagas}")
    saida("")
    saida("COMPOSIÇÃO DO ALUGUEL")
    for item in orcamento.itens:
        saida(f"  {item.descricao:<48} {moeda_br(item.valor_centavos):>18}")
    saida("-" * 72)
    saida(
        f"Aluguel mensal:{moeda_br(orcamento.aluguel_mensal_centavos):>57}"
    )
    saida(
        f"Contrato imobiliário:{moeda_br(orcamento.contrato.valor_total_centavos):>52}"
    )
    saida(
        f"Total do primeiro ano:{moeda_br(orcamento.total_primeiro_ano_centavos):>51}"
    )
    saida("")
    saida("CRONOGRAMA DE 12 MESES")
    saida(f"{'Mês':>3} | {'Aluguel':>14} | {'Contrato':>14} | {'Total':>14}")
    saida("-" * 57)
    for linha in orcamento.cronograma():
        saida(
            f"{linha['numero_mes']:>3} | "
            f"{moeda_br(linha['aluguel_centavos']):>14} | "
            f"{moeda_br(linha['contrato_centavos']):>14} | "
            f"{moeda_br(linha['total_mes_centavos']):>14}"
        )


def executar(
    entrada: Entrada = input,
    saida: Saida = print,
    diretorio_csv: str | Path = "exports",
    caminho_banco: str | Path = DB_PATH,
) -> int:
    inicializar_banco(caminho_banco)
    saida("=" * 72)
    saida("        SISTEMA DE ORÇAMENTO IMOBILIÁRIO R.M - TERMINAL")
    saida("=" * 72)

    try:
        dados = coletar_dados(entrada, saida)
        orcamento = CalculoService.processar_orcamento(
            dados["nome"],
            dados["possui_criancas"],
            dados["tipo"],
            dados["quartos"],
            dados["vagas"],
            dados["parcelas"],
        )
        codigo = salvar_orcamento(orcamento, caminho_banco)
        exibir_orcamento(orcamento, codigo, saida)

        if ler_sim_nao(
            "\nDeseja gerar o arquivo CSV? (S/N): ", entrada, saida
        ):
            destino = Path(diretorio_csv)
            destino.mkdir(parents=True, exist_ok=True)
            nome = (
                f"orcamento_rm_{codigo}_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            caminho = destino / nome
            caminho.write_bytes(ExportService.gerar_csv(orcamento))
            saida(f"CSV gerado com sucesso: {caminho.resolve()}")

        saida("\nAplicação finalizada com sucesso.")
        return 0
    except (EOFError, KeyboardInterrupt):
        saida("\n\nExecução cancelada pelo usuário.")
        return 130
    except (OSError, TypeError, ValueError) as erro:
        saida(f"\nErro: {erro}")
        return 1


if __name__ == "__main__":
    raise SystemExit(executar())
