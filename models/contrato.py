from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Contrato:
    quantidade_parcelas: int
    valor_total_centavos: int = 200_000

    def __post_init__(self) -> None:
        if not isinstance(self.quantidade_parcelas, int) or isinstance(self.quantidade_parcelas, bool):
            raise ValueError("A quantidade de parcelas deve ser um número inteiro.")
        if not 1 <= self.quantidade_parcelas <= 5:
            raise ValueError("O contrato deve ser parcelado entre uma e cinco vezes.")
        if not isinstance(self.valor_total_centavos, int) or isinstance(self.valor_total_centavos, bool):
            raise ValueError("O valor total do contrato deve ser um número inteiro de centavos.")
        if self.valor_total_centavos <= 0:
            raise ValueError("O valor total do contrato deve ser positivo.")

    @property
    def valores_parcelas_centavos(self) -> list[int]:
        """Distribui eventuais centavos restantes sem alterar o total do contrato."""
        base, resto = divmod(self.valor_total_centavos, self.quantidade_parcelas)
        return [base + (1 if indice < resto else 0) for indice in range(self.quantidade_parcelas)]

    @property
    def valor_parcela_referencia_centavos(self) -> int:
        return self.valores_parcelas_centavos[0]
