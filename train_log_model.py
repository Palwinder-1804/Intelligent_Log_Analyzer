import os

os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

from app.services.anomaly.dataset_loader_service import (
    load_event_traces
)

from app.services.anomaly.sequence_builder_service import (
    build_sequences
)

from app.services.anomaly.lstm_training_service import (
    train_lstm_model
)


HDFS_TRACE_PATH = (
    "datasets/hdfs/Event_traces.csv"
)


def main():

    event_traces = load_event_traces(
        HDFS_TRACE_PATH
    )

    tokenizer, X, y = build_sequences(
        event_traces
    )

    result = train_lstm_model(
        tokenizer,
        X,
        y
    )

    print(result)


if __name__ == "__main__":
    main()