from dataclasses import dataclass

from utils.constants import CONTRATO_TOTAL


@dataclass(frozen=True)
class Contrato:
    quantidade_parcelas: int
    valor_total: float = CONTRATO_TOTAL
    id: int | None = None

    def __post_init__(self) -> None:
        if not 1 <= self.quantidade_parcelas <= 5: raise ValueError("O contrato deve ser parcelado entre uma e cinco vezes.")

    @property
    def valor_parcela(self) -> float:
        return round(self.valor_total / self.quantidade_parcelas, 2)
