from models import Apartamento, Casa, Cliente, Contrato, Estudio, Orcamento


class CalculoService:
    """Caso de uso central; transforma entradas validadas em um orçamento."""

    @staticmethod
    def processar_orcamento(nome: str, possui_criancas: bool, tipo_imovel: str,
                            quartos: int, vagas: int, parcelas: int) -> Orcamento:
        cliente = Cliente(nome, possui_criancas)
        tipo = tipo_imovel.strip().lower()
        if tipo == "apartamento":
            imovel = Apartamento(quartos=quartos, vagas=vagas)
        elif tipo == "casa":
            imovel = Casa(quartos=quartos, vagas=vagas)
        elif tipo in {"estudio", "estúdio"}:
            imovel = Estudio(vagas=vagas)
        else:
            raise ValueError("Tipo de imóvel inválido.")
        return Orcamento(cliente, imovel, Contrato(parcelas))
