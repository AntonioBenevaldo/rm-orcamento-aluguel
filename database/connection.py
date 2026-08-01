import sqlite3
from pathlib import Path

from config import DATABASE_PATH


SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def conectar(caminho_banco: str | Path = DATABASE_PATH) -> sqlite3.Connection:
    caminho = Path(caminho_banco)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(caminho)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar_banco(caminho_banco: str | Path = DATABASE_PATH) -> None:
    with conectar(caminho_banco) as conexao:
        conexao.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
