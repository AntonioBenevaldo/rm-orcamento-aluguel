import streamlit as st

from database import OrcamentoRepository
from ui.styles import aplicar_estilo
from utils.money import formatar_brl

st.set_page_config(
    page_title="Sistema de Orçamento Imobiliário R.M",
    page_icon="🏠",
    layout="wide",
)
aplicar_estilo(st)

repositorio = OrcamentoRepository()
estatisticas = repositorio.estatisticas()

st.title("Sistema de Orçamento Imobiliário R.M")
st.caption("Pensamento algorítmico, orientação a objetos e persistência SQLite")

st.markdown(
    """
    <div class="rm-card">
    A aplicação calcula orçamentos mensais para apartamentos, casas e estúdios, registra cada
    orçamento em banco SQLite e disponibiliza um cronograma financeiro de 12 meses em CSV.
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
col1.metric("Orçamentos registrados", int(estatisticas["quantidade"]))
col2.metric("Aluguel médio", formatar_brl(round(estatisticas["media_aluguel_centavos"])))
col3.metric("Total anual orçado", formatar_brl(int(estatisticas["total_primeiro_ano_centavos"])))

st.subheader("Como utilizar")
st.write(
    "Acesse **Novo orçamento** no menu lateral para informar os dados, calcular, salvar e exportar. "
    "Use **Orçamentos registrados** para consultar o histórico e baixar novamente o CSV."
)

st.subheader("Regras principais")
st.markdown(
    """
    - Apartamento: R$ 700,00; segundo quarto + R$ 200,00; garagem + R$ 300,00; desconto de 5% sem crianças.
    - Casa: R$ 900,00; segundo quarto + R$ 250,00; garagem + R$ 300,00.
    - Estúdio: R$ 1.200,00; duas primeiras vagas + R$ 250,00; vagas adicionais + R$ 60,00 cada.
    - Contrato imobiliário: R$ 2.000,00, parcelável entre uma e cinco vezes.
    """
)
