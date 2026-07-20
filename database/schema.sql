PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL CHECK (length(trim(nome)) >= 2),
    possui_criancas INTEGER NOT NULL CHECK (possui_criancas IN (0, 1)),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS imoveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL CHECK (tipo IN ('apartamento', 'casa', 'estudio')),
    valor_base_centavos INTEGER NOT NULL CHECK (valor_base_centavos > 0),
    quantidade_quartos INTEGER NOT NULL CHECK (quantidade_quartos BETWEEN 1 AND 2),
    quantidade_vagas INTEGER NOT NULL DEFAULT 0 CHECK (quantidade_vagas >= 0),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contratos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor_total_centavos INTEGER NOT NULL DEFAULT 200000 CHECK (valor_total_centavos = 200000),
    quantidade_parcelas INTEGER NOT NULL CHECK (quantidade_parcelas BETWEEN 1 AND 5),
    valor_parcela_centavos INTEGER NOT NULL CHECK (valor_parcela_centavos > 0),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orcamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    imovel_id INTEGER NOT NULL,
    contrato_id INTEGER NOT NULL UNIQUE,
    aluguel_mensal_centavos INTEGER NOT NULL CHECK (aluguel_mensal_centavos > 0),
    total_primeiro_ano_centavos INTEGER NOT NULL CHECK (total_primeiro_ano_centavos > 0),
    status TEXT NOT NULL DEFAULT 'gerado' CHECK (status IN ('gerado', 'aprovado', 'cancelado')),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (imovel_id) REFERENCES imoveis(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (contrato_id) REFERENCES contratos(id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS itens_orcamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orcamento_id INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('base', 'acrescimo', 'desconto')),
    valor_centavos INTEGER NOT NULL,
    ordem INTEGER NOT NULL CHECK (ordem > 0),
    FOREIGN KEY (orcamento_id) REFERENCES orcamentos(id) ON DELETE CASCADE,
    UNIQUE (orcamento_id, ordem)
);

CREATE TABLE IF NOT EXISTS parcelas_orcamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orcamento_id INTEGER NOT NULL,
    numero_mes INTEGER NOT NULL CHECK (numero_mes BETWEEN 1 AND 12),
    aluguel_centavos INTEGER NOT NULL CHECK (aluguel_centavos > 0),
    contrato_centavos INTEGER NOT NULL DEFAULT 0 CHECK (contrato_centavos >= 0),
    total_mes_centavos INTEGER NOT NULL CHECK (total_mes_centavos > 0),
    FOREIGN KEY (orcamento_id) REFERENCES orcamentos(id) ON DELETE CASCADE,
    UNIQUE (orcamento_id, numero_mes)
);

CREATE INDEX IF NOT EXISTS idx_orcamentos_cliente ON orcamentos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_orcamentos_criado_em ON orcamentos(criado_em);
CREATE INDEX IF NOT EXISTS idx_parcelas_orcamento ON parcelas_orcamento(orcamento_id);

CREATE VIEW IF NOT EXISTS vw_orcamentos_resumo AS
SELECT o.id, c.nome AS cliente, i.tipo AS imovel,
       o.aluguel_mensal_centavos / 100.0 AS aluguel_mensal,
       ct.quantidade_parcelas AS parcelas_contrato,
       o.total_primeiro_ano_centavos / 100.0 AS total_primeiro_ano,
       o.status, o.criado_em
FROM orcamentos o
JOIN clientes c ON c.id = o.cliente_id
JOIN imoveis i ON i.id = o.imovel_id
JOIN contratos ct ON ct.id = o.contrato_id;

PRAGMA user_version = 1;
