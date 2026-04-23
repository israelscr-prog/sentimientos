import pytest
from almacenamiento.guardar import guardar_txt, guardar_json
from almacenamiento.leer import leer_txt, leer_json


# ✅ CASOS FELICES
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


# ⚠️ CASOS BORDE
def test_guardar_diccionario_vacio(tmp_path):
    ruta = tmp_path / "empty.json"
    data = {}

    guardar_json(data, ruta)
    contenido = leer_json(ruta)

    assert contenido == {}


def test_guardar_txt_vacio(tmp_path):
    ruta = tmp_path / "empty.txt"

    guardar_txt({}, ruta)
    contenido = leer_txt(ruta)

    assert contenido != ""


# ❌ CASOS DE ERROR
def test_guardar_tipo_invalido(tmp_path):
    ruta = tmp_path / "fail.json"

    with pytest.raises(TypeError):
        guardar_json("esto no es un dict", ruta)


def test_leer_archivo_inexistente():
    with pytest.raises(FileNotFoundError):
        leer_json("no_existe.json")