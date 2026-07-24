from streamlit.testing.v1 import AppTest


def test_painel_principal_carrega_sem_excecoes():
    app = AppTest.from_file("app.py").run(timeout=20)

    assert len(app.exception) == 0
    assert app.title[0].value == "🏠 Imobiliária R.M"
    assert [metrica.label for metrica in app.metric] == [
        "Orçamentos",
        "Clientes",
        "Aluguel médio",
        "Valor contratado",
    ]


def test_formulario_de_novo_orcamento_carrega_sem_excecoes():
    pagina = AppTest.from_file(
        "pages/1_📝_Novo_Orçamento.py"
    ).run(timeout=20)

    assert len(pagina.exception) == 0
    assert pagina.text_input[0].label == "Nome completo"
    assert pagina.selectbox[0].options == ["Apartamento", "Casa", "Estúdio"]
    assert pagina.button[0].label == "Calcular e salvar orçamento"
