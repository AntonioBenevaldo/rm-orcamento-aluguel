# Dicionário de dados - Modelo físico SQLite

## `clientes`

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT | Identificador do cliente registrado na solicitação |
| nome | TEXT | NOT NULL, comprimento ≥ 2 | Nome informado |
| possui_criancas | INTEGER | NOT NULL, CHECK 0/1 | Booleano compatível com SQLite |
| criado_em | TEXT | NOT NULL, DEFAULT | Data/hora ISO gerada pelo SQLite |

## `imoveis`

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | INTEGER | PK, AUTOINCREMENT | Identificador do imóvel orçado |
| tipo | TEXT | CHECK | `apartamento`, `casa` ou `estudio` |
| valor_base_centavos | INTEGER | > 0 | Valor base congelado no momento do orçamento |
| quantidade_quartos | INTEGER | 1 a 2 | Quantidade usada no cálculo |
| quantidade_vagas | INTEGER | ≥ 0 | Garagem ou estacionamento |
| criado_em | TEXT | DEFAULT | Data de criação |

## `contratos`

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | INTEGER | PK | Identificador do contrato |
| valor_total_centavos | INTEGER | CHECK = 200000 | Contrato fixo de R$ 2.000,00 |
| quantidade_parcelas | INTEGER | 1 a 5 | Parcelamento escolhido |
| valor_parcela_centavos | INTEGER | > 0 | Parcela calculada |
| criado_em | TEXT | DEFAULT | Data de criação |

## `orcamentos`

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | INTEGER | PK | Identificador principal |
| cliente_id | INTEGER | FK, NOT NULL | Referência ao cliente |
| imovel_id | INTEGER | FK, NOT NULL | Referência ao imóvel |
| contrato_id | INTEGER | FK, NOT NULL, UNIQUE | Relação 1:1 com o contrato |
| aluguel_mensal_centavos | INTEGER | > 0 | Valor final após acréscimos/desconto |
| total_primeiro_ano_centavos | INTEGER | > 0 | 12 aluguéis + contrato |
| status | TEXT | CHECK | `gerado`, `aprovado` ou `cancelado` |
| criado_em | TEXT | DEFAULT | Data de geração |

## `itens_orcamento`

Guarda a memória de cálculo. A combinação `(orcamento_id, ordem)` é única.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | INTEGER | PK | Identificador do item |
| orcamento_id | INTEGER | FK, CASCADE | Orçamento proprietário |
| descricao | TEXT | NOT NULL | Nome apresentado na composição |
| tipo | TEXT | CHECK | `base`, `acrescimo` ou `desconto` |
| valor_centavos | INTEGER | permite negativo | Desconto é representado por valor negativo |
| ordem | INTEGER | > 0, UNIQUE composto | Posição de exibição |

## `parcelas_orcamento`

Guarda os doze meses exigidos. A combinação `(orcamento_id, numero_mes)` é única.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id | INTEGER | PK | Identificador da linha |
| orcamento_id | INTEGER | FK, CASCADE | Orçamento proprietário |
| numero_mes | INTEGER | 1 a 12 | Mês do cronograma |
| aluguel_centavos | INTEGER | > 0 | Aluguel mensal |
| contrato_centavos | INTEGER | ≥ 0 | Parcela enquanto aplicável |
| total_mes_centavos | INTEGER | > 0 | Aluguel + parcela |

## Objetos auxiliares

- `idx_orcamentos_cliente`: acelera histórico por cliente.
- `idx_orcamentos_criado_em`: acelera ordenação cronológica.
- `idx_parcelas_orcamento`: acelera detalhes do cronograma.
- `vw_orcamentos_resumo`: converte centavos para reais e reúne dados para o painel.
