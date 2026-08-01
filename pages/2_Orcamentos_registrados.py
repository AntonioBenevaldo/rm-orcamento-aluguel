import pandas as pd
import streamlit as st

from database import OrcamentoRepository
from services import ExportService
from ui.styles import aplicar_estilo
from utils.money import formatar_brl

st.set_page_config(page_title="Orçamentos registrados | Imobiliária R.M", page_icon="📋", layout="wide")
aplicar_estilo(st)

repositorio = OrcamentoRepository()
registros = repositorio.listar_resumo()

st.title("Orçamentos registrados")

if not registros:
    st.info("Ainda não há orçamentos registrados.")
    st.stop()

filtro_tipo = st.selectbox("Filtrar por tipo de imóvel", ["Todos", "Apartamento", "Casa", "Estúdio"])
filtrados = [r for r in registros if filtro_tipo == "Todos" or r["tipo_imovel"] == filtro_tipo]

resumo_tabela = pd.DataFrame(
    [
        {
            "Nº": r["id"],
            "Data": r["criado_em"].replace("T", " "),
            "Cliente": r["cliente"],
            "Imóvel": r["tipo_imovel"],
            "Aluguel mensal": formatar_brl(r["aluguel_mensal_centavos"]),
            "Total anual": formatar_brl(r["total_primeiro_ano_centavos"]),
            "Status": r["status"],
        }
        for r in filtrados
    ]
)
st.dataframe(resumo_tabela, hide_index=True, width="stretch")

if not filtrados:
    st.warning("Nenhum orçamento corresponde ao filtro selecionado.")
    st.stop()

orcamento_id = st.selectbox(
    "Abrir orçamento",
    options=[r["id"] for r in filtrados],
    format_func=lambda valor: f"Orçamento nº {valor}",
)
dados = repositorio.buscar_por_id(int(orcamento_id))

if dados:
    resumo = dados["resumo"]
    st.subheader(f"Detalhes do orçamento nº {orcamento_id}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Cliente", resumo["cliente"])
    c2.metric("Imóvel", resumo["tipo_imovel"])
    c3.metric("Aluguel mensal", formatar_brl(resumo["aluguel_mensal_centavos"]))
    c4.metric("Total anual", formatar_brl(resumo["total_primeiro_ano_centavos"]))

    st.markdown("#### Itens do cálculo")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Ordem": item["ordem"],
                    "Descrição": item["descricao"],
                    "Tipo": item["tipo"],
                    "Efeito": (
                        f"- {formatar_brl(item['valor_centavos'])}"
                        if item["tipo"] == "desconto"
                        else f"+ {formatar_brl(item['valor_centavos'])}"
                    ),
                }
                for item in dados["itens"]
            ]
        ),
        hide_index=True,
        width="stretch",
    )

    st.markdown("#### Cronograma")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Mês": p["numero_mes"],
                    "Aluguel": formatar_brl(p["aluguel_centavos"]),
                    "Contrato": formatar_brl(p["contrato_centavos"]),
                    "Total": formatar_brl(p["total_mes_centavos"]),
                }
                for p in dados["parcelas"]
            ]
        ),
        hide_index=True,
        width="stretch",
    )

    st.download_button(
        "Baixar CSV deste orçamento",
        data=ExportService.gerar_csv_bytes(dados["parcelas"]),
        file_name=f"orcamento_rm_{orcamento_id}_12_meses.csv",
        mime="text/csv",
        width="stretch",
    )
