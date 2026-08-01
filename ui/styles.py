CSS = """
<style>
    :root {
        --rm-green: #1f6f50;
        --rm-green-soft: #eaf5ef;
        --rm-border: #d7e5dd;
    }
    .block-container {padding-top: 2rem; padding-bottom: 3rem;}
    h1, h2, h3 {color: var(--rm-green);}
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid var(--rm-border);
        border-radius: 12px;
        padding: 12px;
    }
    .rm-card {
        background: var(--rm-green-soft);
        border: 1px solid var(--rm-border);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0 16px 0;
    }
</style>
"""


def aplicar_estilo(st) -> None:
    st.markdown(CSS, unsafe_allow_html=True)
