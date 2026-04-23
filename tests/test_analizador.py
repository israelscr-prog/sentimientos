import pytest
from sentimiento.analizador import analizar_por_nivel


class MockModel:
    def __call__(self, texto):
        return [{
            "label": "POSITIVE",
            "score": 0.95
        }]


@pytest.fixture
def mock_model(monkeypatch):
    from sentimiento import analizador
    monkeypatch.setattr(analizador, "model", MockModel())


# ✅ CASOS FELICES
def test_flujo_normal_basico(mock_model):
    resultado = analizar_por_nivel("Me encanta esto", "basico")

    assert resultado["nivel"] == "basico"
    assert resultado["sentimiento"] == "POSITIVE"


def test_flujo_normal_intermedio(mock_model):
    resultado = analizar_por_nivel("Me encanta esto", "intermedio")

    assert resultado["nivel"] == "intermedio"
    assert isinstance(resultado["confianza"], float)


# ⚠️ CASOS BORDE
def test_texto_vacio(mock_model):
    resultado = analizar_por_nivel("", "basico")

    assert resultado["sentimiento"] in ["POSITIVE", "NEGATIVE"]


def test_texto_largo(mock_model):
    texto = "bien " * 1000
    resultado = analizar_por_nivel(texto, "basico")

    assert "sentimiento" in resultado


# ❌ CASOS DE ERROR
def test_texto_none(mock_model):
    with pytest.raises(ValueError):
        analizar_por_nivel(None, "basico")


def test_nivel_invalido(mock_model):
    with pytest.raises(ValueError):
        analizar_por_nivel("texto", "ultra")


def test_tipo_incorrecto_texto(mock_model):
    with pytest.raises(TypeError):
        analizar_por_nivel(123, "basico")