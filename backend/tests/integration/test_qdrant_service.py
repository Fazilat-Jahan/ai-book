import pytest
import os
from unittest.mock import patch
from src.services.qdrant_service import get_qdrant_client

@patch.dict(os.environ, {"QDRANT_URL": "http://localhost:6333", "QDRANT_API_KEY": "test_key"})
def test_get_qdrant_client_success():
    client = get_qdrant_client()
    assert client is not None

@patch.dict(os.environ, {}, clear=True)
def test_get_qdrant_client_missing_url():
    with pytest.raises(ValueError, match="QDRANT_URL and QDRANT_API_KEY must be set in the environment."):
        get_qdrant_client()

@patch.dict(os.environ, {"QDRANT_URL": "http://localhost:6333"}, clear=True)
def test_get_qdrant_client_missing_api_key():
    with pytest.raises(ValueError, match="QDRANT_URL and QDRANT_API_KEY must be set in the environment."):
        get_qdrant_client()
