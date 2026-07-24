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
    def itens(self) -> list[ItemCalculo]:
        return self.imovel.calcular_itens(self.cliente)

    @property
    def aluguel_mensal_centavos(self) -> int:
        return self.imovel.calcular_aluguel_centavos(self.cliente)

    @property
    def total_primeiro_ano_centavos(self) -> int:
        return self.aluguel_mensal_centavos * 12 + self.contrato.valor_total_centavos

    def cronograma(self) -> list[dict[str, int]]:
        cronograma = []
        for numero_mes in range(1, 13):
            contrato_centavos = self.contrato.valor_parcela_no_mes(numero_mes)
            cronograma.append(
                {
                    "numero_mes": numero_mes,
                    "aluguel_centavos": self.aluguel_mensal_centavos,
                    "contrato_centavos": contrato_centavos,
                    "total_mes_centavos": self.aluguel_mensal_centavos + contrato_centavos,
                }
            )
        return cronograma
