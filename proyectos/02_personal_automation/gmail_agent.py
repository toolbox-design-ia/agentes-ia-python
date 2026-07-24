"""Proyecto 2 (capitulo 24): agente de automatizacion personal sobre Gmail.

Principios del capitulo: scope minimo (gmail.readonly por defecto), tres
almacenes con velocidades de cambio distintas (config.json, memory.json,
runs.json), lectura incremental, y separacion estricta entre ANALISIS (el
informe) y ACCION (nunca automatica en esta version).
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]  # scope minimo
BASE = Path(__file__).resolve().parent
CONFIG_FILE = BASE / "config.json"
MEMORY_FILE = BASE / "memory.json"
RUNS_FILE = BASE / "runs.json"

CLASSIFY_PROMPT = """Clasifica este correo en UNA categoria:
factura, urgente, accion_pendiente, informativo, promocion

Ten en cuenta las preferencias aprendidas del usuario:
{memoria}

De: {sender}
Asunto: {subject}
Extracto: {snippet}

Responde SOLO con la categoria."""


def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def gmail_service():
    # OAuth 2.0 con credenciales de cliente de Google Cloud Console
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    token = BASE / "token.json"
    if token.exists():
        creds = Credentials.from_authorized_user_file(str(token), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(BASE / "credentials.json"), SCOPES)
            creds = flow.run_local_server(port=0)
        token.write_text(creds.to_json(), encoding="utf-8")
    return build("gmail", "v1", credentials=creds)


def fetch_new_messages(service, runs: dict, max_results: int = 25) -> list[dict]:
    # Lectura incremental: solo lo posterior a la ultima ejecucion
    query = "in:inbox"
    last = runs.get("last_run_epoch")
    if last:
        query += f" after:{last}"
    resp = service.users().messages().list(
        userId="me", q=query, maxResults=max_results).execute()
    out = []
    for ref in resp.get("messages", []):
        msg = service.users().messages().get(
            userId="me", id=ref["id"], format="metadata",
            metadataHeaders=["From", "Subject"]).execute()
        headers = {h["name"]: h["value"]
                   for h in msg["payload"].get("headers", [])}
        out.append({"id": ref["id"], "sender": headers.get("From", ""),
                    "subject": headers.get("Subject", ""),
                    "snippet": msg.get("snippet", "")})
    return out


def classify(cliente, memory: dict, message: dict) -> str:
    prompt = CLASSIFY_PROMPT.format(
        memoria=json.dumps(memory.get("preferencias", {}),
                           ensure_ascii=False),
        sender=message["sender"], subject=message["subject"],
        snippet=message["snippet"])
    resp = cliente.messages.create(model="claude-haiku-4-5", max_tokens=20,
                                   messages=[{"role": "user",
                                              "content": prompt}])
    label = resp.content[0].text.strip().lower()
    allowed = ("factura", "urgente", "accion_pendiente", "informativo",
               "promocion")
    return label if label in allowed else "informativo"


def write_report(items: list[tuple[str, dict]]) -> Path:
    # El informe es el PRODUCTO del agente; la accion la decide el usuario
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [f"# Informe del buzon — {hoy}", ""]
    for categoria in ("urgente", "accion_pendiente", "factura",
                      "informativo", "promocion"):
        grupo = [m for c, m in items if c == categoria]
        if not grupo:
            continue
        lines.append(f"## {categoria} ({len(grupo)})")
        for m in grupo:
            lines.append(f"- {m['sender'][:40]} — {m['subject'][:70]}")
        lines.append("")
    out = BASE / f"informe_{hoy}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> int:
    config = load_json(CONFIG_FILE, {})
    memory = load_json(MEMORY_FILE, {"preferencias": {}})
    runs = load_json(RUNS_FILE, {})
    if not (BASE / "credentials.json").exists():
        print("Falta credentials.json (Google Cloud Console; el capitulo 24 "
              "explica el scope minimo y el Anexo A la puesta en marcha).")
        return 1
    service = gmail_service()
    messages = fetch_new_messages(service, runs,
                                  config.get("max_correos", 25))
    if not messages:
        print("No hay correos nuevos desde la ultima ejecucion.")
        return 0
    cliente = anthropic.Anthropic()
    labeled = [(classify(cliente, memory, m), m) for m in messages]
    report = write_report(labeled)
    runs["last_run_epoch"] = int(datetime.now(timezone.utc).timestamp())
    runs["last_report"] = report.name
    RUNS_FILE.write_text(json.dumps(runs, indent=1), encoding="utf-8")
    print(f"{len(messages)} correos analizados. Informe: {report.name}")
    print("Este agente ANALIZA; las acciones las decides tu tras leer el "
          "informe (separacion analisis/accion del capitulo 24).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
