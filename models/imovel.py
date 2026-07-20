from abc import ABC, abstractmethod
from dataclasses import dataclass

from .cliente import Cliente


@dataclass(frozen=True)
class ItemCalculo:
    descricao: str
    valor: float
    tipo: str = "acrescimo"


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
    def valor_base(self) -> float: ...

    @abstractmethod
    def calcular_itens(self, cliente: Cliente) -> list[ItemCalculo]: ...

    def calcular_aluguel(self, cliente: Cliente) -> float:
        return round(sum(item.valor for item in self.calcular_itens(cliente)), 2)
