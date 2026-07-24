"""Aplicação principal Streamlit - Sistema de Orçamento Imobiliário R.M."""

import streamlit as st

from database.connection import inicializar_banco
from database.queries import obter_indicadores, listar_orcamentos
from utils.formatters import moeda_br

st.set_page_config(page_title="Imobiliária R.M", page_icon="🏠", layout="wide")
inicializar_banco()

st.title("🏠 Imobiliária R.M")
st.caption("Sistema de orçamento de aluguel")

indicadores = obter_indicadores()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Orçamentos", indicadores["quantidade"])
col2.metric("Clientes", indicadores["clientes"])
col3.metric("Aluguel médio", moeda_br(indicadores["aluguel_medio_centavos"]))
col4.metric("Valor contratado", moeda_br(indicadores["valor_total_centavos"]))

st.subheader("Orçamentos recentes")
registros = listar_orcamentos(limite=5)
if registros:
    exibicao = [
        {
            "Nº": registro["id"],
            "Cliente": registro["cliente"],
            "Imóvel": registro["imovel"].title(),
            "Aluguel mensal": moeda_br(registro["aluguel_mensal_centavos"]),
            "Parcelas do contrato": registro["parcelas_contrato"],
            "Total no primeiro ano": moeda_br(registro["total_primeiro_ano_centavos"]),
            "Status": registro["status"].title(),
            "Criado em": registro["criado_em"],
        }
        for registro in registros
    ]
    st.dataframe(exibicao, width="stretch", hide_index=True)
else:
    st.info("Nenhum orçamento cadastrado. Acesse **Novo Orçamento** no menu lateral.")

with st.expander("Regras consideradas pelo sistema"):
    st.markdown("""
    - Apartamento: R$ 700,00; segundo quarto +R$ 200,00; garagem +R$ 300,00.
    - Casa: R$ 900,00; segundo quarto +R$ 250,00; garagem +R$ 300,00.
    - Estúdio: R$ 1.200,00; duas vagas +R$ 250,00; vaga adicional +R$ 60,00.
    - Apartamento para cliente sem crianças: desconto de 5%.
    - Contrato imobiliário: R$ 2.000,00, parcelado em até cinco vezes.
    """)
