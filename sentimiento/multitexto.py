from .analizador import analizar_por_nivel

def analizar_lista_textos(textos: list, nivel="basico"):
    return [analizar_por_nivel(texto, nivel) for texto in textos]   