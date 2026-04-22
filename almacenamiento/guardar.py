import json

def guardar_txt(resultado, ruta="resultado.txt"):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(str(resultado))


def guardar_json(resultado, ruta="resultado.json"):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)