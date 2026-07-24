from tenacity import (
    retry, stop_after_attempt,
    wait_exponential, wait_random,
    retry_if_exception_type
)
import anthropic

@retry(
    retry=retry_if_exception_type(anthropic.RateLimitError),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=60) + wait_random(0, 2)
)
def llamar_modelo(cliente, mensajes, modelo, **kwargs):
    return cliente.messages.create(
        model=modelo,
        messages=mensajes,
        **kwargs
    )
