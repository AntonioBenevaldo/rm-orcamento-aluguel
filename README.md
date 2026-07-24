# Sistema de Orçamento Imobiliário R.M

Aplicação acadêmica em Python com duas formas de execução - Streamlit e
terminal - para calcular, armazenar e exportar orçamentos de apartamentos,
casas e estúdios. As duas interfaces utilizam as mesmas classes, serviços e
banco SQLite.

## Funcionalidades

- Painel com indicadores e histórico recente.
- Aplicação interativa pelo terminal.
- Formulário guiado para apartamento, casa e estúdio.
- Cálculo de quartos, garagem, estacionamento e desconto.
- Contrato de R$ 2.000,00 parcelado em até cinco vezes.
- Cronograma detalhado de 12 meses.
- Persistência transacional em SQLite.
- Consulta de detalhes e exportação CSV individual ou consolidada.
- Testes unitários e de integração do banco físico.
- Valores monetários representados em centavos inteiros do cálculo ao CSV.

## Arquitetura

```text
rm_orcamento_aluguel/
├── app.py                       # Painel principal Streamlit
├── main.py                      # Aplicação interativa no terminal
├── pages/                       # Novo, histórico, detalhes e exportação
├── models/                      # Entidades e regras de domínio
├── services/                    # Cálculo e exportação
├── database/
│   ├── connection.py            # Conexão SQLite
│   ├── queries.py               # Persistência e consultas
│   └── schema.sql               # Modelo físico executável
├── utils/                       # Constantes e formatação
├── data/                        # imobiliaria.db (gerado em execução)
├── tests/                       # Testes automatizados
└── documentos/                 # UML, arquitetura e modelagem de dados
```

## Instalação e execução

Abra o PowerShell na pasta do projeto:

```powershell
cd "C:\Users\Benevaldo\Documents\meus-projetos\rm_orcamento_aluguel"
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

A aplicação abrirá em `http://localhost:8501`.

### Execução pelo terminal

```powershell
python main.py
```

Também é possível clicar duas vezes em `executar_terminal.bat`.

## Testes

```powershell
python -m pytest -q
```

Os 15 testes verificam os três exemplos oficiais, cálculos em centavos,
distribuição exata do contrato, CSV, 12 parcelas, reversão de transações,
chaves estrangeiras, integridade física do SQLite e carregamento da interface.

## Regras de negócio

| Tipo/regra | Valor |
|---|---:|
| Apartamento com um quarto | R$ 700,00 |
| Segundo quarto do apartamento | + R$ 200,00 |
| Casa com um quarto | R$ 900,00 |
| Segundo quarto da casa | + R$ 250,00 |
| Estúdio | R$ 1.200,00 |
| Garagem de casa/apartamento | + R$ 300,00 |
| Duas vagas do estúdio | + R$ 250,00 |
| Vaga adicional do estúdio | + R$ 60,00 |
| Apartamento sem crianças | - 5% |
| Contrato | R$ 2.000,00 em 1 a 5 parcelas |

## Modelo físico

O banco utiliza seis tabelas normalizadas:

```text
clientes ─┐
imoveis  ─┼──< orcamentos ───< itens_orcamento
contratos ┘          └────────< parcelas_orcamento
```

Os valores monetários são gravados como centavos inteiros. O esquema contém `CHECK`, `UNIQUE`, chaves estrangeiras, índices, exclusão em cascata apenas nos detalhes e a visão `vw_orcamentos_resumo`.

O CSV individual possui exatamente 12 registros e as colunas
`numero_mes`, `aluguel_centavos`, `contrato_centavos` e
`total_mes_centavos`. Nenhum valor é recalculado durante a exportação.

- Script físico: [`database/schema.sql`](database/schema.sql)
- Diagrama físico: [`documentos/mod_dados/modelo_fisico.png`](documentos/mod_dados/modelo_fisico.png)
- Fonte PlantUML: [`documentos/mod_dados/modelo_fisico.puml`](documentos/mod_dados/modelo_fisico.puml)
- DBML: [`documentos/mod_dados/modelo_dados.dbml`](documentos/mod_dados/modelo_dados.dbml)

## Diagramas

- Classes completo: `documentos/mod_estatico/diagrama_classes_completo.png`.
- Sequência das camadas: `documentos/mod_dinamico/sequencia_camadas.png`.
- Sequência dos cálculos: `documentos/mod_dinamico/sequencia_calculos.png`.
- Sequência da exportação: `documentos/mod_dinamico/sequencia_exportacao.png`.
- Componentes e implantação: `documentos/arquitetura/`.

Cada diagrama possui versão editável `.puml`, renderização `.png` e versão vetorial `.svg`.

## Orientação a objetos

- **Abstração:** `Imovel` estabelece o contrato comum.
- **Herança:** `Apartamento`, `Casa` e `Estudio` derivam de `Imovel`.
- **Polimorfismo:** cada imóvel calcula seus próprios itens.
- **Encapsulamento:** invariantes são validadas nos modelos.
- **Composição:** `Orcamento` agrega cliente, imóvel, contrato, itens e cronograma.

## Documentação acadêmica

- Modelagem do problema: `documentos/modelagem_problema.md`.
- Arquitetura detalhada: `documentos/arquitetura/arquitetura_software.md`.
- Modelo de dados: `documentos/mod_dados/modelagem_problema.md`.
- Roteiro do pitch: `documentos/roteiro_video_pitch.md`.
