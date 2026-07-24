from dataclasses import dataclass

from utils.constants import CONTRATO_TOTAL_CENTAVOS


@dataclass(frozen=True)
class Contrato:
    quantidade_parcelas: int
    valor_total_centavos: int = CONTRATO_TOTAL_CENTAVOS
    id: int | None = None

    def __post_init__(self) -> None:
        if not 1 <= self.quantidade_parcelas <= 5:
            raise ValueError("O contrato deve ser parcelado entre uma e cinco vezes.")
        if self.valor_total_centavos != CONTRATO_TOTAL_CENTAVOS:
            raise ValueError("O contrato imobiliário deve custar R$ 2.000,00.")

    @property
    def valor_parcela_centavos(self) -> int:
        return self.parcelas_centavos[0]

    @property
    def parcelas_centavos(self) -> tuple[int, ...]:
        """Distribui eventual resto de centavos sem alterar o total do contrato."""
        valor_base, resto = divmod(self.valor_total_centavos, self.quantidade_parcelas)
        return tuple(
            valor_base + (1 if indice < resto else 0)
            for indice in range(self.quantidade_parcelas)
        )

    def valor_parcela_no_mes(self, numero_mes: int) -> int:
        if 1 <= numero_mes <= self.quantidade_parcelas:
            return self.parcelas_centavos[numero_mes - 1]
        return 0
