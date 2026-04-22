from sentimiento.analizador import analizar_por_nivel
from almacenamiento.guardar import guardar_json, guardar_txt

def main():
    texto = "El producto llegó rápido, pero la calidad no es lo que esperaba."

    resultado = analizar_por_nivel(texto, nivel="intermedio")

    print(resultado)

    guardar_txt(resultado)
    guardar_json(resultado)


if __name__ == "__main__":
    main()