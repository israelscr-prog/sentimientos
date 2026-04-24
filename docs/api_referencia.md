# 📖 Referencia de API

Documentación completa de todas las funciones públicas del proyecto SENTIMIENTOS.

---

## Módulo `sentimiento.analizador`

### `analizar_por_nivel(texto, nivel)`

Función principal del proyecto. Analiza el sentimiento de un texto según el nivel de detalle solicitado.

```python
from sentimiento.analizador import analizar_por_nivel

resultado = analizar_por_nivel("Me encanta este producto", nivel="intermedio")
```

**Parámetros:**

| Parámetro | Tipo | Requerido | Defecto | Descripción |
|-----------|------|-----------|---------|-------------|
| `texto` | `str` | ✅ Sí | — | Texto a analizar |
| `nivel` | `str` | ❌ No | `"basico"` | Nivel de análisis: `"basico"`, `"intermedio"`, `"avanzado"` |

**Retorna:** `dict`

| Nivel | Campos del resultado |
|-------|---------------------|
| `basico` | `{"nivel": str, "sentimiento": str}` |
| `intermedio` | `{"nivel": str, "sentimiento": str, "confianza": float}` |
| `avanzado` | `{"nivel": str, "sentimiento": str, "confianza": float, "texto": str}` |

**Excepciones:**

| Excepción | Cuándo se lanza |
|-----------|----------------|
| `ValueError` | `texto` es `None` o `nivel` no es válido |
| `TypeError` | `texto` no es de tipo `str` |

**Caso borde — texto vacío:**
```python
analizar_por_nivel("   ", nivel="basico")
# → {"nivel": "basico", "sentimiento": "neutro", "confianza": 0.0}
```

**Ejemplos:**
```python
# Básico
analizar_por_nivel("Excelente servicio")
# → {"nivel": "basico", "sentimiento": "POSITIVE"}

# Intermedio
analizar_por_nivel("El envío tardó demasiado", nivel="intermedio")
# → {"nivel": "intermedio", "sentimiento": "NEGATIVE", "confianza": 0.997}

# Avanzado
analizar_por_nivel("Calidad aceptable", nivel="avanzado")
# → {"nivel": "avanzado", "sentimiento": "POSITIVE", "confianza": 0.874, "texto": "Calidad aceptable"}

# Nivel inválido → excepción
analizar_por_nivel("Hola", nivel="experto")
# → ValueError: Nivel no válido
```

---

## Módulo `sentimiento.multitexto`

### `analizar_lista_textos(textos, nivel)`

Analiza una lista de textos aplicando el mismo nivel de análisis a todos.

```python
from sentimiento.multitexto import analizar_lista_textos

textos = ["Fantástico", "Horrible", "Normal"]
resultados = analizar_lista_textos(textos, nivel="intermedio")
```

**Parámetros:**

| Parámetro | Tipo | Requerido | Defecto | Descripción |
|-----------|------|-----------|---------|-------------|
| `textos` | `list[str]` | ✅ Sí | — | Lista de textos a analizar |
| `nivel` | `str` | ❌ No | `"basico"` | Nivel de análisis para todos los textos |

**Retorna:** `list[dict]` — Lista de resultados en el mismo orden que la entrada.

**Ejemplo:**
```python
analizar_lista_textos(["Genial", "Pésimo"], nivel="basico")
# → [
#     {"nivel": "basico", "sentimiento": "POSITIVE"},
#     {"nivel": "basico", "sentimiento": "NEGATIVE"}
#   ]
```

---

## Módulo `sentimiento.cliente`

### `get_model()`

Carga y retorna el modelo de análisis de sentimientos de HuggingFace. Implementa **lazy loading**: el modelo se instancia solo cuando se invoca esta función, nunca al importar el módulo.

```python
from sentimiento.cliente import get_model

model = get_model()
```

**Parámetros:** Ninguno

**Retorna:** `transformers.Pipeline` — Pipeline de análisis de sentimientos preentrenado.

> ⚠️ **Nota:** La primera llamada descarga el modelo (~250 MB). Las llamadas posteriores usan la caché local.

---

## Módulo `sentimiento.niveles`

Funciones internas de análisis. **No se recomienda usarlas directamente**; usar `analizar_por_nivel` como punto de acceso.

### `analizar_basico(model, texto)` → `dict`
Retorna `{"nivel": "basico", "sentimiento": str}`.

### `analizar_intermedio(model, texto)` → `dict`
Retorna `{"nivel": "intermedio", "sentimiento": str, "confianza": float}`.

### `analizar_avanzado(model, texto)` → `dict`
Retorna `{"nivel": "avanzado", "sentimiento": str, "confianza": float, "texto": str}`.

---

## Módulo `almacenamiento.guardar`

### `guardar_txt(resultado, ruta)`

Guarda un resultado de análisis en formato TXT legible.

```python
from almacenamiento.guardar import guardar_txt

guardar_txt({"nivel": "basico", "sentimiento": "POSITIVE"})
```

**Parámetros:**

| Parámetro | Tipo | Requerido | Defecto | Descripción |
|-----------|------|-----------|---------|-------------|
| `resultado` | `dict` | ✅ Sí | — | Resultado del análisis |
| `ruta` | `str` | ❌ No | Auto-generada con timestamp | Ruta del archivo de salida |

**Retorna:** `None`. Crea el archivo en `resultados/txt/`.

---

### `guardar_json(resultado, ruta)`

Guarda un resultado de análisis en formato JSON estructurado.

```python
from almacenamiento.guardar import guardar_json

guardar_json({"nivel": "intermedio", "sentimiento": "NEGATIVE", "confianza": 0.99})
```

**Parámetros:**

| Parámetro | Tipo | Requerido | Defecto | Descripción |
|-----------|------|-----------|---------|-------------|
| `resultado` | `dict` | ✅ Sí | — | Resultado del análisis |
| `ruta` | `str` | ❌ No | Auto-generada con timestamp | Ruta del archivo de salida |

**Retorna:** `None`. Crea el archivo en `resultados/json/`.

---

### `guardar_resultado(resultado)`

Orquestador: llama a `guardar_txt` y `guardar_json` con el mismo timestamp.

```python
from almacenamiento.guardar import guardar_resultado

guardar_resultado(resultado)
```

**Parámetros:** `resultado` (`dict`) — Resultado del análisis.

**Retorna:** `None`.

---

## Módulo `almacenamiento.leer`

### `leer_txt(ruta)` → `str`

Lee y retorna el contenido de un archivo TXT.

```python
from almacenamiento.leer import leer_txt
contenido = leer_txt("resultados/txt/resultado_20260424_130000.txt")
```

---

### `leer_json(ruta)` → `dict`

Lee un archivo JSON y retorna el contenido como diccionario.

```python
from almacenamiento.leer import leer_json
datos = leer_json("resultados/json/resultado_20260424_130000.json")
```

---

## Resumen de Funciones Públicas

| Función | Módulo | Uso recomendado |
|---------|--------|----------------|
| `analizar_por_nivel(texto, nivel)` | `sentimiento.analizador` | ✅ Análisis individual |
| `analizar_lista_textos(textos, nivel)` | `sentimiento.multitexto` | ✅ Análisis en lote |
| `guardar_txt(resultado, ruta)` | `almacenamiento.guardar` | ✅ Persistencia TXT |
| `guardar_json(resultado, ruta)` | `almacenamiento.guardar` | ✅ Persistencia JSON |
| `guardar_resultado(resultado)` | `almacenamiento.guardar` | ✅ Persistencia ambos formatos |
| `leer_txt(ruta)` | `almacenamiento.leer` | ✅ Lectura TXT |
| `leer_json(ruta)` | `almacenamiento.leer` | ✅ Lectura JSON |
| `get_model()` | `sentimiento.cliente` | ⚠️ Uso interno |
| `analizar_basico/intermedio/avanzado` | `sentimiento.niveles` | ⚠️ Uso interno |
