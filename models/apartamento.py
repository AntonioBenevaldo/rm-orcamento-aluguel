from dataclasses import dataclass

from utils.constants import (
    APARTAMENTO_BASE_CENTAVOS,
    DESCONTO_SEM_CRIANCAS_PERCENTUAL,
    GARAGEM_CENTAVOS,
    SEGUNDO_QUARTO_APARTAMENTO_CENTAVOS,
)
from .cliente import Cliente
from .imovel import Imovel, ItemCalculo


@dataclass
class Apartamento(Imovel):
    @property
    def tipo(self) -> str:
        return "apartamento"

    @property
    def valor_base_centavos(self) -> int:
        return APARTAMENTO_BASE_CENTAVOS

    def __post_init__(self) -> None:
        if self.quartos not in (1, 2):
            raise ValueError("Apartamento permite um ou dois quartos.")
        if self.vagas not in (0, 1):
            raise ValueError("Apartamento permite zero ou uma vaga neste orçamento.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemCalculo]:
        itens = [ItemCalculo("Aluguel base do apartamento", self.valor_base_centavos, "base")]
        if self.quartos == 2:
            itens.append(ItemCalculo("Segundo quarto", SEGUNDO_QUARTO_APARTAMENTO_CENTAVOS))
        if self.vagas == 1:
            itens.append(ItemCalculo("Garagem", GARAGEM_CENTAVOS))
        if not cliente.possui_criancas:
            subtotal = sum(item.valor_centavos for item in itens)
            desconto = subtotal * DESCONTO_SEM_CRIANCAS_PERCENTUAL // 100
            itens.append(ItemCalculo("Desconto de 5% - cliente sem crianças", -desconto, "desconto"))
        return itens
