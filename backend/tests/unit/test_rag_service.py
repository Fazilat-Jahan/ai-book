import pytest
from unittest.mock import patch, MagicMock
from src.services.rag_service import retrieve_relevant_content, generate_rag_response, QDRANT_COLLECTION_NAME
from qdrant_client.http.models import PointStruct, ScoredPoint

# Mocking external services
@patch('src.services.rag_service.get_qdrant_client')
@patch('src.services.rag_service.generate_embeddings')
def test_retrieve_relevant_content(mock_generate_embeddings, mock_get_qdrant_client):
    # Setup mocks
    mock_qdrant_client = MagicMock()
    mock_get_qdrant_client.return_value = mock_qdrant_client
    mock_generate_embeddings.return_value = [0.1, 0.2, 0.3]

    # Mock search results from Qdrant
    mock_qdrant_client.search.return_value = [
        ScoredPoint(id="1", score=0.9, payload={"content": "relevant chunk 1"}, vector=None, version=0),
        ScoredPoint(id="2", score=0.8, payload={"content": "relevant chunk 2"}, vector=None, version=0),
    ]

    query = "test query"
    result = retrieve_relevant_content(query, top_k=2)

    # Assertions
    mock_generate_embeddings.assert_called_once_with(query)
    mock_qdrant_client.search.assert_called_once_with(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=[0.1, 0.2, 0.3],
        limit=2
    )
    assert result == ["relevant chunk 1", "relevant chunk 2"]

@patch('src.services.rag_service.genai')
def test_generate_rag_response(mock_genai):
    # Setup mocks
    mock_llm_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_llm_model
    mock_llm_model.generate_content.return_value.text = "This is a generated answer."

    query = "What is AI?"
    relevant_content = ["AI is artificial intelligence.", "It makes machines smart."]

    response = generate_rag_response(query, relevant_content)

    # Assertions
    expected_prompt_substrings = [
        "You are a helpful assistant for the 'Physical AI & Humanoid Robotics Program' textbook.",
        "Answer the user's question based on the following context from the textbook.",
        "Context:",
        "AI is artificial intelligence.It makes machines smart.", # .join() removes space
        "Question:",
        "What is AI?",
        "Answer:"
    ]
    actual_prompt = mock_llm_model.generate_content.call_args[0][0]

    for substring in expected_prompt_substrings:
        assert substring in actual_prompt

    mock_genai.GenerativeModel.assert_called_once_with('gemini-pro')
    mock_llm_model.generate_content.assert_called_once()
    assert response == "This is a generated answer."
