import pandas as pd
import streamlit as st

from database import OrcamentoRepository
from services import CalculoService, ExportService
from ui.styles import aplicar_estilo
from utils.money import formatar_brl

st.set_page_config(page_title="Novo orçamento | Imobiliária R.M", page_icon="🧮", layout="wide")
aplicar_estilo(st)

repositorio = OrcamentoRepository()
calculo_service = CalculoService()

st.title("Novo orçamento")
st.caption("Informe somente dados de demonstração. Não utilize dados pessoais reais.")

tipo_imovel = st.selectbox("Tipo de imóvel", ["Apartamento", "Casa", "Estúdio"])

with st.form("form_orcamento", clear_on_submit=False):
    col1, col2 = st.columns(2)
    nome_cliente = col1.text_input(
        "Nome ou identificador do cliente",
        placeholder="Ex.: Cliente 001",
        help="Use um identificador fictício na apresentação acadêmica.",
    )
    possui_criancas_texto = col2.radio(
        "O cliente possui crianças?",
        ["Sim", "Não"],
        horizontal=True,
    )

    col3, col4 = st.columns(2)
    if tipo_imovel in {"Apartamento", "Casa"}:
        quantidade_quartos = col3.selectbox("Quantidade de quartos", [1, 2])
        possui_garagem = col4.checkbox("Possui garagem")
        quantidade_vagas = 1 if possui_garagem else 0
    else:
        quantidade_quartos = 0
        quantidade_vagas = int(
            col3.number_input(
                "Quantidade de vagas",
                min_value=0,
                step=1,
                help="A regra aceita zero vaga ou pelo menos duas vagas.",
            )
        )
        col4.info("Uma vaga isolada não possui preço definido no enunciado.")

    parcelas_contrato = st.slider("Parcelas do contrato de R$ 2.000,00", 1, 5, 5)
    enviar = st.form_submit_button("Calcular e salvar orçamento", type="primary", width="stretch")

if enviar:
    try:
        orcamento = calculo_service.criar_orcamento(
            nome_cliente=nome_cliente,
            possui_criancas=possui_criancas_texto == "Sim",
            tipo_imovel=tipo_imovel,
            quantidade_quartos=quantidade_quartos,
            quantidade_vagas=quantidade_vagas,
            parcelas_contrato=parcelas_contrato,
        )
        orcamento_id = repositorio.salvar(orcamento)
        st.session_state["ultimo_orcamento_id"] = orcamento_id
        st.success(f"Orçamento nº {orcamento_id} calculado e salvo com sucesso.")
    except ValueError as erro:
        st.error(str(erro))
    except Exception:
        st.error("Não foi possível salvar o orçamento. Nenhum registro parcial foi mantido.")

orcamento_id = st.session_state.get("ultimo_orcamento_id")
if orcamento_id:
    dados = repositorio.buscar_por_id(int(orcamento_id))
    if dados:
        resumo = dados["resumo"]
        st.divider()
        st.subheader(f"Resultado do orçamento nº {orcamento_id}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Aluguel mensal", formatar_brl(resumo["aluguel_mensal_centavos"]))
        m2.metric("Contrato", "R$ 2.000,00")
        m3.metric("Total do primeiro ano", formatar_brl(resumo["total_primeiro_ano_centavos"]))

        st.markdown("#### Memória do cálculo")
        itens_exibicao = []
        for item in dados["itens"]:
            sinal = "-" if item["tipo"] == "desconto" else "+"
            itens_exibicao.append(
                {
                    "Ordem": item["ordem"],
                    "Descrição": item["descricao"],
                    "Tipo": item["tipo"].capitalize(),
                    "Efeito": f"{sinal} {formatar_brl(item['valor_centavos'])}",
                }
            )
        st.dataframe(pd.DataFrame(itens_exibicao), hide_index=True, width="stretch")

        st.markdown("#### Cronograma de 12 meses")
        cronograma_exibicao = pd.DataFrame(
            [
                {
                    "Mês": p["numero_mes"],
                    "Aluguel": formatar_brl(p["aluguel_centavos"]),
                    "Contrato": formatar_brl(p["contrato_centavos"]),
                    "Total do mês": formatar_brl(p["total_mes_centavos"]),
                }
                for p in dados["parcelas"]
            ]
        )
        st.dataframe(cronograma_exibicao, hide_index=True, width="stretch")

        csv_bytes = ExportService.gerar_csv_bytes(dados["parcelas"])
        st.download_button(
            "Baixar cronograma CSV",
            data=csv_bytes,
            file_name=f"orcamento_rm_{orcamento_id}_12_meses.csv",
            mime="text/csv",
            width="stretch",
        )
