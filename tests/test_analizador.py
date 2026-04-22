import pytest
from sentimiento.analizador import analizar_por_nivel


# 🔧 Mock del modelo (simula transformers)
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


def test_analizar_basico(mock_model):
    resultado = analizar_por_nivel("Me encanta esto", "basico")

    assert resultado["nivel"] == "basico"
    assert "sentimiento" in resultado


def test_analizar_intermedio(mock_model):
    resultado = analizar_por_nivel("Me encanta esto", "intermedio")

    assert resultado["nivel"] == "intermedio"
    assert "confianza" in resultado


def test_analizar_avanzado(mock_model):
    resultado = analizar_por_nivel("Me encanta esto", "avanzado")

    assert resultado["nivel"] == "avanzado"
    assert "texto" in resultado


def test_nivel_invalido(mock_model):
    with pytest.raises(ValueError):
        analizar_por_nivel("texto", "ultra")