async def run_conversation():
    async with create_mcp_client(config) as client:
        tools = await client.list_tools()

        # Recursos de contexto automático al inicio de sesión
        profile = await client.read_resource("memory://profile")
        today_tasks = await client.read_resource("tasks://today")

        messages = [{
            "role": "user",
            "content": f"Contexto de sesión:\n{profile}\n{today_tasks}"
        }]

        while True:
            user_input = input("\nTú: ").strip()
            if user_input.lower() in ("salir", "exit", "quit"):
                break

            messages.append({"role": "user", "content": user_input})
            response = await llm.complete(messages=messages, tools=tools)

            if response.tool_calls:
                for call in response.tool_calls:
                    result = with_confirmation(
                        call.name, call.arguments,
                        lambda: client.call_tool(call.name, call.arguments)
                    )
                    messages.append(tool_result_message(call, result))

                final = await llm.complete(messages=messages, tools=tools)
                print(f"\nAsistente: {final.content}")
                messages.append({"role": "assistant", "content": final.content})
            else:
                print(f"\nAsistente: {response.content}")
                messages.append({"role": "assistant", "content": response.content})
