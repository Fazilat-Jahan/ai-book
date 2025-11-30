import pytest
from pydantic import ValidationError
from src.models.rag_models import ChatMessageRequest, AskSelectedRequest, ChatbotResponse

def test_chat_message_request_valid():
    req = ChatMessageRequest(message="Hello")
    assert req.message == "Hello"

def test_chat_message_request_invalid():
    with pytest.raises(ValidationError):
        ChatMessageRequest()

def test_ask_selected_request_valid():
    req = AskSelectedRequest(selected_text="This is selected")
    assert req.selected_text == "This is selected"
    assert req.context_id is None

def test_ask_selected_request_with_context():
    req = AskSelectedRequest(selected_text="This is selected", context_id="doc1")
    assert req.selected_text == "This is selected"
    assert req.context_id == "doc1"

def test_ask_selected_request_invalid():
    with pytest.raises(ValidationError):
        AskSelectedRequest()

def test_chatbot_response_valid():
    resp = ChatbotResponse(answer="This is an answer")
    assert resp.answer == "This is an answer"
    assert resp.source_references is None

def test_chatbot_response_with_sources():
    resp = ChatbotResponse(answer="This is an answer", source_references=["doc1", "doc2"])
    assert resp.answer == "This is an answer"
    assert resp.source_references == ["doc1", "doc2"]

def test_chatbot_response_invalid():
    with pytest.raises(ValidationError):
        ChatbotResponse()
