FROM ubuntu:20.04

LABEL maintainer="Renato coelho <contato@renato.tec.br>"
LABEL version="0.0.1"
LABEL description="Validando E-mail por TLD, DNS MX e sintaxe"

SHELL ["/bin/bash", "-c"]

RUN useradd -ms /bin/bash user_email -G sudo && \
  passwd -d  user_email && \
  mkdir -p /home/user_email/app 

WORKDIR /home/user_email

RUN apt update && \
  apt install python3.8 \
  python3.8-venv \
  dnsrecon \
  systemctl \
  curl \
  wget \
  nano \
  zip \
  unzip \
  tzdata \
  sudo -y 

RUN ln -sf /usr/bin/python3.8 /usr/bin/python3 && \
  echo "export PATH=$PATH:/usr/bin/python3" >> \
  /home/user_email/.bashrc && \
  source /home/user_email/.bashrc

WORKDIR /home/user_email/app

COPY app/ .

ADD deploy/email-validator.service /etc/systemd/system/

RUN systemctl daemon-reload && \
  systemctl enable email-validator.service

RUN chown -R user_email:user_email /home/user_email/app 

USER user_email

RUN python3 -m venv /home/user_email/.virtualenvs && \
  source /home/user_email/.virtualenvs/bin/activate && \
  pip install -U pip setuptools wheel && \
  pip install -r requirements.txt

ENV PYTHON_ENV="/home/user_email/app/.env"
ENV PYTHONPATH="/home/user_email/app:/home/user_email/app/utils:/home/user_email/app/models:/home/user_email/app/tests"
ENV TZ="America/Sao_Paulo"
ENV TERM=xterm-256color

EXPOSE 8888

ENTRYPOINT systemctl start email-validator.service