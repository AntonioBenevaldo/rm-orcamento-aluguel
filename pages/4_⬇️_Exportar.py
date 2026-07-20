import streamlit as st

from database.queries import listar_orcamentos
from services import ExportService

st.set_page_config(page_title="Exportar", page_icon="⬇️", layout="wide")
st.title("⬇️ Central de exportação")
registros = listar_orcamentos()
st.write(f"{len(registros)} orçamento(s) disponível(is) para exportação.")
if registros:
    st.download_button("Gerar CSV consolidado", ExportService.gerar_csv_registros(registros), "historico_orcamentos_rm.csv", "text/csv", type="primary")
