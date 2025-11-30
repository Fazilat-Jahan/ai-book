from fastapi import APIRouter, HTTPException
from ..models.rag_models import ChatMessageRequest, AskSelectedRequest, ChatbotResponse
from ..services.rag_service import retrieve_relevant_content, generate_rag_response

router = APIRouter()

@router.post("/chat", response_model=ChatbotResponse)
async def chat_with_bot(request: ChatMessageRequest):
    try:
        print(f"Received message: {request.message}")
        relevant_content = retrieve_relevant_content(request.message)
        print(f"Relevant content: {relevant_content}")
        answer = generate_rag_response(request.message, relevant_content)
        print(f"Generated answer: {answer}")
        return ChatbotResponse(answer=answer, source_references=[]) # Placeholder for sources
    except Exception as e:
        print(f"Error in chat_with_bot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask-selected", response_model=ChatbotResponse)
async def ask_selected(request: AskSelectedRequest):
    try:
        # For ask-selected, we can use the selected text as both the query and the context
        answer = generate_rag_response(request.selected_text, [request.selected_text])
        return ChatbotResponse(answer=answer, source_references=[]) # Placeholder for sources
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
