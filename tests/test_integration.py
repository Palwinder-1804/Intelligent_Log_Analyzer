import os

import pytest
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from app.core.config import settings


def _mongo_available() -> bool:
    try:
        client = MongoClient(
            settings.MONGO_URI,
            serverSelectionTimeoutMS=3000,
        )
        client.admin.command("ping")
        client.close()
        return True
    except ServerSelectionTimeoutError:
        return False


requires_mongo = pytest.mark.skipif(
    not _mongo_available(),
    reason="MongoDB not reachable",
)


@requires_mongo
class TestMongoIntegration:
    def test_database_connection(self):
        from app.core.database import database

        assert database.name == settings.DATABASE_NAME


@requires_mongo
class TestAuthIntegration:
    def test_register_and_login_flow(self, app):
        from fastapi.testclient import TestClient

        app.dependency_overrides.clear()

        import uuid

        unique = uuid.uuid4().hex[:8]
        email = f"pytest_{unique}@test.com"
        username = f"pytest_{unique}"

        with TestClient(app) as client:
            register = client.post(
                "/auth/register",
                json={
                    "username": username,
                    "email": email,
                    "password": "TestPass123!",
                },
            )

            assert register.status_code == 201

            login = client.post(
                "/auth/login",
                json={
                    "email": email,
                    "password": "TestPass123!",
                },
            )

            assert login.status_code == 200
            assert "access_token" in login.json()
