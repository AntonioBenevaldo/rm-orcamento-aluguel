PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL CHECK (length(trim(nome)) > 0),
    possui_criancas INTEGER NOT NULL CHECK (possui_criancas IN (0, 1)),
    criado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS imoveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL CHECK (tipo IN ('Apartamento', 'Casa', 'Estúdio')),
    valor_base_centavos INTEGER NOT NULL CHECK (valor_base_centavos >= 0),
    quantidade_quartos INTEGER NOT NULL CHECK (quantidade_quartos >= 0),
    quantidade_vagas INTEGER NOT NULL CHECK (quantidade_vagas >= 0),
    criado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS contratos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor_total_centavos INTEGER NOT NULL CHECK (valor_total_centavos > 0),
    quantidade_parcelas INTEGER NOT NULL CHECK (quantidade_parcelas BETWEEN 1 AND 5),
    valor_parcela_centavos INTEGER NOT NULL CHECK (valor_parcela_centavos > 0),
    criado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orcamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    imovel_id INTEGER NOT NULL,
    contrato_id INTEGER NOT NULL UNIQUE,
    aluguel_mensal_centavos INTEGER NOT NULL CHECK (aluguel_mensal_centavos >= 0),
    total_primeiro_ano_centavos INTEGER NOT NULL CHECK (total_primeiro_ano_centavos >= 0),
    status TEXT NOT NULL CHECK (status IN ('GERADO', 'CANCELADO')),
    criado_em TEXT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT,
    FOREIGN KEY (imovel_id) REFERENCES imoveis(id) ON DELETE RESTRICT,
    FOREIGN KEY (contrato_id) REFERENCES contratos(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS itens_orcamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orcamento_id INTEGER NOT NULL,
    descricao TEXT NOT NULL CHECK (length(trim(descricao)) > 0),
    tipo TEXT NOT NULL CHECK (tipo IN ('base', 'acrescimo', 'desconto')),
    valor_centavos INTEGER NOT NULL CHECK (valor_centavos >= 0),
    ordem INTEGER NOT NULL CHECK (ordem > 0),
    FOREIGN KEY (orcamento_id) REFERENCES orcamentos(id) ON DELETE CASCADE,
    UNIQUE (orcamento_id, ordem)
);

CREATE TABLE IF NOT EXISTS parcelas_orcamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orcamento_id INTEGER NOT NULL,
    numero_mes INTEGER NOT NULL CHECK (numero_mes BETWEEN 1 AND 12),
    aluguel_centavos INTEGER NOT NULL CHECK (aluguel_centavos >= 0),
    contrato_centavos INTEGER NOT NULL CHECK (contrato_centavos >= 0),
    total_mes_centavos INTEGER NOT NULL CHECK (
        total_mes_centavos >= 0 AND total_mes_centavos = aluguel_centavos + contrato_centavos
    ),
    FOREIGN KEY (orcamento_id) REFERENCES orcamentos(id) ON DELETE CASCADE,
    UNIQUE (orcamento_id, numero_mes)
);

CREATE INDEX IF NOT EXISTS idx_orcamentos_cliente ON orcamentos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_orcamentos_criado_em ON orcamentos(criado_em);
CREATE INDEX IF NOT EXISTS idx_parcelas_orcamento ON parcelas_orcamento(orcamento_id, numero_mes);

CREATE VIEW IF NOT EXISTS vw_orcamentos_resumo AS
SELECT
    o.id,
    o.criado_em,
    o.status,
    c.nome AS cliente,
    c.possui_criancas,
    i.tipo AS tipo_imovel,
    i.quantidade_quartos,
    i.quantidade_vagas,
    ct.quantidade_parcelas,
    o.aluguel_mensal_centavos,
    o.total_primeiro_ano_centavos
FROM orcamentos AS o
JOIN clientes AS c ON c.id = o.cliente_id
JOIN imoveis AS i ON i.id = o.imovel_id
JOIN contratos AS ct ON ct.id = o.contrato_id;
