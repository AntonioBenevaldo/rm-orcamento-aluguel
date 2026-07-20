def formatar_moeda(valor: float) -> str:
    """Formata um número no padrão monetário brasileiro."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
