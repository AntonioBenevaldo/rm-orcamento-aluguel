from dataclasses import dataclass

from utils.constants import CASA_BASE, GARAGEM, SEGUNDO_QUARTO_CASA
from .cliente import Cliente
from .imovel import Imovel, ItemCalculo


@dataclass
class Casa(Imovel):
    @property
    def tipo(self) -> str: return "casa"

    @property
    def valor_base(self) -> float: return CASA_BASE

    def __post_init__(self) -> None:
        if self.quartos not in (1, 2): raise ValueError("Casa permite um ou dois quartos.")
        if self.vagas not in (0, 1): raise ValueError("Casa permite zero ou uma vaga neste orçamento.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemCalculo]:
        itens = [ItemCalculo("Aluguel base da casa", self.valor_base, "base")]
        if self.quartos == 2: itens.append(ItemCalculo("Segundo quarto", SEGUNDO_QUARTO_CASA))
        if self.vagas == 1: itens.append(ItemCalculo("Garagem", GARAGEM))
        return itens
