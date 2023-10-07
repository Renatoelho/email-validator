
# Build da imagem Docker do Validador de E-mails por TLD, DNS MX e Sintaxe

+ Clonando o repositório:

```bash
git clone https://github.com/Renatoelho/email-validator.git email-validator
```

+ Acessando o repositório:

```bash
cd email-validator/
```

+ Fazendo o Build da imagem da aplicação

```bash
docker build -f dockerfile -t renatoelho/email-validator:0.0.1 .
```

+ Ativando a aplicação:

```bash
docker run --rm -d --name=email-validator --hostname=email-validator -p 8888:8888 email-validator:0.0.1 
```

+ Endpoint da documentação

[http://localhost:8888/redoc](http://localhost:8888/redoc)

+ Endpoint da solução

[http://localhost:8000/email_validator](http://localhost:8000/email_validator) 

+ Endpoint para Healthcheck

[http://localhost:8888/healthcheck](http://localhost:8888/healthcheck)

> ***Observação:*** Esse endpoint do ***Healthcheck*** é para, se caso você for implantar a solução utilizando o docker compose por exemplo.