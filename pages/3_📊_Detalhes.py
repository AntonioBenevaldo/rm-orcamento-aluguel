import pandas as pd
import streamlit as st

from database.queries import listar_orcamentos, obter_orcamento
from utils import moeda_br

st.set_page_config(page_title="Detalhes", page_icon="📊", layout="wide")
st.title("📊 Detalhes do orçamento")
registros = listar_orcamentos()
if not registros:
    st.info("Cadastre um orçamento primeiro.")
else:
    escolhido = st.selectbox("Orçamento", registros, format_func=lambda x: f"#{x['id']} - {x['cliente']} - {x['imovel'].title()}")
    detalhe = obter_orcamento(escolhido["id"])
    a, b, c = st.columns(3)
    a.metric("Cliente", detalhe["cliente"])
    b.metric("Aluguel", moeda_br(detalhe["aluguel_mensal_centavos"]))
    c.metric("Total anual", moeda_br(detalhe["total_primeiro_ano_centavos"]))

    itens = pd.DataFrame(
        [
            {
                "Descrição": item["descricao"],
                "Tipo": item["tipo"].title(),
                "Valor": moeda_br(item["valor_centavos"]),
            }
            for item in detalhe["itens"]
        ]
    )
    parcelas = pd.DataFrame(
        [
            {
                "Mês": parcela["numero_mes"],
                "Aluguel": moeda_br(parcela["aluguel_centavos"]),
                "Contrato": moeda_br(parcela["contrato_centavos"]),
                "Total": moeda_br(parcela["total_mes_centavos"]),
            }
            for parcela in detalhe["parcelas"]
        ]
    )
    st.subheader("Itens do cálculo")
    st.dataframe(itens, width="stretch", hide_index=True)
    st.subheader("Parcelas")
    st.dataframe(parcelas, width="stretch", hide_index=True)
