from dataclasses import dataclass

from utils.constants import APARTAMENTO_BASE, DESCONTO_SEM_CRIANCAS, GARAGEM, SEGUNDO_QUARTO_APARTAMENTO
from .cliente import Cliente
from .imovel import Imovel, ItemCalculo


@dataclass
class Apartamento(Imovel):
    @property
    def tipo(self) -> str: return "apartamento"

    @property
    def valor_base(self) -> float: return APARTAMENTO_BASE

    def __post_init__(self) -> None:
        if self.quartos not in (1, 2): raise ValueError("Apartamento permite um ou dois quartos.")
        if self.vagas not in (0, 1): raise ValueError("Apartamento permite zero ou uma vaga neste orçamento.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemCalculo]:
        itens = [ItemCalculo("Aluguel base do apartamento", self.valor_base, "base")]
        if self.quartos == 2: itens.append(ItemCalculo("Segundo quarto", SEGUNDO_QUARTO_APARTAMENTO))
        if self.vagas == 1: itens.append(ItemCalculo("Garagem", GARAGEM))
        if not cliente.possui_criancas:
            desconto = round(sum(i.valor for i in itens) * DESCONTO_SEM_CRIANCAS, 2)
            itens.append(ItemCalculo("Desconto de 5% - cliente sem crianças", -desconto, "desconto"))
        return itens
