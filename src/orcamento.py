"""Geração de orçamento e cronograma de 12 parcelas."""

from __future__ import annotations

from dataclasses import dataclass

from imoveis import Cliente, Imovel, formatar_moeda


@dataclass
class ContratoImobiliario:
    """Contrato imobiliário de R$ 2.000,00 parcelável em até 5 vezes."""

    parcelas: int
    valor_total: float = 2000.00

    def __post_init__(self) -> None:
        if not 1 <= self.parcelas <= 5:
            raise ValueError("O contrato pode ser parcelado de 1 até 5 vezes.")

    @property
    def valor_parcela(self) -> float:
        return round(self.valor_total / self.parcelas, 2)


@dataclass
class Orcamento:
    """Orçamento completo do aluguel."""

    cliente: Cliente
    imovel: Imovel
    contrato: ContratoImobiliario

    @property
    def aluguel_mensal(self) -> float:
        return self.imovel.calcular_aluguel_mensal(self.cliente)

    def gerar_cronograma_12_meses(self) -> list[dict[str, float | int]]:
        """Gera 12 meses de cobrança, incluindo contrato nos primeiros meses."""
        cronograma = []
        for mes in range(1, 13):
            parcela_contrato = self.contrato.valor_parcela if mes <= self.contrato.parcelas else 0.00
            total_mes = round(self.aluguel_mensal + parcela_contrato, 2)
            cronograma.append(
                {
                    "mes": mes,
                    "aluguel_mensal": self.aluguel_mensal,
                    "parcela_contrato": parcela_contrato,
                    "total_mes": total_mes,
                }
            )
        return cronograma

    def total_primeiro_ano(self) -> float:
        """Soma aluguel de 12 meses + contrato imobiliário."""
        return round(sum(linha["total_mes"] for linha in self.gerar_cronograma_12_meses()), 2)

    def resumo_texto(self) -> str:
        """Monta um resumo textual do orçamento."""
        linhas = []
        linhas.append("=" * 68)
        linhas.append("ORÇAMENTO DE ALUGUEL - IMOBILIÁRIA R.M")
        linhas.append("=" * 68)
        linhas.append(f"Cliente: {self.cliente.nome}")
        linhas.append(f"Tipo de imóvel: {self.imovel.tipo}")
        linhas.append(f"Quartos: {self.imovel.quartos}")
        linhas.append(f"Vagas: {self.imovel.vagas}")
        linhas.append(f"Possui crianças: {'Sim' if self.cliente.possui_criancas else 'Não'}")
        linhas.append("-" * 68)
        linhas.append("Composição do aluguel mensal:")
        for item in self.imovel.calcular_itens(self.cliente):
            linhas.append(f"  - {item.descricao}: {formatar_moeda(item.valor)}")
        linhas.append("-" * 68)
        linhas.append(f"Valor final do aluguel mensal: {formatar_moeda(self.aluguel_mensal)}")
        linhas.append(
            f"Contrato imobiliário: {formatar_moeda(self.contrato.valor_total)} "
            f"em {self.contrato.parcelas} parcela(s) de {formatar_moeda(self.contrato.valor_parcela)}"
        )
        linhas.append(f"Total estimado no primeiro ano: {formatar_moeda(self.total_primeiro_ano())}")
        linhas.append("=" * 68)
        return "\n".join(linhas)
