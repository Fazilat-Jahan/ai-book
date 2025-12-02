from pydantic import BaseModel
from typing import List, Optional

class SourceReference(BaseModel):
    title: str
    url: str
    text: str

class ChatMessageRequest(BaseModel):
    message: str

class AskSelectedRequest(BaseModel):
    selected_text: str
    context_id: Optional[str] = None # Not used currently, but kept for future expansion

class ChatbotResponse(BaseModel):
    answer: str
    source_references: Optional[List[SourceReference]] = None

class IndexDocsRequest(BaseModel):
    docs_path: str = "docs/docs" # Default path to documents

class HealthResponse(BaseModel):
    status: str = "ok"
    qdrant_status: str
    gemini_status: str