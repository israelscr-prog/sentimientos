import os
from almacenamiento.guardar import guardar_txt, guardar_json
from almacenamiento.leer import leer_txt, leer_json


def test_guardar_y_leer_txt(tmp_path):
    ruta = tmp_path / "test.txt"
    data = {"mensaje": "hola"}

    guardar_txt(data, ruta)
    contenido = leer_txt(ruta)

    assert "hola" in contenido


def test_guardar_y_leer_json(tmp_path):
    ruta = tmp_path / "test.json"
    data = {"mensaje": "hola"}

    guardar_json(data, ruta)
    contenido = leer_json(ruta)

    assert contenido["mensaje"] == "hola"