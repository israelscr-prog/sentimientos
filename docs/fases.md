# 1 Creacion de estroctura
mkdir sentimiento,almacenamiento,resultados,tests,docs; mkdir resultados\txt,resultados\json; ni sentimiento\__init__.py,sentimiento\cliente.py,sentimiento\analizador.py,sentimiento\niveles.py,sentimiento\multitexto.py,almacenamiento\__init__.py,almacenamiento\guardar.py,almacenamiento\leer.py,tests\test_analizador.py,tests\test_almacenamiento.py,main.py,requirements.txt,README.md

# 2 Creado el cliente de modelo
sentimiento/cliente.py

from transformers import pipeline

def get_model():
    return pipeline("sentiment-analysis")

# 3 Creacion de separacion de niveles
sentimiento/niveles.py

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

# 4 Capa de servicios que centralizar la lógica (patrón facade)
sentimiento/analizador.py

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

# 5 funcion de procesamiento en lote
sentimiento/multitexto.py

from .analizador import analizar_por_nivel

def analizar_lista_textos(textos: list, nivel="basico"):
    return [analizar_por_nivel(texto, nivel) for texto in textos]

# 6 Funcioned de guardad en txt y json
almacenamiento/guardar.py

import json

def guardar_txt(resultado, ruta="resultado.txt"):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(str(resultado))


def guardar_json(resultado, ruta="resultado.json"):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)