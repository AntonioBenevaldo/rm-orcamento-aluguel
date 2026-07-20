# Modelagem estática

O diagrama completo representa entidades, objeto de valor, serviços e o agregado principal. `Imovel` define a abstração; `Apartamento`, `Casa` e `Estudio` especializam as regras; `Orcamento` agrega cliente, imóvel, contrato e itens de cálculo.

O estereótipo `aggregate root` indica que o orçamento coordena o cálculo anual. `ItemCalculo` é um objeto de valor imutável e os serviços não contêm estado.

- Fonte oficial: `diagrama_classes_completo.puml`.
- Imagem: `diagrama_classes_completo.png`.
- Vetor: `diagrama_classes_completo.svg`.
