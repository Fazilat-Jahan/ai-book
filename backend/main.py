import os
import time
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, Iterator
from starlette.middleware.cors import CORSMiddleware
import json

from app.chat_service import get_rag_answer
from app.logger import logger # My custom logger

# Load environment variables at the top
load_dotenv()

app = FastAPI(
    title="AI-Book RAG Chatbot API",
    description="API for the Retrieval-Augmented Generation (RAG) chatbot.",
    version="1.0.0"
)

# Configure CORS - use my version, removing the existing one
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# My global Exception Handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = request.state.request_id if hasattr(request.state, 'request_id') else "N/A"
    
    logger.error(
        f"HTTP Exception: {exc.status_code} - {exc.detail}",
        extra={
            "request_id": request_id,
            "status_code": exc.status_code,
            "detail": exc.detail,
            "path": request.url.path,
            "method": request.method,
            "service": "fastapi"
        }
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status": "error", "request_id": request_id},
    )

# My global Exception Handler for generic Exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    request_id = request.state.request_id if hasattr(request.state, 'request_id') else "N/A"
    
    logger.error(
        f"Unhandled Exception: {exc}",
        exc_info=True, # Log traceback
        extra={
            "request_id": request_id,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": str(exc),
            "path": request.url.path,
            "method": request.method,
            "service": "fastapi"
        }
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred.", "status": "error", "request_id": request_id},
    )

# Pydantic model for the /ask endpoint
class AskRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Hello RAG Chatbot!"}

@app.post("/ask")
async def ask(request: Request, ask_request: AskRequest):
    """
    Endpoint to ask a question to the RAG chatbot.
    Supports streaming responses.
    """
    start_time = time.time()
    request_id = os.urandom(8).hex() # Generate a unique request ID
    request.state.request_id = request_id # Store request_id in request.state for access in exception handlers

    logger.info(
        "Received /ask request",
        extra={
            "request_id": request_id,
            "question": ask_request.question,
            "selected_text": ask_request.selected_text,
            "client_host": request.client.host if request.client else "N/A",
            "endpoint": "/ask",
            "method": "POST",
            "service": "fastapi"
        }
    )

    question = ask_request.question
    selected_text = ask_request.selected_text

    async def generate_response_stream():
        full_response_content = ""
        try:
            response_generator = get_rag_answer(question, selected_text, stream=True)
            for chunk in response_generator:
                full_response_content += chunk
                yield json.dumps({"content": chunk, "status": "streaming"}) + "\n"
            
            # Log successful completion of streaming
            end_time = time.time()
            process_time = round((end_time - start_time) * 1000) # in ms
            logger.info(
                "Completed /ask request successfully",
                extra={
                    "request_id": request_id,
                    "question": question,
                    "selected_text": selected_text,
                    "response_length": len(full_response_content),
                    "process_time_ms": process_time,
                    "status_code": 200,
                    "service": "fastapi"
                }
            )
            yield json.dumps({"content": "", "status": "complete"}) + "\n"
        except Exception as e:
            error_message = f"An error occurred while generating response: {e}"
            end_time = time.time()
            process_time = round((end_time - start_time) * 1000) # in ms
            
            logger.error(
                "Error processing /ask request during streaming",
                exc_info=True,
                extra={
                    "request_id": request_id,
                    "question": question,
                    "selected_text": selected_text,
                    "error": str(e),
                    "process_time_ms": process_time,
                    "status_code": 500, # This status code won't be set for the HTTP response if streaming has started
                    "service": "fastapi"
                }
            )
            yield json.dumps({"content": error_message, "status": "error"}) + "\n"

    return StreamingResponse(generate_response_stream(), media_type="application/json")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
