import streamlit as st

from ui.styles import aplicar_estilo

st.set_page_config(page_title="Regras e arquitetura | Imobiliária R.M", page_icon="🏗️", layout="wide")
aplicar_estilo(st)

st.title("Regras e arquitetura")

st.subheader("Arquitetura monolítica modular")
st.markdown(
    """
    - **Apresentação:** `app.py` e `pages/`.
    - **Aplicação:** `CalculoService` e `ExportService`.
    - **Domínio:** classes de cliente, imóveis, contrato, itens e orçamento.
    - **Persistência:** repositório e SQLite com transação atômica.
    - **Testes:** regras, banco, integridade, cronograma, CSV e interface.
    """
)

st.subheader("Princípios de orientação a objetos")
st.markdown(
    """
    - **Abstração:** `Imovel` define o comportamento comum.
    - **Herança:** `Apartamento`, `Casa` e `Estudio` derivam de `Imovel`.
    - **Polimorfismo:** cada tipo implementa suas próprias regras de cálculo.
    - **Encapsulamento:** as regras ficam nos modelos e serviços, não na interface.
    - **Composição:** `Orcamento` reúne cliente, imóvel, contrato, itens e cronograma.
    """
)

st.subheader("Integridade")
st.write(
    "Os valores monetários são armazenados em centavos inteiros. O banco utiliza chaves estrangeiras, "
    "restrições CHECK e UNIQUE, índices e transações para impedir registros inválidos ou parciais."
)
