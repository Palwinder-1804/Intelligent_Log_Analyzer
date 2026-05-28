import os

# Suppress TensorFlow oneDNN info logs and optimize CPU memory/threads
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
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