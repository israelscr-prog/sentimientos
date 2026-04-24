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

# 11 Cambio en nombres de (1).png y de (1).py y añadido el .gitignore para no subir:

- resultados
- .venv/
- heredado/

# 12 (23/04/26) 10:00am / Mejora de testing y robustez con cambios en archivos guardar.py y analizador.py
 
- Cubren casos: felices, borde y de error
- Intoducion de validaciones
- Usos de: pytest, tmp_path y de mocks 

# 13 (13:30pm) Integracion Continua CI/CD de pipeline con GitHub Actions

- Ejecucion automatica de tests con pytest
- Validaciones en multiples versiones de python
- Instalacion automatica de dependencias
- Configuracion de entorno para imports (PYTHONPATH)

# 14 (24/04/26) 10:00am / Implementación del módulo de almacenamiento
- Creación automática de carpetas (resultados/txt, resultados/json)
- Generación de nombres únicos mediante timestamp
- Evita la sobreescritura de archivos
- Soporte para múltiples formatos de entrada (simple y estructurado)
- Funciones atómicas: guardar_txt, guardar_json
- Función orquestadora: guardar_resultado

# 15 Implementación del módulo de lectura
- Lista de de archivos guardados
- Leer analisis en formato JSON
- Leer analisis en formato TXT
- Buscar por fecha

# 16 ** IMPORTANTE** Se ha degradado las versiones de PYTHON 3.14 y 3.13 a la version 3.11
- El transformer no es conpatible con verisones de phyton mayores al 3.11

# 17 Refactorización del analizador
Se eliminó la inicialización global del modelo para evitar efectos secundarios en tiempo de importación.

Cambios:
- Implementación de lazy loading del modelo
- Validación de entradas
- Manejo de casos borde (texto vacío)

# 18 Refactorización del analizador

# 19 Cambios en funcion en test_analizador

# 20 Mock mas agresivo
Ejecucion de test mas agresivos y ejecucion automaticamente de todos los test INDEPENDIENTEMENTE de PyTorch/TensorFlow/transformers! 

# 21 Refactorización del analizador

# 22 Creacion de documentos
- almacenamiento.md
- api_referencia.md
- arquitectura.md