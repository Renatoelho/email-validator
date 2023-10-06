import requests

url = "http://localhost:8888/email-validator"

payload = {"email": "%testev@gmail.com.br"}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Resposta:")
    print(response.json())
else:
    print(f"Erro {response.status_code}:")
    print(response.text)
