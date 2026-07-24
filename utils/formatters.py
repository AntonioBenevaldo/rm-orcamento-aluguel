def moeda_br(valor_centavos: int) -> str:
    """Formata centavos inteiros no padrão monetário brasileiro."""
    sinal = "-" if valor_centavos < 0 else ""
    absoluto = abs(valor_centavos)
    reais, centavos = divmod(absoluto, 100)
    milhares = f"{reais:,}".replace(",", ".")
    return f"{sinal}R$ {milhares},{centavos:02d}"
