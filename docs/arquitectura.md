# 🏗️ Arquitectura del Proyecto

## Visión General

El proyecto **SENTIMIENTOS** sigue una arquitectura modular en capas, aplicando el **patrón Facade** para centralizar el acceso al analizador de sentimientos y desacoplar la lógica interna del punto de entrada.

---

## Diagrama de Módulos

```
┌─────────────────────────────────────────────────────┐
│                      main.py                        │
│           (Punto de entrada de la aplicación)       │
└────────────────────┬────────────────────────────────┘
                     │
          ┌──────────▼──────────┐
          │  sentimiento/        │
          │  analizador.py       │  ← FACADE (API pública)
          └──┬──────────────────┘
             │
     ┌───────┴──────────────────────┐
     │                              │
┌────▼────────┐           ┌─────────▼──────┐
│  cliente.py  │           │   niveles.py   │
│ (get_model) │           │ analizar_basico │
│ Lazy loading │           │ analizar_inter  │
└─────────────┘           │ analizar_avanz  │
                           └────────────────┘
                                   ▲
                          ┌────────┴────────┐
                          │  multitexto.py   │
                          │ analizar_lista   │
                          └─────────────────┘

┌─────────────────────────────────────────────────────┐
│                   almacenamiento/                   │
│   guardar.py                    leer.py             │
│   guardar_txt()                 leer_txt()          │
│   guardar_json()                leer_json()         │
│   guardar_resultado()                               │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                      tests/                         │
│   test_analizador.py        test_guardar.py         │
│   (mocks + monkeypatch)     (tmp_path)              │
└─────────────────────────────────────────────────────┘
```

---

## Capas de la Arquitectura

### 1. Capa de Entrada — `main.py`
Punto de entrada único. Orquesta la llamada al analizador y el guardado de resultados. No contiene lógica de negocio.

### 2. Capa de Servicio — `sentimiento/analizador.py`
Implementa el **patrón Facade**: expone una única función pública (`analizar_por_nivel`) que oculta la complejidad interna. Incluye validaciones de entrada y manejo de casos borde.

### 3. Capa de Modelo — `sentimiento/cliente.py`
Responsable exclusivamente de la carga del modelo `transformers`. Usa **lazy loading**: el modelo no se instancia al importar el módulo, sino solo cuando se necesita, evitando efectos secundarios en los tests.

### 4. Capa de Lógica — `sentimiento/niveles.py`
Contiene las tres funciones de análisis diferenciadas por nivel de detalle. Cada función es pura y recibe el modelo como parámetro (inyección de dependencias).

### 5. Capa de Lote — `sentimiento/multitexto.py`
Permite procesar listas de textos delegando en `analizar_por_nivel`. Sigue el principio de responsabilidad única (SRP).

### 6. Capa de Persistencia — `almacenamiento/`
Gestiona el guardado y lectura de resultados en dos formatos:
- **TXT**: informe legible para humanos
- **JSON**: formato estructurado para integración con otros sistemas

---

## Flujo de Datos

```
Texto de entrada (str)
        │
        ▼
analizar_por_nivel(texto, nivel)
        │
        ├── Validaciones (None, tipo, nivel inválido, vacío)
        │
        ▼
get_model()  ←── lazy loading (solo si texto válido)
        │
        ▼
analizar_basico / intermedio / avanzado (model, texto)
        │
        ▼
dict { nivel, sentimiento, [confianza], [texto] }
        │
        ├── guardar_txt(resultado)  →  resultados/txt/<timestamp>.txt
        └── guardar_json(resultado) →  resultados/json/<timestamp>.json
```

---

## Decisiones de Diseño

| Decisión | Justificación |
|----------|--------------|
| Patrón Facade en `analizador.py` | Punto de acceso único; oculta complejidad interna |
| Lazy loading del modelo | Evita carga en importación; tests más rápidos y limpios |
| Inyección del modelo en `niveles.py` | Facilita mocking en tests sin parchear globales |
| Timestamp en nombres de archivo | Evita sobreescritura; permite histórico de análisis |
| Python 3.11 obligatorio | `transformers 4.41.2` no es compatible con 3.12+ |
| Tests con mocks agresivos | Independencia total de PyTorch/TensorFlow en CI/CD |

---

## Módulos y Responsabilidades

| Módulo | Responsabilidad |
|--------|----------------|
| `sentimiento/cliente.py` | Carga y retorno del modelo de IA |
| `sentimiento/niveles.py` | Lógica de análisis por nivel de detalle |
| `sentimiento/analizador.py` | Facade: validación + enrutamiento por nivel |
| `sentimiento/multitexto.py` | Procesamiento en lote de listas de textos |
| `almacenamiento/guardar.py` | Persistencia de resultados en TXT y JSON |
| `almacenamiento/leer.py` | Lectura y listado de resultados guardados |
| `main.py` | Orquestación y punto de entrada |
| `tests/` | Validación con mocks, monkeypatch y tmp_path |
