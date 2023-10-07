import requests

url = "http://localhost:8888/email-validator"

payload = {"email": "contato@renato.tec.br"}
#payload = {"email": "contato@baralhomagico.com.br"}
#payload = {"email": "contato@gmail.com.br"}
#payload = {"email": "contato@gmail.com.br.vc"}
#payload = {"email": "contato@gmail.com.bx.vc"}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Resposta:")
    print(response.json())
else:
    print(f"Erro {response.status_code}:")
    print(response.text)
