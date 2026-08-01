from models import Apartamento, Casa, Cliente, Contrato, Estudio, Orcamento, ParcelaOrcamento


class CalculoService:
    TIPOS_PERMITIDOS = {"Apartamento", "Casa", "Estúdio", "Estudio"}

    def criar_orcamento(
        self,
        *,
        nome_cliente: str,
        possui_criancas: bool,
        tipo_imovel: str,
        quantidade_quartos: int,
        quantidade_vagas: int,
        parcelas_contrato: int,
    ) -> Orcamento:
        cliente = Cliente(nome_cliente, possui_criancas)
        imovel = self._criar_imovel(tipo_imovel, quantidade_quartos, quantidade_vagas)
        contrato = Contrato(parcelas_contrato)

        aluguel_centavos, itens = imovel.calcular_aluguel_centavos(cliente)
        parcelas = self._montar_cronograma(aluguel_centavos, contrato)
        total_primeiro_ano = sum(parcela.total_mes_centavos for parcela in parcelas)

        return Orcamento(
            cliente=cliente,
            imovel=imovel,
            contrato=contrato,
            itens=itens,
            parcelas=parcelas,
            aluguel_mensal_centavos=aluguel_centavos,
            total_primeiro_ano_centavos=total_primeiro_ano,
        )

    @staticmethod
    def _criar_imovel(tipo: str, quartos: int, vagas: int):
        if not isinstance(tipo, str):
            raise ValueError("Selecione apartamento, casa ou estúdio.")
        tipo_normalizado = tipo.strip().lower()
        if tipo_normalizado == "apartamento":
            return Apartamento(quartos, vagas)
        if tipo_normalizado == "casa":
            return Casa(quartos, vagas)
        if tipo_normalizado in {"estúdio", "estudio"}:
            return Estudio(vagas)
        raise ValueError("Selecione apartamento, casa ou estúdio.")

    @staticmethod
    def _montar_cronograma(aluguel_centavos: int, contrato: Contrato) -> list[ParcelaOrcamento]:
        parcelas_contrato = contrato.valores_parcelas_centavos
        cronograma: list[ParcelaOrcamento] = []
        for numero_mes in range(1, 13):
            contrato_mes = parcelas_contrato[numero_mes - 1] if numero_mes <= len(parcelas_contrato) else 0
            cronograma.append(
                ParcelaOrcamento(
                    numero_mes=numero_mes,
                    aluguel_centavos=aluguel_centavos,
                    contrato_centavos=contrato_mes,
                    total_mes_centavos=aluguel_centavos + contrato_mes,
                )
            )
        return cronograma
