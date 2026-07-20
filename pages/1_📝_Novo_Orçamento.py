import pandas as pd
import streamlit as st

from database.connection import inicializar_banco
from database.queries import salvar_orcamento
from services import CalculoService, ExportService
from utils import moeda_br

st.set_page_config(page_title="Novo Orçamento", page_icon="📝", layout="wide")
inicializar_banco()
st.title("📝 Novo orçamento")
st.caption("Preencha os dados; o cálculo será salvo no SQLite e poderá ser exportado em CSV.")

with st.form("novo_orcamento"):
    col_cliente, col_imovel = st.columns(2)
    with col_cliente:
        st.subheader("Cliente")
        nome = st.text_input("Nome completo")
        possui_criancas = st.radio("Possui crianças?", ["Sim", "Não"], horizontal=True) == "Sim"
        parcelas = st.select_slider("Parcelas do contrato de R$ 2.000,00", options=[1, 2, 3, 4, 5], value=5)
    with col_imovel:
        st.subheader("Imóvel")
        tipo = st.selectbox("Tipo", ["Apartamento", "Casa", "Estúdio"])
        if tipo != "Estúdio":
            quartos = st.radio("Quartos", [1, 2], horizontal=True)
            vagas = 1 if st.checkbox("Adicionar garagem (+ R$ 300,00)") else 0
        else:
            quartos = 1
            estacionamento = st.checkbox("Adicionar estacionamento (duas vagas por R$ 250,00)")
            vagas = st.number_input("Quantidade de vagas", min_value=2, max_value=20, value=2, step=1, disabled=not estacionamento) if estacionamento else 0
    calcular = st.form_submit_button("Calcular e salvar orçamento", type="primary", width="stretch")

if calcular:
    try:
        orcamento = CalculoService.processar_orcamento(nome, possui_criancas, tipo, int(quartos), int(vagas), int(parcelas))
        codigo = salvar_orcamento(orcamento)
        st.session_state["ultimo_orcamento"] = orcamento
        st.success(f"Orçamento nº {codigo} salvo com sucesso.")
        a, b, c = st.columns(3)
        a.metric("Aluguel mensal", moeda_br(orcamento.aluguel_mensal))
        b.metric("Parcela do contrato", moeda_br(orcamento.contrato.valor_parcela))
        c.metric("Total no primeiro ano", moeda_br(orcamento.total_primeiro_ano))
        st.subheader("Composição")
        st.dataframe(pd.DataFrame([{"Descrição": i.descricao, "Tipo": i.tipo, "Valor": moeda_br(i.valor)} for i in orcamento.itens]), width="stretch", hide_index=True)
        st.subheader("Cronograma de 12 meses")
        st.dataframe(ExportService.criar_dataframe(orcamento), width="stretch", hide_index=True)
        st.download_button("⬇️ Baixar CSV deste orçamento", ExportService.gerar_csv(orcamento), f"orcamento_rm_{codigo}.csv", "text/csv", width="stretch")
    except ValueError as erro:
        st.error(str(erro))
