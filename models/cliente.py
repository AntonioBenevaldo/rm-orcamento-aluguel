from dataclasses import dataclass


@dataclass(frozen=True)
class Cliente:
    nome: str
    possui_criancas: bool
    id: int | None = None

    def __post_init__(self) -> None:
        nome = self.nome.strip()
        if len(nome) < 2:
            raise ValueError("O nome do cliente deve possuir pelo menos dois caracteres.")
        object.__setattr__(self, "nome", nome)
