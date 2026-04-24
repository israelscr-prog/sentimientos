# 💾 Módulo de Almacenamiento

## Descripción

El módulo `almacenamiento/` gestiona la persistencia de los resultados del análisis de sentimientos. Soporta dos formatos de salida: **TXT** (legible por humanos) y **JSON** (estructurado para integración con otros sistemas).

---

## Estructura

```
almacenamiento/
├── __init__.py
├── guardar.py    # Funciones de escritura
└── leer.py       # Funciones de lectura
```

---

## Sistema de Archivos de Resultados

```
resultados/
├── txt/
│   ├── resultado_20260424_130000.txt
│   └── resultado_20260424_133045.txt
└── json/
    ├── resultado_20260424_130000.json
    └── resultado_20260424_133045.json
```

- Las carpetas `resultados/txt/` y `resultados/json/` se crean **automáticamente** si no existen.
- Cada archivo lleva un **timestamp único** en el nombre para evitar sobreescrituras.
- La carpeta `resultados/` está incluida en `.gitignore` y no se sube al repositorio.

---

## Módulo `guardar.py`

### `guardar_txt(resultado, ruta)`

Guarda el resultado como texto plano en formato informe legible.

```python
from almacenamiento.guardar import guardar_txt

resultado = {"nivel": "intermedio", "sentimiento": "POSITIVE", "confianza": 0.998}
guardar_txt(resultado)
# → Crea: resultados/txt/resultado_20260424_133045.txt
```

**Formato del archivo TXT generado:**
```
========================================
  ANÁLISIS DE SENTIMIENTO
  Fecha: 2026-04-24 13:30:45
========================================
Nivel      : intermedio
Sentimiento: POSITIVE
Confianza  : 0.998
========================================
```

---

### `guardar_json(resultado, ruta)`

Guarda el resultado en formato JSON estructurado con indentación.

```python
from almacenamiento.guardar import guardar_json

resultado = {"nivel": "avanzado", "sentimiento": "NEGATIVE", "confianza": 0.87, "texto": "Muy decepcionante"}
guardar_json(resultado)
# → Crea: resultados/json/resultado_20260424_133045.json
```

**Formato del archivo JSON generado:**
```json
{
    "nivel": "avanzado",
    "sentimiento": "NEGATIVE",
    "confianza": 0.87,
    "texto": "Muy decepcionante"
}
```

---

### `guardar_resultado(resultado)`

Función orquestadora que llama a `guardar_txt` y `guardar_json` en una sola operación. Usa el mismo timestamp para ambos archivos, garantizando coherencia.

```python
from almacenamiento.guardar import guardar_resultado

guardar_resultado(resultado)
# → Crea TXT y JSON con el mismo timestamp
```

---

## Módulo `leer.py`

### `leer_txt(ruta)`

Lee y retorna el contenido de un archivo TXT como string.

```python
from almacenamiento.leer import leer_txt

contenido = leer_txt("resultados/txt/resultado_20260424_133045.txt")
print(contenido)
```

---

### `leer_json(ruta)`

Lee un archivo JSON y retorna el contenido como diccionario Python.

```python
from almacenamiento.leer import leer_json

datos = leer_json("resultados/json/resultado_20260424_133045.json")
print(datos["sentimiento"])  # → "NEGATIVE"
```

---

### Funciones adicionales de `leer.py`

| Función | Descripción |
|---------|-------------|
| `listar_archivos(formato)` | Lista todos los archivos guardados de un formato (`txt` o `json`) |
| `buscar_por_fecha(fecha)` | Filtra archivos por fecha (`YYYYMMDD`) |

---

## Comportamiento ante Errores

| Situación | Comportamiento |
|-----------|---------------|
| Carpeta inexistente | Se crea automáticamente con `os.makedirs` |
| Archivo no encontrado en lectura | Lanza `FileNotFoundError` |
| Resultado `None` | Lanza `ValueError` antes de intentar escribir |
| JSON inválido en lectura | Lanza `json.JSONDecodeError` |

---

## Tests del Módulo

Los tests usan `tmp_path` de pytest para escribir en directorios temporales, sin afectar los resultados reales del proyecto.

```python
def test_guardar_txt(tmp_path):
    resultado = {"nivel": "basico", "sentimiento": "POSITIVE"}
    ruta = tmp_path / "test.txt"
    guardar_txt(resultado, ruta=str(ruta))
    assert ruta.exists()
    assert "POSITIVE" in ruta.read_text(encoding="utf-8")

def test_guardar_json(tmp_path):
    resultado = {"nivel": "basico", "sentimiento": "NEGATIVE"}
    ruta = tmp_path / "test.json"
    guardar_json(resultado, ruta=str(ruta))
    import json
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    assert datos["sentimiento"] == "NEGATIVE"
```
