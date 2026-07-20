# Modelagem de dados e modelo físico

## Modelo conceitual

Um cliente solicita orçamentos. Cada orçamento utiliza um imóvel e possui exatamente um contrato. Para garantir auditoria, o orçamento guarda os itens que formaram o aluguel e as 12 parcelas apresentadas.

## Modelo lógico

- `clientes` 1:N `orcamentos`;
- `imoveis` 1:N `orcamentos`;
- `contratos` 1:1 `orcamentos`;
- `orcamentos` 1:N `itens_orcamento`;
- `orcamentos` 1:N `parcelas_orcamento`.

As tabelas de itens e parcelas são snapshots: se uma constante comercial mudar futuramente, o orçamento antigo continua reproduzível.

## Modelo físico SQLite

O script executável está em `database/schema.sql`. O diagrama editável está em `modelo_fisico.puml` e a representação DBML em `modelo_dados.dbml`.

Decisões importantes:

1. Valores monetários usam `INTEGER` em centavos, não `FLOAT`.
2. `CHECK` limita tipos, status, parcelas, quartos, vagas e meses.
3. Chaves estrangeiras usam `ON DELETE RESTRICT` nas entidades principais e `CASCADE` nos detalhes.
4. Restrições `UNIQUE` impedem mês ou ordem duplicada no mesmo orçamento.
5. Índices aceleram consultas por cliente, data e parcelas.
6. A visão `vw_orcamentos_resumo` simplifica o painel Streamlit.
7. `PRAGMA foreign_keys = ON` garante integridade referencial em cada conexão.

O banco `data/imobiliaria.db` é criado automaticamente e fica fora do Git.
