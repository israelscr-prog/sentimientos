from .cliente import get_model
from .niveles import (
    analizar_basico,
    analizar_intermedio,
    analizar_avanzado
)

# Inicialización del modelo (mockeable en tests)
model = get_model()


def analizar_por_nivel(texto: str, nivel: str = "basico"):
    """
    Analiza el sentimiento de un texto según el nivel indicado.

    :param texto: Texto a analizar
    :param nivel: Nivel de análisis (basico, intermedio, avanzado)
    :return: dict con el resultado
    """

    # 🔒 Validaciones
    if texto is None:
        raise ValueError("El texto no puede ser None")

    if not isinstance(texto, str):
        raise TypeError("El texto debe ser un string")

    if nivel not in ["basico", "intermedio", "avanzado"]:
        raise ValueError("Nivel no válido")

    # ⚙️ Lógica principal
    if nivel == "basico":
        return analizar_basico(model, texto)

    elif nivel == "intermedio":
        return analizar_intermedio(model, texto)

    elif nivel == "avanzado":
        return analizar_avanzado(model, texto)