import json

def leer_txt(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def leer_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)