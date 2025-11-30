from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
import pytest

client = TestClient(app)

@patch('src.api.chatbot.retrieve_relevant_content')
@patch('src.api.chatbot.generate_rag_response')
def test_chat_with_bot_success(mock_generate_rag_response, mock_retrieve_relevant_content):
    mock_retrieve_relevant_content.return_value = ["mocked relevant content"]
    mock_generate_rag_response.return_value = "Mocked chat response"

    response = client.post("/api/v1/chat", json={"message": "Hello bot"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Mocked chat response", "source_references": []}
    mock_retrieve_relevant_content.assert_called_once_with("Hello bot")
    mock_generate_rag_response.assert_called_once_with("Hello bot", ["mocked relevant content"])

@patch('src.api.chatbot.retrieve_relevant_content')
@patch('src.api.chatbot.generate_rag_response')
def test_chat_with_bot_error(mock_generate_rag_response, mock_retrieve_relevant_content):
    mock_retrieve_relevant_content.side_effect = Exception("Service error")
    
    response = client.post("/api/v1/chat", json={"message": "Hello bot"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Service error"}

def test_chat_with_bot_invalid_request():
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422 # Pydantic validation error

@patch('src.api.chatbot.generate_rag_response')
def test_ask_selected_success(mock_generate_rag_response):
    mock_generate_rag_response.return_value = "Mocked selected text response"

    response = client.post("/api/v1/ask-selected", json={"selected_text": "Selected text"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Mocked selected text response", "source_references": []}
    mock_generate_rag_response.assert_called_once_with("Selected text", ["Selected text"])

@patch('src.api.chatbot.generate_rag_response')
def test_ask_selected_error(mock_generate_rag_response):
    mock_generate_rag_response.side_effect = Exception("Service error")
    
    response = client.post("/api/v1/ask-selected", json={"selected_text": "Selected text"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Service error"}

def test_ask_selected_invalid_request():
    response = client.post("/api/v1/ask-selected", json={})
    assert response.status_code == 422 # Pydantic validation error
