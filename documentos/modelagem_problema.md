# Modelagem do Problema - Orçamento de Aluguel Imobiliária R.M

## 1. Descrição do problema

A Imobiliária R.M necessita automatizar orçamentos de apartamentos, casas e estúdios. O sistema deve aplicar regras comerciais com precisão, apresentar contrato e cronograma anual, manter histórico e permitir exportação CSV.

## 2. Direcionadores de negócio

| Direcionador | Objetivo |
|---|---|
| Automação | Substituir o cálculo manual e repetitivo |
| Precisão | Aplicar acréscimos e desconto sempre na ordem correta |
| Transparência | Exibir todos os itens que formaram o aluguel |
| Rastreabilidade | Preservar cliente, imóvel, contrato, itens e parcelas |
| Interoperabilidade | Gerar CSV compatível com planilhas |
| Evolução | Separar interface, serviços, domínio e persistência |

## 3. Atores

- **Atendente/usuário:** preenche o formulário, consulta e exporta.
- **Cliente:** pessoa para quem o orçamento é emitido.
- **Sistema:** valida, calcula, persiste e apresenta os resultados.

## 4. Entradas

Nome do cliente, informação sobre crianças, tipo de imóvel, quartos, garagem ou vagas de estacionamento e quantidade de parcelas do contrato.

## 5. Regras de negócio

| Código | Regra |
|---|---|
| RN01 | Apartamento com um quarto custa R$ 700,00 |
| RN02 | Segundo quarto do apartamento acrescenta R$ 200,00 |
| RN03 | Casa com um quarto custa R$ 900,00 |
| RN04 | Segundo quarto da casa acrescenta R$ 250,00 |
| RN05 | Estúdio custa R$ 1.200,00 |
| RN06 | Garagem de apartamento/casa acrescenta R$ 300,00 |
| RN07 | Duas vagas de estúdio custam R$ 250,00; cada adicional, R$ 60,00 |
| RN08 | Apartamento para cliente sem crianças recebe 5% de desconto sobre o subtotal |
| RN09 | Contrato custa R$ 2.000,00 e aceita de uma a cinco parcelas |
| RN10 | O cronograma possui exatamente 12 meses |

## 6. Casos de uso

### UC01 - Gerar orçamento

1. Usuário informa cliente e características.
2. Sistema valida os campos.
3. Serviço instancia a subclasse correta.
4. Domínio calcula itens, desconto, contrato e total anual.
5. Persistência grava todas as entidades em uma transação.
6. Interface apresenta métricas, memória de cálculo e parcelas.

### UC02 - Consultar orçamento

O usuário seleciona um registro no histórico e recebe resumo, itens e doze parcelas.

### UC03 - Exportar CSV

O usuário exporta o cronograma individual ou o histórico consolidado em UTF-8.

## 7. Pensamento algorítmico

- **Decomposição:** entrada, validação, cálculo, contrato, cronograma, persistência e saída.
- **Padrões:** os imóveis compartilham quartos, vagas e operação de cálculo.
- **Abstração:** `Imovel` ignora detalhes de interface e banco.
- **Decisões:** tipo do imóvel, segundo quarto, garagem, crianças e vagas.
- **Repetição:** laço gera os meses de 1 a 12.
- **Avaliação:** testes com valores esperados comprovam o algoritmo.

## 8. Pseudocódigo

```text
INÍCIO
  LER dados
  VALIDAR nome, tipo, quartos, vagas e parcelas
  CRIAR Cliente, Imovel específico e Contrato
  CALCULAR itens do aluguel
  SE apartamento E sem crianças
    APLICAR desconto de 5% sobre o subtotal
  FIM-SE
  PARA mês DE 1 ATÉ 12
    parcela <- valor do contrato SE mês <= parcelas SENÃO zero
    total <- aluguel + parcela
  FIM-PARA
  INICIAR transação
  SALVAR entidades, itens e parcelas
  CONFIRMAR transação
  EXIBIR resultado e disponibilizar CSV
FIM
```

## 9. Critérios de aceitação

- Os três cenários oficiais retornam R$ 1.140,00, R$ 1.450,00 e R$ 1.570,00.
- Parcelamento fora de 1 a 5 é rejeitado.
- Cada orçamento persistido tem itens e exatamente 12 parcelas.
- Chaves estrangeiras e integridade SQLite não apresentam falhas.
- CSV individual possui cabeçalho e 12 linhas de dados.
