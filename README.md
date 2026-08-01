# Sistema de Orçamento Imobiliário R.M

Aplicação acadêmica em Python e Streamlit para calcular, persistir e exportar orçamentos de locação de apartamentos, casas e estúdios.

## Funcionalidades

- Cálculo do aluguel conforme as regras de cada imóvel.
- Contrato imobiliário fixo de R$ 2.000,00 em uma a cinco parcelas.
- Cronograma financeiro de 12 meses.
- Memória detalhada de acréscimos e desconto.
- Persistência transacional em seis tabelas SQLite.
- Consulta dos orçamentos registrados.
- Exportação CSV em UTF-8 com separador ponto e vírgula.
- Testes automatizados de domínio, banco, integridade, transação, CSV e interface.

## Regras implementadas

| Imóvel | Regra |
|---|---|
| Apartamento | Base R$ 700,00; segundo quarto + R$ 200,00; garagem + R$ 300,00; desconto de 5% quando o cliente não possui crianças. |
| Casa | Base R$ 900,00; segundo quarto + R$ 250,00; garagem + R$ 300,00. |
| Estúdio | Base R$ 1.200,00; pacote das duas primeiras vagas + R$ 250,00; cada vaga adicional + R$ 60,00. |
| Contrato | R$ 2.000,00, parcelável entre uma e cinco vezes. |

A regra do estúdio aceita zero vaga ou pelo menos duas vagas, porque o enunciado não define preço isolado para uma vaga. Quando R$ 2.000,00 não é divisível exatamente pela quantidade de parcelas, os centavos restantes são distribuídos nas primeiras parcelas para preservar o total exato.

## Arquitetura

```text
app.py / pages/          Interface Streamlit
services/                Casos de uso e exportação
models/                  Entidades e regras orientadas a objetos
database/                SQLite, schema e repositório transacional
utils/                   Formatação monetária
tests/                   Testes automatizados
data/                     Banco criado em tempo de execução
docs/                     Diagramas PlantUML
```

## Instalação no Windows

### Pré-requisitos

- Windows 10 ou 11.
- Python 3.10 ou superior instalado e disponível no terminal.
- Conexão com a internet apenas durante a instalação das dependências.

Abra o PowerShell ou o terminal do VS Code na pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Inicialização simplificada no Windows

Também foram incluídos três arquivos de apoio:

1. `INSTALAR.bat` - cria o ambiente virtual e instala as dependências.
2. `INICIAR_SISTEMA.bat` - inicia a aplicação Streamlit.
3. `EXECUTAR_TESTES.bat` - executa a suíte de testes.

Na primeira utilização, execute `INSTALAR.bat`. Depois, utilize `INICIAR_SISTEMA.bat`.

## Executar os testes

```powershell
python -m pytest -v
```

## Executar a aplicação

```powershell
python -m streamlit run app.py
```

O terminal exibirá o endereço local, normalmente `http://localhost:8501`.

## Banco de dados

O arquivo `data/imobiliaria.db` é criado automaticamente. Valores monetários são gravados como `INTEGER` em centavos. A operação de gravação é atômica: se qualquer item ou parcela falhar, o orçamento inteiro é revertido.

## Documentação técnica

O diretório `docs/` contém o diagrama de classes, o modelo de dados e o fluxograma em formato PlantUML (`.puml`). Esses arquivos podem ser abertos no VS Code com uma extensão compatível com PlantUML ou renderizados pela ferramenta PlantUML.

## Privacidade

Utilize somente dados fictícios na demonstração, nas capturas e no vídeo. O banco local está ignorado pelo Git para evitar publicação acidental de registros.
