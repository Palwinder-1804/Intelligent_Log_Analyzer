import numpy as np

from app.services.anomaly.embedding_anomaly_service import (
    generate_embedding,
)
from app.services.anomaly.model_loader_service import (
    get_lstm_model,
    get_tokenizer,
    models_exist,
)
from app.services.anomaly.semantic_similarity_service import (
    calculate_similarity,
)
from app.services.anomaly.sequence_builder_service import (
    WINDOW_SIZE,
)
from app.services.rag.vector_store_service import log_vector_store

NEUTRAL_SCORE = 0.5


def _prepare_event_tokens(log: str) -> list[str]:
    tokens = log.strip().split()
    if not tokens:
        return [log.strip()] if log.strip() else []
    return tokens


def _lstm_prediction_confidence(log: str) -> float:
    if not models_exist():
        return NEUTRAL_SCORE

    model = get_lstm_model()
    tokenizer = get_tokenizer()

    if model is None or tokenizer is None:
        return NEUTRAL_SCORE

    tokens = _prepare_event_tokens(log)
    sequences = tokenizer.texts_to_sequences([tokens])

    if not sequences or not sequences[0]:
        return NEUTRAL_SCORE

    event_sequence = sequences[0]
    if len(event_sequence) > WINDOW_SIZE:
        event_sequence = event_sequence[-WINDOW_SIZE:]

    from tensorflow.keras.preprocessing.sequence import pad_sequences
    padded_sequence = pad_sequences(
        [event_sequence],
        maxlen=WINDOW_SIZE,
        padding="post",
    )

    prediction = model.predict(padded_sequence, verbose=0)

    return float(np.max(prediction))


def detect_anomaly(log: str):
    prediction_confidence = _lstm_prediction_confidence(log)

    current_embedding = generate_embedding(log)

    retrieved_docs = log_vector_store.similarity_search(log, k=5)

    historical_logs = [doc.page_content for doc in retrieved_docs]

    if historical_logs:
        historical_embeddings = [
            generate_embedding(log_text) for log_text in historical_logs
        ]
        similarity_score = calculate_similarity(
            current_embedding,
            historical_embeddings,
        )
    else:
        similarity_score = NEUTRAL_SCORE

    anomaly_score = (1 - prediction_confidence) + (1 - similarity_score)

    is_anomaly = anomaly_score > 0.8

    severity = "LOW"

    if anomaly_score > 1.4:
        severity = "CRITICAL"
    elif anomaly_score > 1.1:
        severity = "HIGH"
    elif anomaly_score > 0.8:
        severity = "MEDIUM"

    return {
        "log": log,
        "prediction_confidence": float(prediction_confidence),
        "semantic_similarity": float(similarity_score),
        "anomaly_score": float(anomaly_score),
        "is_anomaly": bool(is_anomaly),
        "severity": severity,
        "lstm_available": bool(models_exist()),
    }
