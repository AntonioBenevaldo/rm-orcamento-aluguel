# Orçamento de Aluguel - Imobiliária R.M

Projeto desenvolvido para a disciplina **Algorithmic Thinking & Introduction to Object-Oriented Programming**.

A aplicação gera orçamento mensal de aluguel para **apartamentos**, **casas** e **estúdios**, calcula o contrato imobiliário de **R$ 2.000,00** parcelado em até **5 vezes** e permite exportar um arquivo **CSV com as 12 parcelas** do orçamento.

Esta versão possui duas formas de execução:

1. **Aplicação via terminal**, usando Python puro.
2. **Interface web**, usando Python, Flask, HTML, CSS e JavaScript.

---

## Funcionalidades

- Cadastro simples do cliente.
- Escolha do tipo de imóvel: apartamento, casa ou estúdio.
- Cálculo automático do aluguel mensal conforme as regras de negócio.
- Acréscimo por segundo quarto em apartamento ou casa.
- Acréscimo por garagem em apartamento ou casa.
- Acréscimo por estacionamento em estúdio.
- Desconto de 5% para apartamento quando o cliente não possui crianças.
- Cálculo do contrato imobiliário de R$ 2.000,00 em até 5 parcelas.
- Geração de arquivo `.csv` com 12 meses de orçamento.
- Interface web com arquivos HTML/CSS.

---

## Estrutura do projeto

```text
rm_orcamento_aluguel/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── imoveis.py
│   ├── orcamento.py
│   └── csv_exporter.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── resultado.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── formulario.js
│
├── docs/
│   ├── fluxograma.png
│   ├── fluxograma.mmd
│   ├── fluxograma.dot
│   ├── pseudocodigo.txt
│   ├── instrucoes_interface_web.txt
│   ├── roteiro_video_pitch.txt
│   └── roteiro_video_pitch_interface_web.txt
│
├── exemplos/
│   └── orcamento_exemplo.csv
│
├── saida_csv/
│   └── arquivos CSV gerados pela interface web
│
├── web_app.py
├── requirements.txt
└── README.md
```

---

## Como executar pelo terminal

Abra o terminal dentro da pasta `src`:

```bash
cd src
python main.py
```

No Windows, caso `python` não funcione, tente:

```bash
py main.py
```

Depois responda às perguntas exibidas no terminal.

---

## Como executar a interface web

Abra o terminal na pasta raiz do projeto:

```bash
cd rm_orcamento_aluguel
```

Crie um ambiente virtual, se desejar:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação web:

```bash
python web_app.py
```

Depois abra no navegador:

```text
http://127.0.0.1:5000
```

---

## Exemplo de teste

Use estes dados na interface web ou no terminal:

```text
Cliente: João
Possui crianças: Não
Tipo de imóvel: Apartamento
Quartos: 2
Garagem: Sim
Parcelas do contrato: 5
```

Resultado esperado:

```text
Apartamento com 1 quarto: R$ 700,00
Acréscimo por 2 quartos: R$ 200,00
Garagem: R$ 300,00
Subtotal: R$ 1.200,00
Desconto de 5%: R$ 60,00
Aluguel mensal final: R$ 1.140,00
Contrato: R$ 2.000,00 em 5 parcelas de R$ 400,00
Total estimado no primeiro ano: R$ 15.680,00
```

---

## Orientação a objetos aplicada

O projeto usa classes para separar responsabilidades:

- `Cliente`: armazena os dados do cliente.
- `ItemOrcamento`: representa cada item de cobrança ou desconto.
- `Imovel`: classe abstrata base para os tipos de imóveis.
- `Apartamento`, `Casa` e `Estudio`: especializam as regras de cálculo de cada imóvel.
- `ContratoImobiliario`: calcula o valor do contrato e suas parcelas.
- `Orcamento`: reúne cliente, imóvel e contrato para gerar o orçamento completo.
- `ExportadorCSV`: salva o cronograma de 12 meses em CSV.

Essa organização demonstra os princípios de orientação a objetos, como abstração, especialização por classes e separação de responsabilidades.

---

## Parte HTML/CSS

A interface web foi criada para agregar uma camada visual ao projeto.

Arquivos principais:

- `templates/base.html`: estrutura comum das páginas.
- `templates/index.html`: formulário de entrada dos dados.
- `templates/resultado.html`: tela com resultado, tabela de cálculo e botão para baixar CSV.
- `static/css/style.css`: estilos visuais da aplicação.
- `static/js/formulario.js`: controla campos dinâmicos do formulário.

A regra de negócio continua nos arquivos Python da pasta `src`. Assim, o HTML/CSS cuida da apresentação, enquanto o Python cuida dos cálculos.

---

## Arquivos para entrega

- Código-fonte Python: pasta `src`.
- Interface web HTML/CSS: pastas `templates` e `static`.
- Aplicação web: `web_app.py`.
- Dependências: `requirements.txt`.
- Fluxograma, pseudocódigo e roteiros: pasta `docs`.
- CSV de exemplo: pasta `exemplos`.
- CSVs gerados pela interface: pasta `saida_csv`.
- README explicativo: `README.md`.
# rm-orcamento-aluguel
