# Quickstart Guide: AI-Book Hackathon Deliverables

This guide provides a quick overview to set up and run the AI-Book Hackathon project, including the Docusaurus textbook and the RAG chatbot.

## Prerequisites

- Node.js (v18 or higher) & npm (or yarn) for Docusaurus
- Python 3.11 for FastAPI backend
- Docker (optional, for local Qdrant or FastAPI containerization)
- GitHub account for deployment to GitHub Pages
- Qdrant Cloud account (free tier is sufficient)

## 1. Docusaurus Frontend (Textbook)

Navigate to the `docs/` directory.

```bash
cd docs
npm install
npm start
```

This will start the Docusaurus development server, and the textbook will be accessible in your browser (usually `http://localhost:3000`).

## 2. FastAPI Backend (RAG Chatbot API)

Navigate to the `backend/` directory.

### Environment Setup

Create a `.env` file in the `backend/` directory with the following variables:

```dotenv
QDRANT_URL="<your-qdrant-cloud-url>"
QDRANT_API_KEY="<your-qdrant-api-key>"
OPENAI_API_KEY="<your-openai-api-key>" # Required for embeddings and LLM
```

### Install Dependencies and Run

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

This will start the FastAPI development server, typically accessible at `http://localhost:8000`. The API documentation (Swagger UI) will be available at `http://localhost:8000/docs`.

## 3. Deployment to GitHub Pages

The Docusaurus site will be deployed to GitHub Pages. Ensure your `docusaurus.config.js` is configured correctly for your GitHub repository (e.g., `baseUrl`, `projectName`, `organizationName`).

Deployment typically involves running a build command and then a deployment script or GitHub Actions workflow. A basic deployment command for Docusaurus is:

```bash
npm run deploy
```

Refer to the `.github/workflows/` for specific GitHub Actions configurations for both Docusaurus and FastAPI deployment.

## 4. Initial Content Ingestion (for RAG)

Before the RAG chatbot can answer questions, the textbook content needs to be ingested into Qdrant Cloud. This typically involves:

1.  **Parsing**: Extracting text from Docusaurus Markdown files.
2.  **Chunking**: Breaking down the text into smaller, manageable chunks.
3.  **Embedding**: Converting text chunks into vector embeddings using an LLM (e.g., OpenAI Embeddings).
4.  **Indexing**: Uploading vectors and associated metadata to Qdrant Cloud.

This process will likely be handled by a dedicated script or a FastAPI endpoint. Details for content ingestion will be specified in the `tasks.md`.
