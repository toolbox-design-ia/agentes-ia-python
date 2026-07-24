import httpx

def buscar_web_propia(subpregunta: str, api_key: str) -> list[dict]:
    r = httpx.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
        json={"q": subpregunta, "num": 5},
    )
    r.raise_for_status()
    data = r.json()
    return [
        {
            "url": item["link"],
            "title": item["title"],
            "snippet": item.get("snippet", ""),
        }
        for item in data.get("organic", [])
    ]
