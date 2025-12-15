# AI-Book RAG Chatbot

This project implements a Retrieval-Augmented Generation (RAG) chatbot for the AI Book, allowing users to ask questions based on the book's content. The project consists of a FastAPI backend and a React frontend integrated into a Docusaurus documentation site.

## Architecture

-   **Backend**: FastAPI (Python) for RAG orchestration, document processing (parsing, chunking, embedding), Qdrant vector database interaction, and LLM (Gemini via OpenAI client) integration.
-   **Frontend**: React component integrated into Docusaurus, providing a chat widget to interact with the backend.
-   **Vector Database**: Qdrant (Cloud) for storing and retrieving document embeddings.
-   **LLM**: Google Gemini, accessed via an OpenAI-compatible client.

## Setup and Running

Follow these steps to set up and run the AI-Book RAG Chatbot locally.

### 1. Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
QDRANT_URL="YOUR_QDRANT_CLOUD_URL"
QDRANT_API_KEY="YOUR_QDRANT_CLOUD_API_KEY"
```

-   **GEMINI_API_KEY**: Obtain this from Google AI Studio.
-   **QDRANT_URL**: Your Qdrant Cloud cluster URL.
-   **QDRANT_API_KEY**: Your Qdrant Cloud API key.

### 2. Backend Setup

Navigate to the `backend/` directory and install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend Setup (Docusaurus)

Navigate to the `docs/` directory and install Node.js dependencies:

```bash
cd docs
npm install
```

### 4. Index Documents

Before running the chatbot, you need to index the book's documents into Qdrant. This will parse the documents, chunk them, generate embeddings, and upsert them to your Qdrant collection.

From the root of the project, run:

```bash
python backend/scripts/index_documents.py
```

**Note**: This script will recreate the `ai_book` Qdrant collection, deleting any existing data in it. Ensure your `GEMINI_API_KEY`, `QDRANT_URL`, and `QDRANT_API_KEY` are correctly set in `backend/.env`.

### 5. Run the Backend

From the `backend/` directory, start the FastAPI application:

```bash
cd backend
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`.

### 6. Run the Frontend

From the `docs/` directory, start the Docusaurus development server:

```bash
cd docs
npm start
```

The Docusaurus site, including the RAG chatbot widget, will be available at `http://localhost:3000` (or another port if 3000 is in use).

## Usage

-   Open the Docusaurus site in your browser.
-   Click the "Chat" button (or similar) to open the chatbot widget.
-   Ask questions related to the AI Book content.

## Known Issues / Enhancements

-   Source references are not yet displayed in the frontend chat widget (backend currently doesn't provide them in the stream).
-   The current chunking strategy is word-based; a token-based strategy could offer more precision.
-   Advanced LLM context window management and prompt engineering could further enhance response quality.

---
