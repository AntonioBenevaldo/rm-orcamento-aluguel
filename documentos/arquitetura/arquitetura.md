# Arquitetura da aplicação

```text
Navegador (templates + static)
            |
            v
       app.py / web_app.py        <- apresentação e rotas
            |
            v
 servicos/orcamento_service.py    <- caso de uso e validação
            |
            v
 modelos/                         <- regras do domínio e POO
        /            \
       v              v
banco_de_dados/      utilitarios/ <- SQLite, moeda e CSV
```

As dependências apontam da apresentação para o domínio. As regras não dependem do Flask nem do SQLite, o que permite testá-las isoladamente.
