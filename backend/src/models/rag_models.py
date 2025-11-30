from pydantic import BaseModel
from typing import List, Optional

class ChatMessageRequest(BaseModel):
    message: str

class AskSelectedRequest(BaseModel):
    selected_text: str
    context_id: Optional[str] = None

class ChatbotResponse(BaseModel):
    answer: str
    source_references: Optional[List[str]] = None
