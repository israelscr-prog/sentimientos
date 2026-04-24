python3.11 -m venv env# 🧠 SENTIMIENTOS — Analizador de Sentimientos con IA

Proyecto de refactorización profesional de un analizador de sentimientos basado en IA (`transformers`). Partiendo del código heredado `InicioSentimiento.py`, se ha modularizado la arquitectura, añadido tests, configurado CI/CD y documentado cada fase del proceso.

---

## 📋 Descripción

El proyecto analiza el sentimiento de textos en lenguaje natural (positivo/negativo) usando el modelo preentrenado de HuggingFace `transformers`. Soporta tres niveles de análisis y almacena los resultados en formatos TXT y JSON.

---

## 🗂️ Estructura del Proyecto

```
SENTIMIENTOS/
├── sentimiento/
│   ├── __init__.py
│   ├── cliente.py          # Carga del modelo (lazy loading)
│   ├── analizador.py       # Fachada principal (patrón facade)
│   ├── niveles.py          # Lógica por nivel (básico, intermedio, avanzado)
│   └── multitexto.py       # Procesamiento en lote
├── almacenamiento/
│   ├── __init__.py
│   ├── guardar.py          # Guardar resultados en TXT y JSON
│   └── leer.py             # Leer y listar resultados guardados
├── tests/
│   ├── __init__.py
│   ├── test_analizador.py  # Tests del analizador (con mocks)
│   └── test_guardar.py     # Tests de persistencia (con tmp_path)
├── docs/
│   ├── arquitectura.md
│   ├── api_referencia.md
│   ├── almacenamiento.md
│   └── fases.md
├── legacy/
│   └── InicioSentimiento.py  # Código original heredado
├── resultados/
│   ├── txt/
│   └── json/
├── main.py
├── conftest.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalación

> **Requisito:** Python 3.11 (versiones superiores no son compatibles con `transformers`)

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd SENTIMIENTOS

# 2. Crear entorno virtual
python3.11 -m venv .venv
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\activate          # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## 🚀 Uso

### Ejecución básica

```bash
python main.py
```

### Uso programático

```python
from sentimiento.analizador import analizar_por_nivel

# Nivel básico — solo sentimiento
resultado = analizar_por_nivel("Me encanta este producto", nivel="basico")
# → {'nivel': 'basico', 'sentimiento': 'POSITIVE'}

# Nivel intermedio — sentimiento + confianza
resultado = analizar_por_nivel("El envío tardó demasiado", nivel="intermedio")
# → {'nivel': 'intermedio', 'sentimiento': 'NEGATIVE', 'confianza': 0.998}

# Nivel avanzado — sentimiento + confianza + texto original
resultado = analizar_por_nivel("Calidad aceptable", nivel="avanzado")
# → {'nivel': 'avanzado', 'sentimiento': 'POSITIVE', 'confianza': 0.87, 'texto': 'Calidad aceptable'}
```

### Análisis de múltiples textos

```python
from sentimiento.multitexto import analizar_lista_textos

textos = ["Excelente servicio", "Muy decepcionante", "Normal"]
resultados = analizar_lista_textos(textos, nivel="intermedio")
```

### Guardar y leer resultados

```python
from almacenamiento.guardar import guardar_txt, guardar_json
from almacenamiento.leer import leer_json, leer_txt

# Guardar
guardar_txt(resultado)    # → resultados/txt/resultado_<timestamp>.txt
guardar_json(resultado)   # → resultados/json/resultado_<timestamp>.json

# Leer
datos = leer_json("resultados/json/resultado_20260424_130000.json")
texto = leer_txt("resultados/txt/resultado_20260424_130000.txt")
```

---

## 📊 Niveles de Análisis

| Nivel | Campos devueltos | Descripción |
|-------|-----------------|-------------|
| `basico` | `nivel`, `sentimiento` | Solo etiqueta positivo/negativo |
| `intermedio` | `nivel`, `sentimiento`, `confianza` | Añade puntuación de confianza (0-1) |
| `avanzado` | `nivel`, `sentimiento`, `confianza`, `texto` | Incluye además el texto original |

---

## 🧪 Tests

Los tests están completamente desacoplados del modelo `transformers` mediante `monkeypatch` y `mocks`, lo que garantiza ejecución rápida y determinista sin necesidad de PyTorch/TensorFlow.

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=sentimiento --cov=almacenamiento --cov-report=term-missing

# Verbose
pytest -v
```

### Casos cubiertos

- ✅ Análisis en los tres niveles (básico, intermedio, avanzado)
- ✅ Nivel inválido → `ValueError`
- ✅ Texto `None` → `ValueError`
- ✅ Texto no string → `TypeError`
- ✅ Texto vacío → respuesta neutra
- ✅ Persistencia TXT y JSON (`tmp_path`)
- ✅ Timestamp único (evita sobreescritura)

---

## 🔄 CI/CD — GitHub Actions

El pipeline se ejecuta automáticamente en cada `push` y `pull request`:

- Instalación automática de dependencias
- Ejecución de todos los tests con `pytest`
- Validación en Python 3.11
- Configuración de `PYTHONPATH` para imports correctos

---

## 📦 Dependencias

| Paquete | Versión | Uso |
|---------|---------|-----|
| `transformers` | 4.41.2 | Modelo de análisis de sentimientos |
| `python-dotenv` | 1.0.1 | Gestión de variables de entorno |
| `pytest` | 9.0.2 | Framework de testing |
| `pytest-cov` | 5.0.0 | Cobertura de tests |
| `ruff` | 0.5.0 | Linter y formateador |
| `flake8` | 7.0.0 | Linting adicional |
| `bandit` | 1.7.9 | Análisis de seguridad |

---

## 🏗️ Arquitectura

El proyecto sigue el **patrón Facade** para centralizar la lógica de análisis:

```
main.py
   └── sentimiento.analizador  ← Facade
         ├── sentimiento.cliente   (carga del modelo, lazy loading)
         └── sentimiento.niveles   (lógica por nivel)
              └── sentimiento.multitexto  (procesamiento en lote)

almacenamiento.guardar  ←→  almacenamiento.leer
```

**Decisiones de diseño clave:**
- **Lazy loading del modelo**: el modelo solo se carga cuando se necesita, evitando efectos secundarios en tiempo de importación
- **Validación de entradas**: `None`, no-string y nivel inválido se gestionan con excepciones específicas
- **Caso borde texto vacío**: devuelve sentimiento `neutro` con confianza `0.0`
- **Timestamp automático**: cada resultado guardado tiene nombre único

---

## 📁 Documentación adicional

| Documento | Descripción |
|-----------|-------------|
| [`docs/arquitectura.md`](docs/arquitectura.md) | Diagrama y decisiones de diseño |
| [`docs/api_referencia.md`](docs/api_referencia.md) | Referencia completa de funciones |
| [`docs/almacenamiento.md`](docs/almacenamiento.md) | Módulo de persistencia |
| [`docs/fases.md`](docs/fases.md) | Registro cronológico de todas las fases |

---

## 👤 Autor

Israel C. Rojas - Programador con IA - Hostelero - Emprendedor

Proyecto desarrollado como ejercicio de refactorización profesional para curso de desarrollo con IA.

---

## 📄 Licencia

Uso educativo. Código libre para fines de aprendizaje.
