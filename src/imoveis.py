"""Classes de imóveis para o sistema R.M Orçamento de Aluguel.

Este módulo concentra as regras de negócio de cada tipo de locação.
A organização por classes facilita a aplicação dos princípios de
programação orientada a objetos exigidos no trabalho.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


def formatar_moeda(valor: float) -> str:
    """Formata número no padrão monetário brasileiro."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@dataclass
class Cliente:
    """Representa o cliente que solicita o orçamento."""

    nome: str
    possui_criancas: bool


@dataclass
class ItemOrcamento:
    """Item que compõe o cálculo do aluguel mensal."""

    descricao: str
    valor: float


@dataclass
class Imovel(ABC):
    """Classe base abstrata para todos os tipos de imóvel."""

    quartos: int = 1
    vagas: int = 0

    @abstractmethod
    def calcular_itens(self, cliente: Cliente) -> list[ItemOrcamento]:
        """Retorna os itens de cobrança/desconto do aluguel mensal."""

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Nome do tipo de imóvel."""

    def calcular_aluguel_mensal(self, cliente: Cliente) -> float:
        """Soma todos os itens e retorna o valor final do aluguel mensal."""
        total = sum(item.valor for item in self.calcular_itens(cliente))
        return round(total, 2)


@dataclass
class Apartamento(Imovel):
    """Apartamento: R$ 700,00 para 1 quarto.

    Regras adicionais:
    - 2 quartos: acrescenta R$ 200,00.
    - Vaga de garagem: acrescenta R$ 300,00.
    - Cliente sem crianças: desconto de 5% no aluguel de apartamento.
    """

    VALOR_BASE: float = 700.00
    ACRESCIMO_SEGUNDO_QUARTO: float = 200.00
    VALOR_GARAGEM: float = 300.00
    DESCONTO_SEM_CRIANCAS: float = 0.05

    @property
    def tipo(self) -> str:
        return "Apartamento"

    def __post_init__(self) -> None:
        if self.quartos not in (1, 2):
            raise ValueError("Apartamento permite apenas 1 ou 2 quartos.")
        if self.vagas not in (0, 1):
            raise ValueError("Apartamento permite 0 ou 1 vaga de garagem neste orçamento.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemOrcamento]:
        itens = [ItemOrcamento("Aluguel base - apartamento com 1 quarto", self.VALOR_BASE)]

        if self.quartos == 2:
            itens.append(ItemOrcamento("Acréscimo por apartamento com 2 quartos", self.ACRESCIMO_SEGUNDO_QUARTO))

        if self.vagas == 1:
            itens.append(ItemOrcamento("Acréscimo por vaga de garagem", self.VALOR_GARAGEM))

        subtotal = sum(item.valor for item in itens)
        if not cliente.possui_criancas:
            desconto = round(subtotal * self.DESCONTO_SEM_CRIANCAS, 2)
            itens.append(ItemOrcamento("Desconto de 5% para cliente sem crianças", -desconto))

        return itens


@dataclass
class Casa(Imovel):
    """Casa: R$ 900,00 para 1 quarto.

    Regras adicionais:
    - 2 quartos: acrescenta R$ 250,00.
    - Vaga de garagem: acrescenta R$ 300,00.
    """

    VALOR_BASE: float = 900.00
    ACRESCIMO_SEGUNDO_QUARTO: float = 250.00
    VALOR_GARAGEM: float = 300.00

    @property
    def tipo(self) -> str:
        return "Casa"

    def __post_init__(self) -> None:
        if self.quartos not in (1, 2):
            raise ValueError("Casa permite apenas 1 ou 2 quartos.")
        if self.vagas not in (0, 1):
            raise ValueError("Casa permite 0 ou 1 vaga de garagem neste orçamento.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemOrcamento]:
        itens = [ItemOrcamento("Aluguel base - casa com 1 quarto", self.VALOR_BASE)]

        if self.quartos == 2:
            itens.append(ItemOrcamento("Acréscimo por casa com 2 quartos", self.ACRESCIMO_SEGUNDO_QUARTO))

        if self.vagas == 1:
            itens.append(ItemOrcamento("Acréscimo por vaga de garagem", self.VALOR_GARAGEM))

        return itens


@dataclass
class Estudio(Imovel):
    """Estúdio: R$ 1.200,00.

    Regra de estacionamento:
    - 0 vagas: sem acréscimo.
    - 2 vagas: R$ 250,00.
    - Acima de 2 vagas: R$ 250,00 + R$ 60,00 por vaga adicional.
    """

    VALOR_BASE: float = 1200.00
    VALOR_DUAS_VAGAS: float = 250.00
    VALOR_VAGA_ADICIONAL: float = 60.00

    @property
    def tipo(self) -> str:
        return "Estúdio"

    def __post_init__(self) -> None:
        self.quartos = 1
        if self.vagas not in (0, 2) and self.vagas < 3:
            raise ValueError("Estúdio permite 0 vagas ou, no mínimo, 2 vagas de estacionamento.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemOrcamento]:
        itens = [ItemOrcamento("Aluguel base - estúdio", self.VALOR_BASE)]

        if self.vagas >= 2:
            itens.append(ItemOrcamento("Estacionamento do estúdio - pacote com 2 vagas", self.VALOR_DUAS_VAGAS))
            vagas_adicionais = self.vagas - 2
            if vagas_adicionais > 0:
                itens.append(
                    ItemOrcamento(
                        f"{vagas_adicionais} vaga(s) adicional(is) de estacionamento",
                        vagas_adicionais * self.VALOR_VAGA_ADICIONAL,
                    )
                )

        return itens
