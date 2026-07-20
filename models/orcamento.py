from dataclasses import dataclass
from datetime import datetime

from .cliente import Cliente
from .contrato import Contrato
from .imovel import Imovel, ItemCalculo


@dataclass
class Orcamento:
    cliente: Cliente
    imovel: Imovel
    contrato: Contrato
    id: int | None = None
    criado_em: datetime | None = None

    @property
    def itens(self) -> list[ItemCalculo]: return self.imovel.calcular_itens(self.cliente)

    @property
    def aluguel_mensal(self) -> float: return self.imovel.calcular_aluguel(self.cliente)

    @property
    def total_primeiro_ano(self) -> float: return round(self.aluguel_mensal * 12 + self.contrato.valor_total, 2)

    def cronograma(self) -> list[dict]:
        return [{"mes": mes, "aluguel": self.aluguel_mensal, "contrato": self.contrato.valor_parcela if mes <= self.contrato.quantidade_parcelas else 0.0, "total": round(self.aluguel_mensal + (self.contrato.valor_parcela if mes <= self.contrato.quantidade_parcelas else 0.0), 2)} for mes in range(1, 13)]
