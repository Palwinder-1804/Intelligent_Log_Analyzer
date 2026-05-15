import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Ensure backend root is on PYTHONPATH
BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)


@pytest.fixture
def app():
    with patch(
        "app.services.rag.bootstrap_service.bootstrap_knowledge_base",
        return_value=None,
    ):
        from app.main import app as fastapi_app

        yield fastapi_app


@pytest.fixture
def client(app):
    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_user():
    return {
        "_id": "507f1f77bcf86cd799439011",
        "username": "testuser",
        "email": "test@example.com",
        "role": "viewer",
    }


@pytest.fixture
def auth_headers(mock_user):
    from app.core.security import create_access_token

    token = create_access_token(
        data={
            "sub": str(mock_user["_id"]),
            "email": mock_user["email"],
            "role": mock_user["role"],
        }
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
def override_auth(app, mock_user):
    from app.api.dependencies.auth_dependency import get_current_user

    async def _fake_current_user():
        return mock_user

    app.dependency_overrides[get_current_user] = _fake_current_user
    yield
    app.dependency_overrides.clear()
