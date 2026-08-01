from abc import ABC, abstractmethod

from .cliente import Cliente
from .item_calculo import ItemCalculo


class Imovel(ABC):
    tipo: str
    valor_base_centavos: int

    def __init__(self, quantidade_quartos: int, quantidade_vagas: int) -> None:
        if not isinstance(quantidade_quartos, int) or isinstance(quantidade_quartos, bool):
            raise ValueError("A quantidade de quartos deve ser um número inteiro.")
        if not isinstance(quantidade_vagas, int) or isinstance(quantidade_vagas, bool):
            raise ValueError("A quantidade de vagas deve ser um número inteiro.")
        self.quantidade_quartos = quantidade_quartos
        self.quantidade_vagas = quantidade_vagas
        self.validar()

    @abstractmethod
    def validar(self) -> None:
        """Valida as combinações permitidas para o imóvel."""

    @abstractmethod
    def calcular_itens(self, cliente: Cliente) -> list[ItemCalculo]:
        """Retorna a memória detalhada do cálculo do aluguel."""

    def calcular_aluguel_centavos(self, cliente: Cliente) -> tuple[int, list[ItemCalculo]]:
        itens = self.calcular_itens(cliente)
        total = sum(item.efeito_centavos for item in itens)
        if total < 0:
            raise ValueError("O aluguel calculado não pode ser negativo.")
        return total, itens


class Apartamento(Imovel):
    tipo = "Apartamento"
    valor_base_centavos = 70_000

    def validar(self) -> None:
        if self.quantidade_quartos not in {1, 2}:
            raise ValueError("Apartamento deve possuir um ou dois quartos.")
        if self.quantidade_vagas not in {0, 1}:
            raise ValueError("Apartamento deve possuir zero ou uma vaga de garagem.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemCalculo]:
        itens = [ItemCalculo("Aluguel-base do apartamento", "base", self.valor_base_centavos, 1)]
        ordem = 2
        if self.quantidade_quartos == 2:
            itens.append(ItemCalculo("Acréscimo pelo segundo quarto", "acrescimo", 20_000, ordem))
            ordem += 1
        if self.quantidade_vagas == 1:
            itens.append(ItemCalculo("Acréscimo pela garagem", "acrescimo", 30_000, ordem))
            ordem += 1

        subtotal = sum(item.efeito_centavos for item in itens)
        if not cliente.possui_criancas:
            desconto = subtotal * 5 // 100
            itens.append(ItemCalculo("Desconto de 5% para cliente sem crianças", "desconto", desconto, ordem))
        return itens


class Casa(Imovel):
    tipo = "Casa"
    valor_base_centavos = 90_000

    def validar(self) -> None:
        if self.quantidade_quartos not in {1, 2}:
            raise ValueError("Casa deve possuir um ou dois quartos.")
        if self.quantidade_vagas not in {0, 1}:
            raise ValueError("Casa deve possuir zero ou uma vaga de garagem.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemCalculo]:
        itens = [ItemCalculo("Aluguel-base da casa", "base", self.valor_base_centavos, 1)]
        ordem = 2
        if self.quantidade_quartos == 2:
            itens.append(ItemCalculo("Acréscimo pelo segundo quarto", "acrescimo", 25_000, ordem))
            ordem += 1
        if self.quantidade_vagas == 1:
            itens.append(ItemCalculo("Acréscimo pela garagem", "acrescimo", 30_000, ordem))
        return itens


class Estudio(Imovel):
    tipo = "Estúdio"
    valor_base_centavos = 120_000

    def __init__(self, quantidade_vagas: int) -> None:
        super().__init__(quantidade_quartos=0, quantidade_vagas=quantidade_vagas)

    def validar(self) -> None:
        if self.quantidade_vagas < 0:
            raise ValueError("A quantidade de vagas não pode ser negativa.")
        if self.quantidade_vagas == 1:
            raise ValueError("Para estúdio, informe zero vaga ou pelo menos duas vagas.")

    def calcular_itens(self, cliente: Cliente) -> list[ItemCalculo]:
        itens = [ItemCalculo("Aluguel-base do estúdio", "base", self.valor_base_centavos, 1)]
        if self.quantidade_vagas >= 2:
            itens.append(ItemCalculo("Pacote das duas primeiras vagas", "acrescimo", 25_000, 2))
            vagas_adicionais = self.quantidade_vagas - 2
            if vagas_adicionais:
                itens.append(
                    ItemCalculo(
                        f"{vagas_adicionais} vaga(s) adicional(is) a R$ 60,00",
                        "acrescimo",
                        vagas_adicionais * 6_000,
                        3,
                    )
                )
        return itens
