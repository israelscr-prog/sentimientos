import json
from datetime import datetime
from pathlib import Path


# 📁 Carpetas base
CARPETA_TXT = Path("resultados/txt")
CARPETA_JSON = Path("resultados/json")


# 🕒 Generar timestamp único
def _generar_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


# 📁 Crear carpetas si no existen
def _crear_carpetas():
    CARPETA_TXT.mkdir(parents=True, exist_ok=True)
    CARPETA_JSON.mkdir(parents=True, exist_ok=True)


# 🧱 Guardar TXT (función testable)
def guardar_txt(resultado: dict, ruta: Path):
    if not isinstance(resultado, dict):
        raise TypeError("El resultado debe ser un diccionario")

    if "mensaje" in resultado:
        contenido = resultado["mensaje"]
    else:
        texto = resultado.get("texto", "")
        basico = resultado.get("basico", {})
        intermedio = resultado.get("intermedio", {})
        avanzado = resultado.get("avanzado", {})

        contenido = f"""
============================================
ANÁLISIS DE SENTIMIENTO
============================================

TEXTO ANALIZADO:
{texto}

RESULTADO BÁSICO: {basico.get("sentimiento", "N/A")}
RESULTADO INTERMEDIO: {intermedio.get("sentimiento", "N/A")}
JUSTIFICACIÓN: {avanzado.get("justificacion", "N/A")}
"""

    ruta.write_text(contenido.strip(), encoding="utf-8")
    return ruta


# 🧱 Guardar JSON (función testable)
def guardar_json(resultado: dict, ruta: Path):
    if not isinstance(resultado, dict):
        raise TypeError("El resultado debe ser un diccionario")

    if "mensaje" in resultado or resultado == {}:
        data = resultado
    else:
        data = {
            "timestamp": _generar_timestamp(),
            "texto": resultado.get("texto", ""),
            "basico": resultado.get("basico", {}),
            "intermedio": resultado.get("intermedio", {}),
            "avanzado": resultado.get("avanzado", {}),
        }

    ruta.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")
    return ruta


# 🚀 FUNCIÓN PRINCIPAL 
def guardar_resultado(texto_entrada: str, resultados: dict) -> dict:
    """
    Orquesta el guardado en TXT y JSON.

    - Crea carpetas si no existen
    - Usa timestamp único
    - No sobreescribe archivos
    """

    _crear_carpetas()

    timestamp = _generar_timestamp()
    nombre_base = f"analisis_{timestamp}"

    ruta_txt = CARPETA_TXT / f"{nombre_base}.txt"
    ruta_json = CARPETA_JSON / f"{nombre_base}.json"

    # Añadir texto al resultado
    resultados["texto"] = texto_entrada

    guardar_txt(resultados, ruta_txt)
    guardar_json(resultados, ruta_json)

    return {
        "txt": str(ruta_txt),
        "json": str(ruta_json)
    }