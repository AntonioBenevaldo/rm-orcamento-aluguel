from dataclasses import dataclass

from utils.constants import (
    ESTACIONAMENTO_DUAS_VAGAS_CENTAVOS,
    ESTUDIO_BASE_CENTAVOS,
    VAGA_ADICIONAL_ESTUDIO_CENTAVOS,
)
from .cliente import Cliente
from .imovel import Imovel, ItemCalculo


@dataclass
class Estudio(Imovel):
    @property
    def tipo(self) -> str:
        return "estudio"

    @property
    def valor_base_centavos(self) -> int:
        return ESTUDIO_BASE_CENTAVOS

    def __post_init__(self) -> None:
        self.quartos = 1
        if self.vagas != 0 and self.vagas < 2:
            raise ValueError("Estúdio permite zero vagas ou, no mínimo, duas vagas.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemCalculo]:
        itens = [ItemCalculo("Aluguel base do estúdio", self.valor_base_centavos, "base")]
        if self.vagas >= 2:
            itens.append(ItemCalculo("Estacionamento com duas vagas", ESTACIONAMENTO_DUAS_VAGAS_CENTAVOS))
            if self.vagas > 2:
                itens.append(
                    ItemCalculo(
                        f"{self.vagas - 2} vaga(s) adicional(is)",
                        (self.vagas - 2) * VAGA_ADICIONAL_ESTUDIO_CENTAVOS,
                    )
                )
        return itens
