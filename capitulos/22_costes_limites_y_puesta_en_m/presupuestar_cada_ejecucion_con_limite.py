import time

class PresupuestoEjecucion:
    def __init__(self, max_llamadas=10, max_tokens_salida=8000,
                 max_herramientas=20, max_segundos=120, max_coste_usd=0.50):
        self.max_llamadas = max_llamadas
        self.max_tokens_salida = max_tokens_salida
        self.max_herramientas = max_herramientas
        self.max_segundos = max_segundos
        self.max_coste_usd = max_coste_usd
        self.llamadas = 0
        self.tokens_salida = 0
        self.herramientas = 0
        self.coste_usd = 0.0
        self.inicio = time.time()

    def registrar_llamada(self, tokens_out, coste):
        self.llamadas += 1
        self.tokens_salida += tokens_out
        self.coste_usd += coste

    def registrar_herramienta(self):
        self.herramientas += 1

    def dentro_de_limite(self):
        elapsed = time.time() - self.inicio
        if self.llamadas >= self.max_llamadas:
            return False, "máximo de llamadas alcanzado"
        if self.tokens_salida >= self.max_tokens_salida:
            return False, "máximo de tokens de salida alcanzado"
        if self.herramientas >= self.max_herramientas:
            return False, "máximo de herramientas alcanzado"
        if elapsed >= self.max_segundos:
            return False, f"tiempo máximo superado ({elapsed:.1f}s)"
        if self.coste_usd >= self.max_coste_usd:
            return False, f"coste máximo superado (${self.coste_usd:.4f})"
        return True, ""
