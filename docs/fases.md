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

# 7 Funcioned de leer txt y de json
almacenamiento/leer.py

import json

def leer_txt(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def leer_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

# 8 La raiz del codigo donde se ejecuta
main.py

from sentimiento.analizador import analizar_por_nivel
from almacenamiento.guardar import guardar_json, guardar_txt

def main():
    texto = "El producto llegó rápido, pero la calidad no es lo que esperaba."

    resultado = analizar_por_nivel(texto, nivel="intermedio")

    print(resultado)

    guardar_txt(resultado)
    guardar_json(resultado)


if __name__ == "__main__":
    main()

# 9 Añadido test de almacenamiento y de analizador
tests/test_analizador.py
tests/test_almacenamiento.py

Añadido mock test para analizar_por_nivel (basico, intermedio, avanzado)
- Error implementado para manejar nivel invalido
- Añadido test de persistencia usando tmp_path para TXT y JSON
- Tests desacoplados del transformer usando monkeypatch
- Garantiza una ejecución de pruebas rápida y determinista.

# 10 Refactorizado el guardar.py para que los formatos de salida sean mas profesionales
almacenamiento/guardar.py

- Timestamp automático
- Creación automática de carpetas
- TXT tipo informe humano
- JSON estructurado
