# 🖥️ Interfaz Gráfica — `sentimiento/interfaz.py`

Documentación técnica del módulo de interfaz gráfica desarrollado con **Tkinter**.

---

## Descripción

La interfaz gráfica permite al usuario analizar textos en tiempo real, visualizar los resultados en tres niveles de detalle, consultar el historial de análisis guardados y guardar resultados manualmente. Está implementada como una clase Python que encapsula toda la lógica visual y de interacción.

---
## Componentes de la interfaz

| Componente | Descripción | Funcional |
|------------|-------------|:-----------:|
| Área de texto de entrada | Campo para introducir el texto a analizar | ✅ |
| Botón Analizar Sentimiento | Lanza el análisis en los 3 niveles | ✅ |
| Botón Limpiar | Limpia todos los campos | ✅ |
| Botón Guardar | Guarda manualmente en TXT y JSON | ✅ |
| Pestaña Resultados por Nivel | Tabla con Básico / Intermedio / Avanzado | ✅ |
| Pestaña Análisis Detallado | Emociones y polaridad extendida | ✅ |
| Pestaña Justificación | Explicación del análisis + recomendación | ✅ |
| Pestaña Historial | Lista de análisis guardados | ✅ |
| Panel ¿Qué significa la polaridad? | Leyenda explicativa | ✅ |
| Barra de estado | Confirma guardado automático | ✅ |
---

## Instalación de Tkinter

Tkinter viene **incluido con Python**, no requiere instalación con `pip`.

| Sistema | Comando |
|---------|---------|
| **Windows** | No requiere instalación. Verificar con `python -m tkinter` |
| **Linux (Ubuntu/Debian)** | `sudo apt-get install python3-tk` |
| **macOS (Homebrew)** | `brew install python-tk@3.11` |

> ⚠️ No añadir `tkinter` al `requirements.txt` — es parte de la librería estándar de Python.

---

## Estructura del archivo

```
sentimiento/
└── interfaz.py
```

El módulo exporta una única función pública:

```python
from sentimiento.interfaz import iniciar_interfaz

iniciar_interfaz()
```

---

## Imports y dependencias

```python
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import threading

from sentimiento.analizador import analizar_por_nivel
from almacenamiento.guardar import guardar_resultado
from almacenamiento.leer import leer_json, listar_archivos
```

| Import | Propósito |
|--------|-----------|
| `tkinter as tk` | Librería base — ventanas, botones, labels |
| `ttk` | Widgets mejorados — `Notebook` (pestañas) y `Treeview` (tabla) |
| `scrolledtext` | Campo de texto con scroll integrado |
| `messagebox` | Ventanas emergentes de aviso y error |
| `datetime` | Generación del timestamp del análisis |
| `threading` | Análisis en hilo paralelo para no bloquear la GUI |
| `analizar_por_nivel` | Lógica de análisis (módulo `sentimiento`) |
| `guardar_resultado` | Persistencia de resultados (módulo `almacenamiento`) |
| `listar_archivos` | Lectura del historial (módulo `almacenamiento`) |

---

## Clase `AplicacionSentimiento`

### `__init__(self, root)`

Constructor de la aplicación. Recibe la ventana principal de Tkinter, configura título y tamaño, y delega la construcción visual a `_construir_ui()`.

```python
def __init__(self, root):
    self.root = root
    self.root.title("Análisis de Sentimiento - Local")
    self.root.geometry("940x700")
    self._construir_ui()
```

---

### `_construir_ui()`

Método principal de construcción visual. Ensambla todos los componentes de arriba a abajo, en el mismo orden en que aparecen en pantalla:

```
_construir_ui()
   ├── Label título
   ├── LabelFrame + ScrolledText     → entrada de texto
   ├── Frame + 3 Buttons             → Analizar / Limpiar / Guardar
   ├── Notebook (pestañas)
   │     ├── _construir_tab_niveles()
   │     ├── _construir_tab_detallado()
   │     ├── _construir_tab_justificacion()
   │     └── _construir_tab_historial()
   ├── LabelFrame leyenda polaridad
   └── Label barra de estado (StringVar reactiva)
```

**Variables de instancia inicializadas aquí:**

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `self.texto_entrada` | `ScrolledText` | Campo de texto de entrada |
| `self.notebook` | `ttk.Notebook` | Contenedor de pestañas |
| `self.barra_estado` | `StringVar` | Texto reactivo de la barra inferior |
| `self.ultimo_resultado` | `dict` / `None` | Último análisis realizado |

---

## Componentes de la interfaz

### Área de texto — `LabelFrame` + `ScrolledText`

```python
frame_texto = tk.LabelFrame(self.root, text="Texto a analizar", padx=5, pady=5)
self.texto_entrada = scrolledtext.ScrolledText(frame_texto, height=5, wrap="word")
```

- `LabelFrame`: contenedor con borde y título visible
- `wrap="word"`: el texto salta de línea por palabras, no por caracteres
- Se guarda en `self` porque `_analizar()` necesita leerlo

---

### Botones

```python
tk.Button(frame_botones, text="🔍 ANALIZAR SENTIMIENTO",
          command=self._analizar, bg="#d0e8ff")
tk.Button(frame_botones, text="🧹 LIMPIAR",
          command=self._limpiar)
tk.Button(frame_botones, text="💾 GUARDAR",
          command=self._guardar_manual)
```

- `command=self._metodo` conecta cada botón con su función
- `side="left"` coloca los tres botones en fila horizontal

---

### Pestañas — `ttk.Notebook`

```python
self.notebook = ttk.Notebook(self.root)
self.tab_niveles = ttk.Frame(self.notebook)
self.notebook.add(self.tab_niveles, text="📊 Resultados por Nivel")
```

Cada pestaña es un `Frame` vacío que se rellena con su método `_construir_tab_*()`.
`fill="both", expand=True` hace que ocupen todo el espacio disponible.

| Pestaña | Widget interior | Se rellena en |
|---------|----------------|---------------|
| Resultados por Nivel | `Treeview` (tabla) | `_actualizar_ui()` |
| Análisis Detallado | `ScrolledText` | `_actualizar_ui()` |
| Justificación & Recomendación | `ScrolledText` | `_actualizar_ui()` |
| Historial | `Listbox` | `_cargar_historial()` |

---

### Tabla de resultados — `ttk.Treeview`

```python
cols = ("Nivel", "Sentimiento", "Polaridad", "Intensidad")
self.tabla = ttk.Treeview(self.tab_niveles, columns=cols, show="headings", height=6)
```

- `show="headings"`: oculta la columna de árbol por defecto
- Las filas se insertan en `_actualizar_ui()` con colores según sentimiento:
  - 🟢 Fondo verde (`#e8f5e9`) para `POSITIVE`
  - 🔴 Fondo rojo (`#ffebee`) para `NEGATIVE`

---

### Barra de estado — `StringVar`

```python
self.barra_estado = tk.StringVar(value="Listo")
tk.Label(self.root, textvariable=self.barra_estado, relief="sunken", anchor="w")
```

`StringVar` es una variable reactiva de Tkinter: al llamar `self.barra_estado.set("texto")` desde cualquier método, el Label se actualiza automáticamente en pantalla sin manipular el widget directamente.

---

## Flujo de ejecución al pulsar "Analizar"

```
Clic en "ANALIZAR SENTIMIENTO"
        │
        ▼
_analizar()
  └── Lee self.texto_entrada
  └── Lanza threading.Thread → _ejecutar_analisis(texto)
                                        │
                          (hilo paralelo, GUI no se congela)
                                        │
                          analizar_por_nivel(texto, "basico")
                          analizar_por_nivel(texto, "intermedio")
                          analizar_por_nivel(texto, "avanzado")
                                        │
                          guardar_resultado(ultimo_resultado)
                                        │
                          root.after(0, _actualizar_ui)   ← vuelve al hilo principal
                                        │
                          Actualiza tabla, textos y barra de estado
```

> 💡 `root.after(0, funcion)` es la forma segura de actualizar la UI desde un hilo secundario en Tkinter. Nunca se deben modificar widgets directamente desde un hilo que no sea el principal.

---

## Función pública `iniciar_interfaz()`

```python
def iniciar_interfaz():
    root = tk.Tk()
    AplicacionSentimiento(root)
    root.mainloop()
```

- `tk.Tk()` crea la ventana principal del sistema operativo
- `mainloop()` inicia el bucle de eventos de Tkinter — la aplicación queda viva esperando acciones del usuario hasta que se cierra la ventana
