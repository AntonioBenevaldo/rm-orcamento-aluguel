def formatar_brl(centavos: int) -> str:
    """Formata um valor inteiro em centavos no padrão monetário brasileiro."""
    sinal = "-" if centavos < 0 else ""
    valor = abs(centavos) / 100
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sinal}R$ {texto}"
