import pytest
from unittest.mock import MagicMock
from sentimiento.analizador import analizar_por_nivel

@pytest.fixture(autouse=True)  # ← SE EJECUTA AUTOMÁTICAMENTE EN TODOS LOS TESTS
def mock_pipeline_global(monkeypatch):
    """Mock AGRESIVO que bloquea transformers ANTES de que se cargue"""
    
    # Mock 1: Intercepta get_model() DONDE SE USA
    def mock_get_model():
        class MockPipeline:
            def __call__(self, texto, **kwargs):
                return [{"label": "POSITIVE", "score": 0.95}]
        return MockPipeline()
    
    # Mock 2: Intercepta pipeline() directamente (doble seguridad)
    def mock_pipeline(*args, **kwargs):
        class MockPipeline:
            def __call__(self, texto, **kwargs):
                return [{"label": "POSITIVE", "score": 0.95}]
        return MockPipeline()
    
    # ✅ CAMBIO CLAVE: parchea DONDE SE IMPORTA/USO
    monkeypatch.setattr("sentimiento.analizador.get_model", mock_get_model)
    monkeypatch.setattr("transformers.pipelines.pipeline", mock_pipeline)

# ===========================================
# CASOS FELICES (Happy Path)
# ===========================================
def test_flujo_normal_basico(mock_pipeline_global):
    """Test básico: texto positivo → resultado correcto"""
    resultado = analizar_por_nivel("Me encanta esto", "basico")
    assert resultado["nivel"] == "basico"
    assert resultado["sentimiento"] == "POSITIVE"

def test_flujo_normal_intermedio(mock_pipeline_global):
    """Test intermedio: texto positivo → nivel correcto + confianza float"""
    resultado = analizar_por_nivel("Me encanta esto", "intermedio")
    assert resultado["nivel"] == "intermedio"
    assert isinstance(resultado["confianza"], float)

# ===========================================
# CASOS BORDE (Edge Cases)
# ===========================================
def test_texto_vacio(mock_pipeline_global):
    """Texto vacío → neutro con confianza 0.0"""
    resultado = analizar_por_nivel("", "basico")
    assert resultado["sentimiento"] == "neutro"
    assert resultado["confianza"] == 0.0
    assert resultado["nivel"] == "basico"

def test_texto_largo(mock_pipeline_global):
    """Texto muy largo → procesa correctamente"""
    texto = "bien " * 500  # 2000+ caracteres
    resultado = analizar_por_nivel(texto, "basico")
    assert resultado["nivel"] == "basico"
    assert resultado["sentimiento"] == "POSITIVE"

# ===========================================
# CASOS DE ERROR (Error Cases)
# ===========================================
def test_texto_none(mock_pipeline_global):
    """None → ValueError"""
    with pytest.raises(ValueError, match="El texto no puede ser None"):
        analizar_por_nivel(None, "basico")

def test_nivel_invalido(mock_pipeline_global):
    """Nivel inválido → ValueError"""
    with pytest.raises(ValueError, match="Nivel no válido"):
        analizar_por_nivel("texto", "ultra")

def test_tipo_incorrecto_texto(mock_pipeline_global):
    """Número en lugar de string → TypeError"""
    with pytest.raises(TypeError, match="El texto debe ser un string"):
        analizar_por_nivel(123, "basico")