from .cliente import get_model
from .niveles import (
    analizar_basico,
    analizar_intermedio,
    analizar_avanzado
)

model = get_model()

def analizar_por_nivel(texto: str, nivel: str = "basico"):
    if nivel == "basico":
        return analizar_basico(model, texto)
    elif nivel == "intermedio":
        return analizar_intermedio(model, texto)
    elif nivel == "avanzado":
        return analizar_avanzado(model, texto)
    else:
        raise ValueError("Nivel no válido")