import pandas as pd
import streamlit as st

from database.queries import listar_orcamentos
from services import ExportService

st.set_page_config(page_title="Orçamentos", page_icon="📋", layout="wide")
st.title("📋 Orçamentos cadastrados")
registros = listar_orcamentos()
if registros:
    st.dataframe(pd.DataFrame(registros), width="stretch", hide_index=True)
    st.download_button("⬇️ Exportar listagem", ExportService.gerar_csv_registros(registros), "orcamentos_rm.csv", "text/csv")
else:
    st.info("Nenhum orçamento cadastrado.")
