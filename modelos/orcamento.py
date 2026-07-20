"""Modelos do contrato e do orçamento anual."""

from dataclasses import dataclass

from .cliente import Cliente
from .imovel import Imovel


@dataclass(frozen=True)
class ContratoImobiliario:
    parcelas: int
    valor_total: float = 2000.0

    def __post_init__(self) -> None:
        if not 1 <= self.parcelas <= 5:
            raise ValueError("O contrato pode ser parcelado de 1 a 5 vezes.")

    @property
    def valor_parcela(self) -> float:
        return round(self.valor_total / self.parcelas, 2)


@dataclass
class Orcamento:
    cliente: Cliente
    imovel: Imovel
    contrato: ContratoImobiliario

    @property
    def aluguel_mensal(self) -> float:
        return self.imovel.calcular_aluguel_mensal(self.cliente)

    def gerar_cronograma_12_meses(self) -> list[dict[str, float | int]]:
        return [
            {
                "mes": mes,
                "aluguel_mensal": self.aluguel_mensal,
                "parcela_contrato": self.contrato.valor_parcela if mes <= self.contrato.parcelas else 0.0,
                "total_mes": round(self.aluguel_mensal + (self.contrato.valor_parcela if mes <= self.contrato.parcelas else 0.0), 2),
            }
            for mes in range(1, 13)
        ]

    def total_primeiro_ano(self) -> float:
        return round(sum(item["total_mes"] for item in self.gerar_cronograma_12_meses()), 2)
