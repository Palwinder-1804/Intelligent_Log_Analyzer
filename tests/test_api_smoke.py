from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestPublicEndpoints:
    def test_health_root(self, client):
        response = client.get("/")

        assert response.status_code == 200
        assert "message" in response.json()


class TestAnomalyEndpoint:
    def test_detect_anomaly(self, client, auth_headers):
        with (
            patch(
                "app.services.anomaly.hybrid_detection_service.log_vector_store"
            ) as mock_store,
            patch(
                "app.api.routes.anomaly.store_anomaly",
                new_callable=AsyncMock,
            ),
        ):
            mock_store.similarity_search.return_value = []

            response = client.post(
                "/anomaly/detect",
                json={"log": "E5 E22 E5 E26 E5 E11"},
                headers=auth_headers,
            )

        assert response.status_code == 200
        body = response.json()
        assert "anomaly_score" in body
        assert "is_anomaly" in body
        assert "severity" in body
        assert "lstm_available" in body

    def test_detect_requires_auth(self, app, client):
        from app.api.dependencies.auth_dependency import get_current_user

        app.dependency_overrides.pop(get_current_user, None)

        response = client.post(
            "/anomaly/detect",
            json={"log": "test log"},
        )

        assert response.status_code in (401, 403)


class TestRagEndpoint:
    def test_rag_search(self, client, auth_headers):
        mock_doc = MagicMock()
        mock_doc.page_content = "sample log chunk"
        mock_doc.metadata = {"source": "hdfs"}

        with patch(
            "app.services.rag.retrieval_service.log_vector_store"
        ) as mock_store:
            mock_store.similarity_search.return_value = [mock_doc]

            response = client.post(
                "/rag/search?query=disk+failure",
                headers=auth_headers,
            )

        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "disk failure"
        assert len(data["results"]) == 1


class TestRcaEndpoint:
    def test_rca_analyze(self, client, auth_headers):
        mock_logs = [
            {
                "service": "hdfs-datanode",
                "message": "disk failure on datanode",
                "timestamp": "2024-01-01 12:00:00",
                "parsed": True,
            }
        ]

        async def mock_find():
            for log in mock_logs:
                yield log

        mock_cursor = MagicMock()
        mock_cursor.__aiter__ = lambda self: mock_find()

        with patch(
            "app.services.rca.root_cause_service.parsed_logs_collection"
        ) as mock_collection:
            mock_collection.find.return_value = mock_cursor

            response = client.post(
                "/rca/analyze",
                json={"query": "disk failure"},
                headers=auth_headers,
            )

        assert response.status_code == 200
        body = response.json()
        assert body["query"] == "disk failure"
        assert "probable_root_cause" in body
        assert "timeline" in body


class TestModuleImports:
    def test_embedding_service_exports_model(self):
        from app.services.rag.embedding_service import embedding_model

        assert embedding_model is not None

    def test_rca_schema_import(self):
        from app.schemas.rca_schema import RCARequest

        assert RCARequest.model_fields["query"]
