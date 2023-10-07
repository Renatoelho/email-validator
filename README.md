# Validando e-mails com TLD, DNS MX e Sintaxe

![Validando e-mails](https://drive.google.com/uc?export=view&id=1y1zFTkjJ6VcXPoQighzCTwI7SC8p9N1r)

Este projeto visa obter bom nível de confiança de um determinado endereço de e-mail, considerando diversos fatores, incluindo a validade do ***Top-Level Domain*** (TLD) que é quando um domínio está listado entre os domínios válidos existentes como .com, .com.br etc., a existência de ***registros de DNS do tipo MX*** associados ao domínio e a validação de ***sintaxe*** do e-mail.

### Requisitos

+ ![Docker](https://img.shields.io/badge/Docker-23.0.3-E3E3E3)

+ ![Git](https://img.shields.io/badge/Git-2.25.1%2B-E3E3E3)

+ ![Ubuntu](https://img.shields.io/badge/Ubuntu-20.04-E3E3E3)

Existem várias maneiras de atribuir uma alta taxa de confiança a um determinado endereço de ***e-mail***, como a verificação da conexão ***SMTP*** e a confirmação do e-mail quando uma mensagem é enviada e aguarda-se uma ação por parte do usuário, entre outras. No entanto, também existem abordagens que incluem a verificação da validade do ***TLD*** do domínio em questão, a presença de registros ***DNS do tipo MX*** vinculados ao domínio e outras verificações relevantes.

A abordagem mais eficaz envolve a implementação de um fluxo de confirmação de e-mail. No entanto, essa opção é mais adequada quando o usuário detentor do endereço de e-mail está se cadastrando no sistema. Para processos em lote (***ETL***), essa abordagem proativa não é recomendada, uma vez que o momento de check-in do usuário no sistema já passou e pode causar algum desconforto se o usuário/cliente for solicitado a confirmar algo algum tempo depois de se cadastrar no sistema.

A atribuição de uma pontuação baseada em métricas, como a existência do domínio entre lista de domínios válidos (TLD) que é gerenciado pela [IANA](https://www.iana.org/domains), registros DNS do tipo MX e validação de sintaxe do e-mail, proporciona um bom grau de confiança. No escopo desse projeto, um domínio com TLD válido tem um peso de 45%, a presença de registros DNS do tipo MX contribui com mais 25% e uma sintaxe válida tem um peso de mais 20% no valor final da pontuação.

|Regra|percentual da pontuação|
|--------------------------------|--------------------------|
|TLD válido|45%|
|Registros DNS tipo MX|25%|
|Sintaxe válida|20%|

> ***Observação:*** Esses percentuais fazem sentido para o contexto da regra de negócio que utilizei nesse projeto, mas caso queira pode alterar para outros percentuais. 

Se o TLD for inválido, as demais regras não serão aplicadas, e a pontuação é cumulativa. Um exemplo é um endereço de e-mail onde seu TLD é válido, mas não existem registros de DNS do tipo MX e a sintaxe do e-mail é válida, recebe uma ***pontuação de 65%***.

O valor final da pontuação é a soma do percentual das três regras, podendo chegar, no máximo, ***a 90%***. Isso ocorre porque, mesmo com essas verificações, ainda não é possível alcançar 100% de confiança no endereço de e-mail específico. Para ***atingir 100%*** de confiança, seria necessário realizar um processo adicional de confirmação de e-mail.

### Implantação da solução

Foi criada uma API com FastAPI (Python) que inclui um endpoint (***/email_validator***) que recebe um ***payload*** no método ***POST***. Esse payload contém uma chave chamada ```email``` e um valor que descreve o endereço de e-mail, por exemplo: ```{"email": "contato@renato.tec.br"}```. Esse endereço de e-mail será validado e a API deverá responder com o seguinte conteúdo:

```json
{
    "email": "contato@renato.tec.br",
    "domain_tld": true,
    "domain_dns_mx": true,
    "syntax": true,
    "score": 90.0
}
```

Para implantar essa solução disponibilizei uma imagem no [Docker Hub](https://hub.docker.com/repository/docker/renatoelho/email-validator/general), onde com o seguinte comando do Docker você criar um contêiner e já pode iniciar suas validações:

+ Ativando a solução

```bash
docker run -d --name=email-validator --hostname=email-validator -p 8888:8888 renatoelho/email-validator:0.0.1
```

+ Endpoint da documentação

[http://localhost:8888/redoc](http://localhost:8888/redoc)

+ Endpoint da solução

[http://localhost:8000/email_validator](http://localhost:8000/email_validator) 

+ Endpoint para Healthcheck

[http://localhost:8888/healthcheck](http://localhost:8888/healthcheck)

> ***Observação:*** Esse endpoint do ***Healthcheck*** é para, se caso você for implantar a solução utilizando o docker compose por exemplo.

### Detalhes da aplicação

Para obter mais detalhes sobre como este projeto foi desenvolvido, verifique os arquivos do projeto [clicando aqui](https://github.com/Renatoelho/email-validator/tree/main/app). Para acessar a parte de construção da imagem da solução, [visite aqui](https://github.com/Renatoelho/email-validator/blob/main/README-build.md).

### Vídeo de apresentação

Em desenvolvimento...

### Licença

Este projeto é licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT) - consulte o arquivo [LICENSE](https://github.com/Renatoelho/email-validator/blob/main/LICENSE) para obter detalhes.

### Agradecimentos

Agradecimento a ***Emerson de Sales*** por suas contribuições para este projeto!

### Referências

O que é um domínio de nível superior (TLD)?, ***Cloudflare***. Disponível em: <https://www.cloudflare.com/pt-br/learning/dns/top-level-domain/>. Acesso em: 3 out. 2023.

Tool Documentation, ***DNS Recon***. Disponível em: <https://www.kali.org/tools/dnsrecon/#dnsrecon>. Acesso em: 3 out. 2023.

MX Record, ***Wikipedia***. Disponível em: <https://pt.wikipedia.org/wiki/Mx_record>. Acesso em: 3 out. 2023.

Por que você deve verificar endereço de email?, ***Emailable***. Disponível em: <https://emailable.com/pt-br/blog/por-que-voce-deve-verificar-endereco-de-email/>. Acesso em: 3 out. 2023.
