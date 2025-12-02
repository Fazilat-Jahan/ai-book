import os
import re
import uuid
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict

from backend.models import ChatMessageRequest, AskSelectedRequest, ChatbotResponse, IndexDocsRequest, HealthResponse, SourceReference
from backend.embeddings import generate_embeddings, get_openai_client
from backend.qdrant_client import get_qdrant_client, recreate_qdrant_collection, upsert_points_to_qdrant, search_qdrant
from qdrant_client.models import PointStruct

router = APIRouter()

QDRANT_COLLECTION_NAME = "ai_book"

def get_markdown_files(docs_path):
    """
    Finds all Markdown files in the specified directory, excluding tutorials.
    """
    markdown_files = []
    for root, _, files in os.walk(docs_path):
        if 'tutorial-basics' in root or 'tutorial-extras' in root:
            continue
        for file in files:
            if file.endswith('.md') or file.endswith('.mdx'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def chunk_content(content):
    """
    Splits the content into chunks based on paragraphs.
    """
    paragraphs = re.split(r'\n\s*\n', content)
    chunks = []
    for paragraph in paragraphs:
        if paragraph.strip():
            chunks.append(paragraph.strip())
    return chunks

def extract_title(content):
    """
    Extracts the title from the markdown content (first H1 tag).
    """
    match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Untitled"

def construct_url(file_path):
    """
    Constructs a URL from the file path.
    """
    # Remove 'docs/docs/' prefix and '.md' or '.mdx' suffix
    url_path = file_path.replace('docs/docs/', '').replace('.mdx', '').replace('.md', '')
    # Handle 'index' files
    if url_path.endswith('index'):
        url_path = url_path[:-5]
    return f"/docs/{url_path}"

async def _index_documents_task(docs_path: str):
    """
    Background task to ingest and process the content into Qdrant.
    """
    print(f"Starting document indexing from {docs_path}...")
    try:
        recreate_qdrant_collection()
        markdown_files = get_markdown_files(docs_path)
        
        all_chunks = []
        for file_path in markdown_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                title = extract_title(content)
                url = construct_url(file_path)
                chunks = chunk_content(content)
                all_chunks.extend([(chunk, title, url) for chunk in chunks])

        print(f"Found {len(markdown_files)} markdown files.")
        print(f"Created {len(all_chunks)} chunks of content.")
        print("Generating embeddings and indexing content in Qdrant...")

        points = []
        for i, (chunk, title, url) in enumerate(all_chunks):
            # Handle potential ResourceExhausted errors
            try:
                embedding = generate_embeddings(chunk)
            except Exception as e:
                print(f"Error generating embedding for chunk {i+1}: {e}. Skipping this chunk.")
                continue
            
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={"text": chunk, "title": title, "url": url}
            )
            points.append(point)
            if (i + 1) % 10 == 0:
                print(f"  - Generated embeddings for {i+1}/{len(all_chunks)} chunks.")

        if points:
            upsert_points_to_qdrant(points)
            print("Content ingestion and indexing complete.")
        else:
            print("No points to upsert.")

    except Exception as e:
        print(f"Error during document indexing: {e}")

@router.post("/index-docs", status_code=202)
async def index_docs(request: IndexDocsRequest, background_tasks: BackgroundTasks):
    """
    Triggers a background task to index documentation files into Qdrant.
    """
    background_tasks.add_task(_index_documents_task, request.docs_path)
    return {"message": "Document indexing started in the background."}

@router.post("/ask", response_model=ChatbotResponse)
async def ask(request: ChatMessageRequest):
    """
    Receives a user query, retrieves relevant content, and generates a response.
    """
    try:
        query_embedding = generate_embeddings(request.message)
        search_results = search_qdrant(query_embedding, limit=5)

        relevant_content_for_llm: List[Dict] = []
        source_references: List[SourceReference] = []

        for hit in search_results:
            relevant_content_for_llm.append({
                "text": hit.payload["text"],
                "title": hit.payload["title"],
                "url": hit.payload["url"]
            })
            source_references.append(SourceReference(
                title=hit.payload["title"],
                url=hit.payload["url"],
                text=hit.payload["text"] # Storing full text for completeness, though UI might just show title/url
            ))
        
        context_str = "\n\n".join([item['text'] for item in relevant_content_for_llm])

        openai_client = get_openai_client()
        response = openai_client.chat.completions.create(
            model="gemini-1.5-pro-latest", # Use the correct Gemini model name for the OpenAI-compatible proxy
            messages=[
                {"role": "system", "content": "You are a helpful assistant for the 'Physical AI & Humanoid Robotics Program' textbook. Answer the user's question truthfully and only based on the following context from the textbook. If the context does not contain the answer, say "This answer is not in the textbook content.". Do not use any outside knowledge."},
                {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion:\n{request.message}"}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response.choices[0].message.content

        if not context_str and "This answer is not in the textbook content." not in answer:
            answer = "This answer is not in the textbook content."


        return ChatbotResponse(answer=answer, source_references=source_references)
    except Exception as e:
        print(f"Error in /ask endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask-selected", response_model=ChatbotResponse)
async def ask_selected(request: AskSelectedRequest):
    """
    Receives selected text, and generates a response based on it.
    This bypasses Qdrant search and uses the selected text directly as context.
    """
    try:
        # Use selected text as the direct context for the LLM
        context_item = {
            "text": request.selected_text,
            "title": "Selected Content",
            "url": "#selected-content" # A dummy URL for selected text
        }
        
        openai_client = get_openai_client()
        response = openai_client.chat.completions.create(
            model="gemini-1.5-pro-latest", # Use the correct Gemini model name for the OpenAI-compatible proxy
            messages=[
                {"role": "system", "content": "You are a helpful assistant for the 'Physical AI & Humanoid Robotics Program' textbook. Answer the user's question truthfully and only based on the following selected text from the textbook. If the selected text does not contain the answer, say "This answer is not in the selected content.". Do not use any outside knowledge."},
                {"role": "user", "content": f"Selected Content:\n{context_item['text']}\n\nQuestion:\n{request.selected_text}"}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response.choices[0].message.content

        # If LLM doesn't find the answer in the selected content, ensure fallback message
        if "This answer is not in the selected content." not in answer and not context_item['text']:
             answer = "This answer is not in the selected content."
        elif not context_item['text'] and answer.strip() == "":
            answer = "No content was selected."

        source_references = [SourceReference(
            title=context_item['title'],
            url=context_item['url'],
            text=context_item['text']
        )]
        
        return ChatbotResponse(answer=answer, source_references=source_references)
    except Exception as e:
        print(f"Error in /ask-selected endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Provides health status of the RAG system components.
    """
    qdrant_status = "ok"
    gemini_status = "ok"

    try:
        client = get_qdrant_client()
        client.get_collections() # Simple call to check connection
    except Exception as e:
        qdrant_status = f"error: {e}"

    try:
        openai_client = get_openai_client()
        openai_client.chat.completions.create(model="gemini-1.5-pro-latest", messages=[{"role": "user", "content": "hello"}], max_tokens=10)
    except Exception as e:
        gemini_status = f"error: {e}"

    return HealthResponse(
        status="ok" if qdrant_status == "ok" and gemini_status == "ok" else "degraded",
        qdrant_status=qdrant_status,
        gemini_status=gemini_status
    )