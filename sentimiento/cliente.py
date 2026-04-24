from transformers import pipeline

_model = None

def get_model():
    global _model
    if _model is None:
        _model = pipeline(
            "sentiment-analysis",
            model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
            revision="af0f99b"
        )
    return _model