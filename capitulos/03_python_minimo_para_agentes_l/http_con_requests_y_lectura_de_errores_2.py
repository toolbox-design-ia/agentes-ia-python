try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()   # lanza excepción si el código es 4xx o 5xx
    datos = response.json()
except requests.exceptions.Timeout:
    print("La petición tardó demasiado. Reintenta.")
except requests.exceptions.HTTPError as e:
    print(f"Error HTTP: {e}")
    print(f"Detalle: {response.text}")
except Exception as e:
    print(f"Error inesperado: {e}")
