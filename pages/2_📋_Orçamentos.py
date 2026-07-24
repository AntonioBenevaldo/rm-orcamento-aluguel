import pandas as pd
import streamlit as st

from database.queries import listar_orcamentos
from services import ExportService
from utils import moeda_br

st.set_page_config(page_title="Orçamentos", page_icon="📋", layout="wide")
st.title("📋 Orçamentos cadastrados")
registros = listar_orcamentos()
if registros:
    exibicao = pd.DataFrame(
        [
            {
                "Nº": registro["id"],
                "Cliente": registro["cliente"],
                "Imóvel": registro["imovel"].title(),
                "Aluguel mensal": moeda_br(registro["aluguel_mensal_centavos"]),
                "Parcelas": registro["parcelas_contrato"],
                "Total anual": moeda_br(registro["total_primeiro_ano_centavos"]),
                "Status": registro["status"].title(),
                "Data": registro["criado_em"],
            }
            for registro in registros
        ]
    )
    st.dataframe(exibicao, width="stretch", hide_index=True)
    st.download_button("⬇️ Exportar listagem", ExportService.gerar_csv_registros(registros), "orcamentos_rm.csv", "text/csv")
else:
    st.info("Nenhum orçamento cadastrado.")
