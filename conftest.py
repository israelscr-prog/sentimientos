# conftest.py
import warnings

def pytest_configure():
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        module="transformers.models.bert.tokenization_bert",
    )