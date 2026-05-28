import os

import joblib

from app.services.anomaly.lstm_training_service import (
    MODEL_PATH,
    TOKENIZER_PATH,
)

_model = None
_tokenizer = None


def models_exist() -> bool:
    return os.path.isfile(MODEL_PATH) and os.path.isfile(TOKENIZER_PATH)


def get_lstm_model():
    global _model

    if _model is None:
        if not models_exist():
            return None
        from tensorflow.keras.models import load_model
        _model = load_model(MODEL_PATH)

    return _model


def get_tokenizer():
    global _tokenizer

    if _tokenizer is None:
        if not models_exist():
            return None
        _tokenizer = joblib.load(TOKENIZER_PATH)

    return _tokenizer
