"""Serviço responsável por validar entradas e montar um orçamento."""

from modelos import Apartamento, Casa, Cliente, ContratoImobiliario, Estudio, Orcamento


class OrcamentoService:
    @staticmethod
    def criar(dados: dict) -> Orcamento:
        cliente = Cliente(str(dados.get("nome_cliente", "")), OrcamentoService._booleano(dados.get("possui_criancas")))
        tipo = str(dados.get("tipo_imovel", "")).strip().lower()

        if tipo in {"apartamento", "casa"}:
            quartos = int(dados.get("quartos", 1))
            vagas = 1 if OrcamentoService._booleano(dados.get("garagem")) else 0
            imovel = Apartamento(quartos, vagas) if tipo == "apartamento" else Casa(quartos, vagas)
        elif tipo in {"estudio", "estúdio"}:
            possui_estacionamento = OrcamentoService._booleano(dados.get("estacionamento_estudio"))
            vagas = int(dados.get("vagas_estudio") or 0) if possui_estacionamento else 0
            imovel = Estudio(vagas=vagas)
        else:
            raise ValueError("Escolha apartamento, casa ou estúdio.")

        contrato = ContratoImobiliario(int(dados.get("parcelas_contrato", 1)))
        return Orcamento(cliente, imovel, contrato)

    @staticmethod
    def _booleano(valor: object) -> bool:
        return str(valor).strip().lower() in {"s", "sim", "true", "1", "on"}
