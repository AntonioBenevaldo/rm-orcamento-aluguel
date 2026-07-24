from abc import ABC, abstractmethod
from dataclasses import dataclass

from .cliente import Cliente


@dataclass(frozen=True)
class ItemCalculo:
    descricao: str
    valor_centavos: int
    tipo: str = "acrescimo"

    def __post_init__(self) -> None:
        if self.tipo not in {"base", "acrescimo", "desconto"}:
            raise ValueError("Tipo de item de cálculo inválido.")
        if self.tipo == "desconto" and self.valor_centavos >= 0:
            raise ValueError("Um desconto deve possuir valor negativo.")
        if self.tipo != "desconto" and self.valor_centavos < 0:
            raise ValueError("Base e acréscimos não podem ser negativos.")


@dataclass
class Imovel(ABC):
    quartos: int = 1
    vagas: int = 0
    id: int | None = None

    @property
    @abstractmethod
    def tipo(self) -> str: ...

    @property
    @abstractmethod
    def valor_base_centavos(self) -> int: ...

    @abstractmethod
    def calcular_itens(self, cliente: Cliente) -> list[ItemCalculo]: ...

    def calcular_aluguel_centavos(self, cliente: Cliente) -> int:
        return sum(item.valor_centavos for item in self.calcular_itens(cliente))
