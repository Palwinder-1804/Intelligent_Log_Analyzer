import os

import numpy as np
import pytest

from app.services.anomaly.dataset_loader_service import load_event_traces
from app.services.anomaly.log_template_service import normalize_log
from app.services.anomaly.model_loader_service import models_exist
from app.services.anomaly.semantic_similarity_service import calculate_similarity
from app.services.anomaly.sequence_builder_service import WINDOW_SIZE, build_sequences
from app.services.parsing.log_parser_service import parse_log_line
from app.schemas.anomaly_schema import AnomalyDetectRequest
from app.schemas.rca_schema import RCARequest


HDFS_TRACE_PATH = "datasets/hdfs/Event_traces.csv"


class TestLogParser:
    def test_parses_structured_log(self):
        line = "2024-01-15 10:30:00 ERROR auth-service Login failed from 192.168.1.5"
        result = parse_log_line(line)

        assert result["parsed"] is True
        assert result["level"] == "ERROR"
        assert result["service"] == "auth-service"
        assert result["ip_address"] == "192.168.1.5"

    def test_unparsed_log_returns_raw(self):
        result = parse_log_line("random unstructured log line")

        assert result["parsed"] is False
        assert result["raw_log"] == "random unstructured log line"


class TestLogTemplate:
    def test_normalizes_ip_and_numbers(self):
        log = "Connection from 10.0.0.1 failed after 3 retries"
        normalized = normalize_log(log)

        assert "<ip>" in normalized
        assert "<num>" in normalized
        assert "10.0.0.1" not in normalized


class TestSequenceBuilder:
    def test_builds_sequences_with_correct_window(self):
        traces = [["E1", "E2", "E3", "E4", "E5", "E6", "E7"]]
        tokenizer, X, y = build_sequences(traces)

        assert X.shape[1] == WINDOW_SIZE
        assert len(y) == X.shape[0]
        assert len(tokenizer.word_index) > 0


class TestDatasetLoader:
    def test_loads_hdfs_event_traces(self):
        if not os.path.isfile(HDFS_TRACE_PATH):
            pytest.skip("HDFS dataset not present")

        traces = load_event_traces(HDFS_TRACE_PATH)

        assert len(traces) > 0
        assert isinstance(traces[0], list)
        assert len(traces[0]) > WINDOW_SIZE
        assert traces[0][0].startswith("E")


class TestSemanticSimilarity:
    def test_returns_max_similarity(self):
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([0.0, 1.0, 0.0])
        c = np.array([0.9, 0.1, 0.0])

        score = calculate_similarity(a, [b, c])

        assert 0.0 <= score <= 1.0
        assert score > calculate_similarity(a, [b])


class TestSchemas:
    def test_anomaly_detect_request(self):
        req = AnomalyDetectRequest(log="E1 E2 E3")
        assert req.log == "E1 E2 E3"

    def test_rca_request(self):
        req = RCARequest(query="disk failure")
        assert req.query == "disk failure"


class TestModelLoader:
    def test_models_exist_returns_bool(self):
        assert isinstance(models_exist(), bool)
