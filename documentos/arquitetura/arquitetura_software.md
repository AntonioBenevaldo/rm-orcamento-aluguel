# Arquitetura do Software - Sistema de Orçamento Imobiliário R.M

## 1. Visão geral

A solução é um monólito modular executado pelo Streamlit. Embora seja implantada como uma única aplicação, suas responsabilidades são separadas em apresentação, serviços, domínio e persistência.

```text
Usuário → Streamlit → Services → Models → Database/SQLite
                     └──────────→ Exportação/pandas
```

Essa organização permite testar as regras sem abrir o navegador e substituir a interface ou o banco futuramente com menor impacto.

## 2. Tecnologias utilizadas

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Interface | Streamlit ≥ 1.48 | Aplicação web interativa escrita em Python |
| Domínio e serviços | Python ≥ 3.10 | POO, tipagem e biblioteca padrão |
| Persistência | SQLite 3 | Transações ACID e configuração local zero |
| Dados monetários | INTEGER em centavos | Evita imprecisão de ponto flutuante |
| Exportação | pandas + CSV | Tabelas e arquivo interoperável |
| Qualidade | pytest | Testes unitários e de integração |

## 3. Camadas e dependências

- `app.py` e `pages/`: entrada, navegação e componentes visuais.
- `services/`: coordena os casos de uso de cálculo e exportação.
- `models/`: entidades, objetos de valor, herança e regras invariantes.
- `database/`: conexão, esquema físico e consultas transacionais.
- `utils/`: constantes comerciais e formatação.
- `data/`: arquivo físico `imobiliaria.db`, criado em execução.

As páginas podem depender dos serviços e da persistência; os modelos não dependem do Streamlit ou do SQLite.

## 4. Componentes da interface

| Página | Arquivo | Responsabilidade |
|---|---|---|
| Painel | `app.py` | Indicadores e orçamentos recentes |
| Novo orçamento | `pages/1_📝_Novo_Orçamento.py` | Formulário, cálculo, gravação e CSV individual |
| Orçamentos | `pages/2_📋_Orçamentos.py` | Histórico e exportação consolidada |
| Detalhes | `pages/3_📊_Detalhes.py` | Itens e parcelas de um orçamento |
| Exportar | `pages/4_⬇️_Exportar.py` | Central de exportação |

## 5. Decisões arquiteturais

1. **Persistência normalizada:** o orçamento referencia cliente, imóvel e contrato.
2. **Snapshot auditável:** itens e parcelas guardam exatamente os valores apresentados ao cliente.
3. **Dinheiro em centavos:** cálculos persistidos não usam `FLOAT`.
4. **Transação única:** todas as seis tabelas são gravadas juntas ou nenhuma alteração é confirmada.
5. **Integridade:** `CHECK`, `UNIQUE`, chaves estrangeiras e índices protegem os dados.
6. **Compatibilidade:** a versão Flask anterior permanece em `legacy_flask.py`, fora da execução oficial.

## 6. Requisitos não funcionais

| Requisito | Atendimento |
|---|---|
| Manutenibilidade | Camadas e classes pequenas, coesas e testáveis |
| Confiabilidade | Validações no domínio e no banco; transações e testes |
| Usabilidade | Formulário guiado, métricas, mensagens e downloads |
| Segurança local | SQL parametrizado; nenhuma concatenação de entrada em consultas |
| Interoperabilidade | CSV UTF-8 com separador compatível com planilhas brasileiras |
| Desempenho | Índices de cliente, data e parcelas; adequado ao escopo acadêmico |

## 7. Implantação

Execução local:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

No Streamlit Community Cloud, o repositório deve conter `app.py` e `requirements.txt`. Como o SQLite no serviço pode ser efêmero, a implantação acadêmica serve para demonstração; uma evolução produtiva usaria PostgreSQL ou armazenamento persistente externo.
