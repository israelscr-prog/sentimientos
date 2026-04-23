import json
import os
from datetime import datetime


def _generar_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


def _asegurar_directorio(ruta):
    os.makedirs(ruta, exist_ok=True)


def guardar_txt(resultado: dict, ruta: str = None):
    if not isinstance(resultado, dict):
        raise TypeError("El resultado debe ser un diccionario")

    if ruta is None:
        timestamp = _generar_timestamp()
        carpeta = "resultados/txt"
        _asegurar_directorio(carpeta)
        ruta = os.path.join(carpeta, f"analisis_{timestamp}.txt")
    else:
        ruta = str(ruta)

    # 🔥 SOPORTE FLEXIBLE
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

RESULTADO BÁSICO:    {basico.get("sentimiento", "N/A")}

RESULTADO INTERMEDIO: {intermedio.get("sentimiento", "N/A")} | \
polaridad: {intermedio.get("polaridad", "N/A")} | \
intensidad: {intermedio.get("intensidad", "N/A")}

JUSTIFICACIÓN:       {avanzado.get("justificacion", "N/A")}
"""

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido.strip())

    return ruta


def guardar_json(resultado: dict, ruta: str = None):
    if not isinstance(resultado, dict):
        raise TypeError("El resultado debe ser un diccionario")

    if ruta is None:
        timestamp = _generar_timestamp()
        carpeta = "resultados/json"
        _asegurar_directorio(carpeta)
        ruta = os.path.join(carpeta, f"analisis_{timestamp}.json")
    else:
        ruta = str(ruta)

    # 🔥 SOPORTE FLEXIBLE
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

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return ruta