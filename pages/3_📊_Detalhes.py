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
    a.metric("Cliente", detalhe["cliente"]); b.metric("Aluguel", moeda_br(detalhe["aluguel_mensal"])); c.metric("Total anual", moeda_br(detalhe["total_primeiro_ano"]))
    st.subheader("Itens do cálculo"); st.dataframe(pd.DataFrame(detalhe["itens"]), width="stretch", hide_index=True)
    st.subheader("Parcelas"); st.dataframe(pd.DataFrame(detalhe["parcelas"]), width="stretch", hide_index=True)
