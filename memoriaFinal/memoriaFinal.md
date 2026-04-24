# Memoria Final — Proyecto Análisis de Sentimiento

## Descripción del código heredado

El código original usaba la API de **OpenAI (GPT-4o-mini)** para analizar
sentimientos. Dependía de una clave de API externa (`OPENAI_API_KEY`),
conexión a internet y un coste económico por cada llamada.

---

## Problemas del código original

### 1. Dependencia de API externa de pago
**Situación original:**
```python
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```
El análisis dependía completamente de la API de OpenAI, lo que implica:
- Necesidad de conexión a internet
- Coste económico por cada llamada
- Dependencia de un servicio externo que puede fallar o cambiar

**Solución:**
Se sustituyó por el modelo local `distilbert-base-uncased-finetuned-sst-2-english`
usando la librería `transformers` de HuggingFace, que funciona completamente
offline una vez descargado.

---

### 2. Modelo cargado múltiples veces
**Situación original:**
```python
def get_model():
    return pipeline("sentiment-analysis")
```
Cada llamada a `get_model()` instanciaba un nuevo pipeline, cargando el
modelo 3 veces en memoria (una por cada nivel de análisis).

**Solución:**
Se implementó un patrón de caché con variable global:
```python
_model = None

def get_model():
    global _model
    if _model is None:
        _model = pipeline(
            "sentiment-analysis",
            model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
            revision="af0f99b"
        )
    return _model
```

---

### 3. Niveles de análisis basados en prompts
**Situación original:**
Los tres niveles (básico, intermedio, avanzado) se diferenciaban mediante
prompts distintos enviados a GPT-4o-mini, obteniendo respuestas en JSON
que luego había que parsear manualmente con riesgo de fallos.

**Solución:**
Se implementaron tres funciones locales en `analizador.py` que procesan
la salida del modelo de HuggingFace y construyen el resultado por nivel
sin depender de parseo de JSON externo.

---

### 4. Función `guardar_resultado()` con firma incorrecta
**Situación original:**
```python
def guardar_resultado(texto_entrada: str, resultados: dict):
```
Se llamaba con dos argumentos separados, pero `interfaz.py` ya incluía
el texto dentro del diccionario de resultados, causando un `TypeError`.

**Solución:**
Se unificó en un solo parámetro:
```python
def guardar_resultado(resultados: dict) -> dict:
```

---

### 5. Entorno virtual subido a GitHub
**Situación original:**
La carpeta `env/` no estaba en `.gitignore`, lo que generaba más de
10.000 archivos rastreados por Git y superaba el límite de 100MB de GitHub.

**Solución:**
Se configuró un `.gitignore` adecuado y se eliminó `env/` del índice:
