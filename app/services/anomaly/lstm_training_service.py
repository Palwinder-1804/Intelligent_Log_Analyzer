import os

import joblib


MODEL_DIR = "trained_models"
MODEL_PATH = f"{MODEL_DIR}/lstm_model.keras"

TOKENIZER_PATH = f"{MODEL_DIR}/tokenizer.pkl"


def train_lstm_model(
    tokenizer,
    X,
    y
):
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
    from tensorflow.keras.utils import to_categorical

    vocab_size = len(
        tokenizer.word_index
    ) + 1

    y = to_categorical(
        y,
        num_classes=vocab_size
    )

    model = Sequential([

        Embedding(
            input_dim=vocab_size,
            output_dim=64,
            input_length=X.shape[1]
        ),

        LSTM(
            128,
            return_sequences=True
        ),

        Dropout(0.2),

        LSTM(64),

        Dense(
            vocab_size,
            activation="softmax"
        )
    ])

    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["accuracy"]
    )

    model.fit(
        X,
        y,
        epochs=5,
        batch_size=128,
        validation_split=0.2
    )

    os.makedirs(MODEL_DIR, exist_ok=True)

    model.save(MODEL_PATH)

    joblib.dump(
        tokenizer,
        TOKENIZER_PATH
    )

    return {
        "message": "LSTM model trained successfully"
    }