from dataclasses import dataclass


TIPOS_ITEM = {"base", "acrescimo", "desconto"}


@dataclass(slots=True, frozen=True)
class ItemCalculo:
    descricao: str
    tipo: str
    valor_centavos: int
    ordem: int

    def __post_init__(self) -> None:
        if not isinstance(self.descricao, str):
            raise ValueError("A descrição do item deve ser um texto.")
        if not self.descricao.strip():
            raise ValueError("A descrição do item não pode ser vazia.")
        if self.tipo not in TIPOS_ITEM:
            raise ValueError(f"Tipo de item inválido: {self.tipo}.")
        if self.valor_centavos < 0:
            raise ValueError("O valor do item deve ser não negativo.")
        if self.ordem < 1:
            raise ValueError("A ordem do item deve ser positiva.")

    @property
    def efeito_centavos(self) -> int:
        return -self.valor_centavos if self.tipo == "desconto" else self.valor_centavos
