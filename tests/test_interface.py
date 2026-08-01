import pytest

streamlit = pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest


@pytest.mark.parametrize(
    ("arquivo", "titulo_esperado"),
    [
        ("app.py", "Sistema de Orçamento Imobiliário R.M"),
        ("pages/1_Novo_orcamento.py", "Novo orçamento"),
        ("pages/2_Orcamentos_registrados.py", "Orçamentos registrados"),
        ("pages/3_Regras_e_arquitetura.py", "Regras e arquitetura"),
    ],
)
def test_paginas_carregam_sem_excecao(arquivo, titulo_esperado):
    app = AppTest.from_file(arquivo)
    app.run(timeout=10)
    assert not app.exception
    assert any(titulo_esperado in titulo.value for titulo in app.title)


def test_formulario_de_novo_orcamento_exibe_campos_principais():
    app = AppTest.from_file("pages/1_Novo_orcamento.py")
    app.run(timeout=10)

    assert not app.exception
    assert app.text_input[0].label == "Nome ou identificador do cliente"
    assert app.selectbox[0].label == "Tipo de imóvel"
    assert app.slider[0].label == "Parcelas do contrato de R$ 2.000,00"
