def with_confirmation(tool_name: str, args: dict, execute_fn):
    policy = get_policy(tool_name)

    if policy.is_blocked:
        return {"error": f"La herramienta '{tool_name}' está bloqueada por política."}

    if policy.requires_confirmation:
        print(f"\n[CONFIRMACIÓN] El agente quiere ejecutar:")
        print(f"  Herramienta: {tool_name}")
        print(f"  Argumentos:  {json.dumps(args, ensure_ascii=False, indent=2)}")
        respuesta = input("  ¿Autorizar? (s/n): ").strip().lower()
        if respuesta != "s":
            log_action(tool_name, args, authorized=False)
            return {"error": "Acción denegada por el usuario."}

    result = execute_fn()
    log_action(tool_name, args, authorized=True)
    return result
