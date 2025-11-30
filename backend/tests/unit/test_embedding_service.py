import pytest
import os
from unittest.mock import patch, MagicMock
from src.services.embedding_service import get_embedding_model, generate_embeddings

# Mock the google.generativeai module
mock_genai = MagicMock()
mock_genai.embed_content.return_value = {'embedding': [0.1, 0.2, 0.3]}

@patch.dict(os.environ, {"GEMINI_API_KEY": "test_gemini_key"})
@patch('src.services.embedding_service.genai', mock_genai)
def test_get_embedding_model_success():
    model = get_embedding_model()
    assert model is not None
    mock_genai.configure.assert_called_once_with(api_key="test_gemini_key")

@patch.dict(os.environ, {}, clear=True)
def test_get_embedding_model_missing_api_key():
    with pytest.raises(ValueError, match="GEMINI_API_KEY must be set in the environment."):
        get_embedding_model()

@patch.dict(os.environ, {"GEMINI_API_KEY": "test_gemini_key"})
@patch('src.services.embedding_service.genai', mock_genai)
def test_generate_embeddings_success():
    text = "test text"
    embedding = generate_embeddings(text)
    assert embedding == [0.1, 0.2, 0.3]
    mock_genai.embed_content.assert_called_once_with(
        model=mock_genai.GenerativeModel.return_value, # Access the mocked model instance
        content=text
    )

@patch.dict(os.environ, {}, clear=True)
def test_generate_embeddings_missing_api_key():
    with pytest.raises(ValueError, match="GEMINI_API_KEY must be set in the environment."):
        generate_embeddings("some text")
