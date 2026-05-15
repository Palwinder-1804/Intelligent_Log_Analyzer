from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

import numpy as np

WINDOW_SIZE = 5


def build_sequences(event_traces):
    flattened_sequences = []

    for trace in event_traces:
        if len(trace) <= WINDOW_SIZE:
            continue

        for i in range(len(trace) - WINDOW_SIZE):
            sequence = trace[i : i + WINDOW_SIZE + 1]
            flattened_sequences.append(sequence)

    if not flattened_sequences:
        raise ValueError(
            "No training sequences built. Each trace must contain more than "
            f"{WINDOW_SIZE} events. Check that the dataset loader reads the "
            "correct column (HDFS CSV uses 'Features')."
        )

    tokenizer = Tokenizer(filters="")
    tokenizer.fit_on_texts(flattened_sequences)

    sequences = tokenizer.texts_to_sequences(flattened_sequences)
    sequences = pad_sequences(
        sequences,
        maxlen=WINDOW_SIZE + 1,
        padding="post",
        truncating="post",
    )

    X = sequences[:, :-1]
    y = sequences[:, -1]

    return tokenizer, X, y
