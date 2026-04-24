import json
from pathlib import Path

# 📁 Carpetas base
CARPETA_TXT = Path("resultados/txt")
CARPETA_JSON = Path("resultados/json")


# 🧱 FUNCIONES BASE
def leer_txt(ruta):
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")
    return ruta.read_text(encoding="utf-8")


def leer_json(ruta):
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")
    return json.loads(ruta.read_text(encoding="utf-8"))


# 🚀 FUNCIONES DE HISTORIAL
def listar_analisis() -> list:
    """Lista todos los archivos de análisis (TXT y JSON)"""
    archivos = []
    if CARPETA_TXT.exists():
        archivos.extend([str(f.name) for f in CARPETA_TXT.glob("*.txt")])
    if CARPETA_JSON.exists():
        archivos.extend([str(f.name) for f in CARPETA_JSON.glob("*.json")])
    return sorted(archivos)


def listar_archivos(formato: str = "json") -> list:
    """
    Lista archivos de un formato concreto (usado por la interfaz gráfica)
    formato: 'txt' o 'json'
    """
    carpeta = CARPETA_JSON if formato == "json" else CARPETA_TXT
    if not carpeta.exists():
        return []
    return sorted([f.name for f in carpeta.glob(f"*.{formato}")])


def leer_json_por_nombre(nombre: str) -> dict:
    """Lee un JSON desde la carpeta de resultados"""
    ruta = CARPETA_JSON / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {nombre}")
    return leer_json(ruta)


def leer_txt_por_nombre(nombre: str) -> str:
    """Lee un TXT desde la carpeta de resultados"""
    ruta = CARPETA_TXT / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {nombre}")
    return leer_txt(ruta)


def buscar_por_fecha(fecha: str) -> list:
    """Filtra archivos por fecha (formato: YYYY-MM-DD)"""
    return [archivo for archivo in listar_analisis() if fecha in archivo]