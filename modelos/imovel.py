"""Hierarquia de imóveis e regras de cálculo do aluguel."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from .cliente import Cliente


@dataclass(frozen=True)
class ItemOrcamento:
    descricao: str
    valor: float


@dataclass
class Imovel(ABC):
    quartos: int = 1
    vagas: int = 0

    @property
    @abstractmethod
    def tipo(self) -> str: ...

    @abstractmethod
    def calcular_itens(self, cliente: Cliente) -> list[ItemOrcamento]: ...

    def calcular_aluguel_mensal(self, cliente: Cliente) -> float:
        return round(sum(item.valor for item in self.calcular_itens(cliente)), 2)


@dataclass
class Apartamento(Imovel):
    VALOR_BASE = 700.0
    ACRESCIMO_SEGUNDO_QUARTO = 200.0
    VALOR_GARAGEM = 300.0
    DESCONTO_SEM_CRIANCAS = 0.05

    @property
    def tipo(self) -> str:
        return "Apartamento"

    def __post_init__(self) -> None:
        if self.quartos not in (1, 2):
            raise ValueError("Apartamento permite 1 ou 2 quartos.")
        if self.vagas not in (0, 1):
            raise ValueError("Apartamento permite 0 ou 1 vaga de garagem.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemOrcamento]:
        itens = [ItemOrcamento("Aluguel base - apartamento", self.VALOR_BASE)]
        if self.quartos == 2:
            itens.append(ItemOrcamento("Acréscimo pelo segundo quarto", self.ACRESCIMO_SEGUNDO_QUARTO))
        if self.vagas == 1:
            itens.append(ItemOrcamento("Vaga de garagem", self.VALOR_GARAGEM))
        if not cliente.possui_criancas:
            desconto = round(sum(item.valor for item in itens) * self.DESCONTO_SEM_CRIANCAS, 2)
            itens.append(ItemOrcamento("Desconto de 5% - cliente sem crianças", -desconto))
        return itens


@dataclass
class Casa(Imovel):
    VALOR_BASE = 900.0
    ACRESCIMO_SEGUNDO_QUARTO = 250.0
    VALOR_GARAGEM = 300.0

    @property
    def tipo(self) -> str:
        return "Casa"

    def __post_init__(self) -> None:
        if self.quartos not in (1, 2):
            raise ValueError("Casa permite 1 ou 2 quartos.")
        if self.vagas not in (0, 1):
            raise ValueError("Casa permite 0 ou 1 vaga de garagem.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemOrcamento]:
        itens = [ItemOrcamento("Aluguel base - casa", self.VALOR_BASE)]
        if self.quartos == 2:
            itens.append(ItemOrcamento("Acréscimo pelo segundo quarto", self.ACRESCIMO_SEGUNDO_QUARTO))
        if self.vagas == 1:
            itens.append(ItemOrcamento("Vaga de garagem", self.VALOR_GARAGEM))
        return itens


@dataclass
class Estudio(Imovel):
    VALOR_BASE = 1200.0
    VALOR_DUAS_VAGAS = 250.0
    VALOR_VAGA_ADICIONAL = 60.0

    @property
    def tipo(self) -> str:
        return "Estúdio"

    def __post_init__(self) -> None:
        self.quartos = 1
        if self.vagas not in (0,) and self.vagas < 2:
            raise ValueError("Estúdio permite 0 vagas ou no mínimo 2 vagas.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemOrcamento]:
        itens = [ItemOrcamento("Aluguel base - estúdio", self.VALOR_BASE)]
        if self.vagas >= 2:
            itens.append(ItemOrcamento("Pacote de estacionamento - 2 vagas", self.VALOR_DUAS_VAGAS))
            if self.vagas > 2:
                adicionais = self.vagas - 2
                itens.append(ItemOrcamento(f"{adicionais} vaga(s) adicional(is)", adicionais * self.VALOR_VAGA_ADICIONAL))
        return itens
