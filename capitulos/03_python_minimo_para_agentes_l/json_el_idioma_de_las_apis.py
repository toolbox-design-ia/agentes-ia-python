import json

payload = {
    "model": "claude-sonnet-5",
    "messages": [{"role": "user", "content": "Hola"}]
}

texto_json = json.dumps(payload)
print(type(texto_json))   # <class 'str'>
print(texto_json)
# {"model": "claude-sonnet-5", "messages": [{"role": "user", "content": "Hola"}]}
