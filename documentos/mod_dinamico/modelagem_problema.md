# Modelagem dinâmica

A modelagem dinâmica registra o comportamento do sistema em três casos complementares:

1. `sequencia_camadas`: percurso completo da interface à transação SQLite.
2. `sequencia_calculos`: ramificações e regras de apartamento, casa e estúdio.
3. `sequencia_exportacao`: geração individual e consolidada do CSV.

Cada diagrama possui fonte `.puml`, imagem `.png` e vetor `.svg`. O arquivo `fluxo_orcamento.mmd` apresenta uma visão resumida compatível com Mermaid.

Os diagramas mostram chamadas que existem no código (`CalculoService.processar_orcamento`, `salvar_orcamento`, `ExportService.gerar_csv`) e, por isso, podem ser usados como evidência da implementação.
