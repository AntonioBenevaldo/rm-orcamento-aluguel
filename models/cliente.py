from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Cliente:
    nome: str
    possui_criancas: bool

    def __post_init__(self) -> None:
        if not isinstance(self.nome, str):
            raise ValueError("O nome ou identificador do cliente deve ser um texto.")
        nome_limpo = self.nome.strip()
        if not nome_limpo:
            raise ValueError("Informe um nome ou identificador para o cliente.")
        if not isinstance(self.possui_criancas, bool):
            raise ValueError("A informação sobre crianças deve ser verdadeira ou falsa.")
        object.__setattr__(self, "nome", nome_limpo)
