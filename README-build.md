
# Build da imagem Docker do Validador de E-mails por TLD, DNS MX e Sintaxe

### Fazendo o Build da imagem base

```bash
docker build -f dockerfile -t renatoelho/email-validator:0.0.1 .
```

### Ativando o serviço de validação de E-mails

```bash
docker run --rm -d --name=email-validator --hostname=
email-validator -p 8888:8888 renatoelho/email-validator:0.0.1 
```
