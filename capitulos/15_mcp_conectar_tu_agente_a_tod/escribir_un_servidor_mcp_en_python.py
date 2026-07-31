from mcp.server import MCPServer

mcp = MCPServer("calculadora")

@mcp.tool()
def sumar(a: float, b: float) -> float:
    """Suma dos números y devuelve el resultado."""
    return a + b

@mcp.tool()
def dividir(dividendo: float, divisor: float) -> float:
    """Divide dos números. Devuelve error si el divisor es cero."""
    if divisor == 0:
        raise ValueError("No se puede dividir entre cero.")
    return dividendo / divisor

if __name__ == "__main__":
    mcp.run()
