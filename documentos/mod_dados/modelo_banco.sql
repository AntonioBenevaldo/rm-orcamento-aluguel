CREATE TABLE orcamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    possui_criancas INTEGER NOT NULL,
    tipo_imovel TEXT NOT NULL,
    quartos INTEGER NOT NULL,
    vagas INTEGER NOT NULL,
    aluguel_mensal REAL NOT NULL,
    parcelas_contrato INTEGER NOT NULL,
    total_primeiro_ano REAL NOT NULL,
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
