from fastapi import FastAPI
from src.api import chatbot
import uvicorn

app = FastAPI(
    title="AI-Book RAG Chatbot API",
    description="API for the Retrieval-Augmented Generation (RAG) chatbot.",
    version="1.0.0"
)

app.include_router(chatbot.router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI-Book RAG Chatbot API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)