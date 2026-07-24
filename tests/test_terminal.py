import csv
from io import StringIO

from main import executar


def criar_entrada(respostas):
    valores = iter(respostas)
    return lambda _mensagem: next(valores)


def test_terminal_calcula_salva_exibe_e_exporta_csv(tmp_path):
    saidas = []
    codigo = executar(
        entrada=criar_entrada(
            [
                "Cliente Demonstração",
                "n",
                "1",
                "2",
                "s",
                "5",
                "s",
            ]
        ),
        saida=saidas.append,
        diretorio_csv=tmp_path / "exports",
        caminho_banco=tmp_path / "terminal.db",
    )

    texto = "\n".join(saidas)
    arquivos = list((tmp_path / "exports").glob("*.csv"))

    assert codigo == 0
    assert "R$ 1.140,00" in texto
    assert "R$ 15.680,00" in texto
    assert "ORÇAMENTO Nº 1" in texto
    assert len(arquivos) == 1

    with arquivos[0].open(encoding="utf-8-sig", newline="") as arquivo:
        linhas = list(csv.DictReader(arquivo, delimiter=";"))
    assert len(linhas) == 12
    assert linhas[0]["total_mes_centavos"] == "154000"


def test_terminal_valida_opcoes_antes_de_continuar(tmp_path):
    saidas = []
    codigo = executar(
        entrada=criar_entrada(
            [
                "A",
                "Cliente Teste",
                "talvez",
                "s",
                "9",
                "2",
                "3",
                "1",
                "n",
                "2",
                "n",
            ]
        ),
        saida=saidas.append,
        caminho_banco=tmp_path / "validacao.db",
    )

    texto = "\n".join(saidas)
    assert codigo == 0
    assert "pelo menos dois caracteres" in texto
    assert "Resposta inválida" in texto
    assert "Opção inválida" in texto


def test_terminal_encerra_sem_traceback_quando_usuario_interrompe(tmp_path):
    saidas = []

    def interromper(_mensagem):
        raise KeyboardInterrupt

    codigo = executar(
        entrada=interromper,
        saida=saidas.append,
        caminho_banco=tmp_path / "interrompido.db",
    )

    assert codigo == 130
    assert "Execução cancelada pelo usuário." in "\n".join(saidas)
