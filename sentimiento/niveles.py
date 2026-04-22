def analizar_basico(model, texto: str) -> dict:
    resultado = model(texto)[0]
    return {
        "nivel": "basico",
        "sentimiento": resultado["label"]
    }


def analizar_intermedio(model, texto: str) -> dict:
    resultado = model(texto)[0]
    return {
        "nivel": "intermedio",
        "sentimiento": resultado["label"],
        "confianza": resultado["score"]
    }


def analizar_avanzado(model, texto: str) -> dict:
    resultado = model(texto)[0]
    return {
        "nivel": "avanzado",
        "sentimiento": resultado["label"],
        "confianza": resultado["score"],
        "texto": texto
    }