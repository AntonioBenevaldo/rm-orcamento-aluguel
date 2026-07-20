"""Modelo de cliente."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Cliente:
    nome: str
    possui_criancas: bool

    def __post_init__(self) -> None:
        nome_limpo = self.nome.strip()
        if not nome_limpo:
            raise ValueError("Informe o nome do cliente.")
        object.__setattr__(self, "nome", nome_limpo)
