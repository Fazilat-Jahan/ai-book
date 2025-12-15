import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict, Any
import uuid

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.document_parser import parse_document
from app.chunking_service import chunk_text
from app.embedding_service import generate_embeddings
from app.qdrant_client import recreate_qdrant_collection, upsert_points_to_qdrant, QDRANT_COLLECTION_NAME
from qdrant_client.models import PointStruct

def get_document_paths(base_dir: str) -> List[Path]:
    """
    Recursively finds all supported document files (.md, .mdx, .pdf) in the given base directory.
    """
    supported_extensions = {'.md', '.mdx', '.pdf'}
    document_paths = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in supported_extensions:
                document_paths.append(file_path)
    return document_paths

def index_documents():
    """
    Orchestrates the end-to-end document indexing workflow.
    """
    print("Starting document indexing workflow...")

    # 1. Load environment variables
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    if os.path.exists(dotenv_path):
        print(f"Loading environment variables from {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)
    else:
        print("Warning: .env file not found. Ensure GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY are set.")

    # 2. Recreate the Qdrant collection
    print(f"Recreating Qdrant collection: {QDRANT_COLLECTION_NAME}")
    try:
        recreate_qdrant_collection()
        print(f"Qdrant collection '{QDRANT_COLLECTION_NAME}' re-created successfully.")
    except Exception as e:
        print(f"Error recreating Qdrant collection: {e}")
        sys.exit(1)

    # Define base directories for documents
    docs_base_path = Path(os.path.abspath(__file__)).parents[2] / "docs" / "docs"
    blog_base_path = Path(os.path.abspath(__file__)).parents[2] / "docs" / "blog"

    all_document_paths = []
    if docs_base_path.exists():
        all_document_paths.extend(get_document_paths(str(docs_base_path)))
    if blog_base_path.exists():
        all_document_paths.extend(get_document_paths(str(blog_base_path)))

    if not all_document_paths:
        print("No supported documents found in 'docs/docs/' or 'docs/blog/'. Exiting.")
        sys.exit(0)

    print(f"Found {len(all_document_paths)} documents to index.")

    points_to_upsert: List[PointStruct] = []
    texts_to_embed: List[str] = []
    metadata_for_points: List[Dict[str, Any]] = []

    for doc_path in all_document_paths:
        print(f"Processing document: {doc_path.relative_to(Path(os.getcwd()))}")
        try:
            # Parse document, getting content page by page for PDFs or whole for MD
            parsed_pages_or_chunks = parse_document(str(doc_path))

            for page_index, (text_content, page_num) in enumerate(parsed_pages_or_chunks):
                if not text_content.strip():
                    continue # Skip empty pages/chunks

                # Chunk the text content
                chunks = chunk_text(text_content)
                print(f"  Split into {len(chunks)} chunks for page/segment {page_num}.")

                for chunk_index, chunk in enumerate(chunks):
                    texts_to_embed.append(chunk)
                    # Prepare metadata for this chunk
                    metadata_for_points.append({
                        "file_path": str(doc_path.relative_to(Path(os.getcwd()))), # Relative path
                        "page_number": page_num,
                        "chunk_index": chunk_index,
                        "text_content": chunk, # Store original chunk text in payload
                    })
        except Exception as e:
            print(f"  Error processing {doc_path}: {e}")
            continue

    if not texts_to_embed:
        print("No text chunks generated for embedding. Exiting.")
        sys.exit(0)

    print(f"Total {len(texts_to_embed)} text chunks prepared for embedding.")
    
    # Generate embeddings in batches
    # The generate_embeddings function handles batching internally up to API limits
    try:
        print("Generating embeddings for all chunks...")
        embeddings = generate_embeddings(texts_to_embed)
        print(f"Successfully generated {len(embeddings)} embeddings.")
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        sys.exit(1)

    # Create PointStructs and upsert to Qdrant
    if len(embeddings) != len(metadata_for_points):
        print("Mismatch between number of embeddings and metadata. Aborting upsert.")
        sys.exit(1)

    print("Preparing PointStructs for Qdrant upsert...")
    for i, embedding in enumerate(embeddings):
        if embedding is None:
            print(f"Warning: Embedding at index {i} is None. Skipping point.")
            continue
        
        points_to_upsert.append(
            PointStruct(
                id=uuid.uuid4().hex, # Generate a unique ID for each point
                vector=embedding,
                payload=metadata_for_points[i]
            )
        )
    
    if points_to_upsert:
        print(f"Upserting {len(points_to_upsert)} points to Qdrant...")
        try:
            upsert_points_to_qdrant(points_to_upsert)
            print("Document indexing completed successfully!")
        except Exception as e:
            print(f"Error upserting points to Qdrant: {e}")
            sys.exit(1)
    else:
        print("No valid points to upsert to Qdrant.")

if __name__ == "__main__":
    index_documents()