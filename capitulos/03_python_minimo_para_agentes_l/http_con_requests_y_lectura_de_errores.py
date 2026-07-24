import requests

url = "https://api.anthropic.com/v1/messages"
headers = {
    "x-api-key": "sk-ant-...",
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}
payload = {
    "model": "claude-sonnet-4-5",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "¿Qué es un agente de IA?"}]
}

response = requests.post(url, headers=headers, json=payload)
