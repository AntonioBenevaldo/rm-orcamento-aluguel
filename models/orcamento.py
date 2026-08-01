from dataclasses import dataclass
from datetime import datetime

from .cliente import Cliente
from .contrato import Contrato
from .imovel import Imovel
from .item_calculo import ItemCalculo


@dataclass(slots=True, frozen=True)
class ParcelaOrcamento:
    numero_mes: int
    aluguel_centavos: int
    contrato_centavos: int
    total_mes_centavos: int

    def __post_init__(self) -> None:
        if not 1 <= self.numero_mes <= 12:
            raise ValueError("O número do mês deve estar entre 1 e 12.")
        if min(self.aluguel_centavos, self.contrato_centavos, self.total_mes_centavos) < 0:
            raise ValueError("Os valores mensais não podem ser negativos.")
        if self.total_mes_centavos != self.aluguel_centavos + self.contrato_centavos:
            raise ValueError("O total do mês deve ser a soma do aluguel com o contrato.")


@dataclass(slots=True)
class Orcamento:
    cliente: Cliente
    imovel: Imovel
    contrato: Contrato
    itens: list[ItemCalculo]
    parcelas: list[ParcelaOrcamento]
    aluguel_mensal_centavos: int
    total_primeiro_ano_centavos: int
    status: str = "GERADO"
    criado_em: str = ""
    id: int | None = None

    def __post_init__(self) -> None:
        if not self.criado_em:
            self.criado_em = datetime.now().isoformat(timespec="seconds")
        if self.status not in {"GERADO", "CANCELADO"}:
            raise ValueError("Status de orçamento inválido.")
        if len(self.parcelas) != 12:
            raise ValueError("O orçamento deve possuir exatamente 12 parcelas mensais.")
        if [parcela.numero_mes for parcela in self.parcelas] != list(range(1, 13)):
            raise ValueError("O cronograma deve conter os meses de 1 a 12, sem duplicidades.")
        if self.aluguel_mensal_centavos < 0 or self.total_primeiro_ano_centavos < 0:
            raise ValueError("Os totais do orçamento não podem ser negativos.")
        if sum(item.efeito_centavos for item in self.itens) != self.aluguel_mensal_centavos:
            raise ValueError("A memória de cálculo não corresponde ao aluguel mensal.")
        if sum(parcela.contrato_centavos for parcela in self.parcelas) != self.contrato.valor_total_centavos:
            raise ValueError("O cronograma não preserva o valor total do contrato.")
        if sum(parcela.total_mes_centavos for parcela in self.parcelas) != self.total_primeiro_ano_centavos:
            raise ValueError("O cronograma não corresponde ao total do primeiro ano.")
