"""Cliente del asistente (capitulo 25): conecta los servidores MCP y el modelo.

Lee assistant-config.json, lanza cada servidor por stdio, recopila sus
herramientas y las expone a Claude en un bucle de conversacion con
confirmacion humana para las herramientas sensibles (policies.json).
"""
import asyncio
import json
import os
import sqlite3
from contextlib import AsyncExitStack
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
BASE = Path(__file__).resolve().parent
DB_PATH = os.getenv("ASSISTANT_DB", str(BASE / "assistant.db"))
MODEL = os.getenv("ASSISTANT_MODEL", "claude-sonnet-5")


def load_config() -> dict:
    return json.loads((BASE / "assistant-config.json").read_text("utf-8"))


def load_policies() -> dict:
    return json.loads((BASE / "policies.json").read_text("utf-8"))


def audit(tool: str, arguments: dict, authorized: bool) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO audit_log (tool, arguments, authorized, ts, session)"
            " VALUES (?, ?, ?, ?, ?)",
            (tool, json.dumps(arguments, ensure_ascii=False),
             int(authorized),
             datetime.now(timezone.utc).isoformat(), "cli"))


async def connect_servers(stack: AsyncExitStack, config: dict):
    sessions, tools = {}, []
    for server in config["servers"]:
        params = StdioServerParameters(
            command=server["command"][0], args=server["command"][1:],
            env={**os.environ, **server.get("env", {})})
        read, write = await stack.enter_async_context(stdio_client(params))
        session = await stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        listed = await session.list_tools()
        for tool in listed.tools:
            tools.append({"name": tool.name,
                          "description": tool.description or "",
                          "input_schema": tool.inputSchema})
            sessions[tool.name] = session
    return sessions, tools


async def run_conversation():
    config, policies = load_config(), load_policies()
    cliente = anthropic.Anthropic()
    async with AsyncExitStack() as stack:
        sessions, tools = await connect_servers(stack, config)
        print(f"Asistente listo: {len(tools)} herramientas de "
              f"{len(config['servers'])} servidores. Enter vacio para salir.")
        messages = []
        while True:
            user = input("\nTu: ").strip()
            if not user:
                return
            messages.append({"role": "user", "content": user})
            while True:
                response = cliente.messages.create(
                    model=MODEL, max_tokens=1000, tools=tools,
                    messages=messages)
                if response.stop_reason != "tool_use":
                    text = "".join(b.text for b in response.content
                                   if b.type == "text")
                    print(f"Asistente: {text}")
                    messages.append({"role": "assistant",
                                     "content": response.content})
                    break
                messages.append({"role": "assistant",
                                 "content": response.content})
                results = []
                for block in response.content:
                    if block.type != "tool_use":
                        continue
                    needs_ok = block.name in policies.get(
                        "require_confirmation", [])
                    authorized = True
                    if needs_ok:
                        answer = input(f"  Autorizar {block.name}"
                                       f"({block.input})? [s/N] ")
                        authorized = answer.strip().lower() == "s"
                    audit(block.name, block.input, authorized)
                    if not authorized:
                        content = "Denegado por el usuario."
                    else:
                        result = await sessions[block.name].call_tool(
                            block.name, block.input)
                        content = "\n".join(
                            c.text for c in result.content
                            if getattr(c, "text", None))
                    results.append({"type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": content})
                messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    asyncio.run(run_conversation())
