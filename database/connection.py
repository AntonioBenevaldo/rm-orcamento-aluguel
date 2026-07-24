import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "imobiliaria.db"
SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def conectar(caminho: str | Path = DB_PATH) -> sqlite3.Connection:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(destino)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.execute("PRAGMA busy_timeout = 5000")
    return conexao


def inicializar_banco(caminho: str | Path = DB_PATH) -> None:
    with conectar(caminho) as conexao:
        conexao.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
