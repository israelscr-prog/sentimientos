import pytest
from sentimiento.analizador import analizar_por_nivel

class MockPipeline:
    """Mock de pipeline que simula sentiment-analysis"""
    def __call__(self, texto):
        return [{"label": "POSITIVE", "score": 0.95}]

@pytest.fixture
def mock_get_model(monkeypatch):
    """Mock de get_model() que devuelve nuestro MockPipeline"""
    def mock_get_model():
        return MockPipeline()
    
    monkeypatch.setattr("sentimiento.cliente.get_model", mock_get_model)

# ===========================================
# CASOS FELICES (Happy Path)
# ===========================================
def test_flujo_normal_basico(mock_get_model):
    """Test básico: texto positivo → resultado correcto"""
    resultado = analizar_por_nivel("Me encanta esto", "basico")
    assert resultado["nivel"] == "basico"
    assert resultado["sentimiento"] == "POSITIVE"

def test_flujo_normal_intermedio(mock_get_model):
    """Test intermedio: texto positivo → nivel correcto + confianza float"""
    resultado = analizar_por_nivel("Me encanta esto", "intermedio")
    assert resultado["nivel"] == "intermedio"
    assert isinstance(resultado["confianza"], float)

# ===========================================
# CASOS BORDE (Edge Cases)
# ===========================================
def test_texto_vacio(mock_get_model):
    """Texto vacío → neutro con confianza 0.0"""
    resultado = analizar_por_nivel("", "basico")
    assert resultado["sentimiento"] == "neutro"
    assert resultado["confianza"] == 0.0
    assert resultado["nivel"] == "basico"

def test_texto_largo(mock_get_model):
    """Texto muy largo → procesa correctamente"""
    texto = "bien " * 500  # 2000+ caracteres
    resultado = analizar_por_nivel(texto, "basico")
    assert "sentimiento" in resultado
    assert resultado["nivel"] == "basico"
    assert resultado["sentimiento"] == "POSITIVE"  # del mock

# ===========================================
# CASOS DE ERROR (Error Cases)
# ===========================================
def test_texto_none(mock_get_model):
    """None → ValueError"""
    with pytest.raises(ValueError, match="El texto no puede ser None"):
        analizar_por_nivel(None, "basico")

def test_nivel_invalido(mock_get_model):
    """Nivel inválido → ValueError"""
    with pytest.raises(ValueError, match="Nivel no válido"):
        analizar_por_nivel("texto", "ultra")

def test_tipo_incorrecto_texto(mock_get_model):
    """Número en lugar de string → TypeError"""
    with pytest.raises(TypeError, match="El texto debe ser un string"):
        analizar_por_nivel(123, "basico")