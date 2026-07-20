from dataclasses import dataclass

from utils.constants import ESTACIONAMENTO_DUAS_VAGAS, ESTUDIO_BASE, VAGA_ADICIONAL_ESTUDIO
from .cliente import Cliente
from .imovel import Imovel, ItemCalculo


@dataclass
class Estudio(Imovel):
    @property
    def tipo(self) -> str: return "estudio"

    @property
    def valor_base(self) -> float: return ESTUDIO_BASE

    def __post_init__(self) -> None:
        self.quartos = 1
        if self.vagas not in (0,) and self.vagas < 2: raise ValueError("Estúdio permite zero vagas ou, no mínimo, duas vagas.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemCalculo]:
        itens = [ItemCalculo("Aluguel base do estúdio", self.valor_base, "base")]
        if self.vagas >= 2:
            itens.append(ItemCalculo("Estacionamento com duas vagas", ESTACIONAMENTO_DUAS_VAGAS))
            if self.vagas > 2:
                itens.append(ItemCalculo(f"{self.vagas - 2} vaga(s) adicional(is)", (self.vagas - 2) * VAGA_ADICIONAL_ESTUDIO))
        return itens
