import os
import re
import uuid
from backend.src.services.qdrant_service import get_qdrant_client
from backend.src.services.embedding_service import generate_embeddings
from qdrant_client.models import Distance, VectorParams, PointStruct

QDRANT_COLLECTION_NAME = "ai-book-collection"

def get_markdown_files(docs_path):
    """
    Finds all Markdown files in the specified directory, excluding tutorials.
    """
    markdown_files = []
    for root, _, files in os.walk(docs_path):
        if 'tutorial-basics' in root or 'tutorial-extras' in root:
            continue
        for file in files:
            if file.endswith('.md'):
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

def main():
    """
    Main function to ingest and process the content.
    """
    qdrant_client = get_qdrant_client()

    # Create collection if it doesn't exist
    try:
        qdrant_client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        print(f"Collection '{QDRANT_COLLECTION_NAME}' already exists.")
    except Exception:
        print(f"Creating collection '{QDRANT_COLLECTION_NAME}'.")
        qdrant_client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

    docs_path = 'docs/docs'
    markdown_files = get_markdown_files(docs_path)
    
    all_chunks = []
    for file_path in markdown_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            chunks = chunk_content(content)
            # Add file path as metadata
            all_chunks.extend([(chunk, file_path) for chunk in chunks])

    print(f"Found {len(markdown_files)} markdown files.")
    print(f"Created {len(all_chunks)} chunks of content.")
    print("Generating embeddings and indexing content in Qdrant...")

    points = []
    for i, (chunk, file_path) in enumerate(all_chunks):
        embedding = generate_embeddings(chunk)
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"content": chunk, "source": file_path}
        )
        points.append(point)
        print(f"  - Generated embedding for chunk {i+1}/{len(all_chunks)}")

    # Upsert all points in one go
    qdrant_client.upsert(
        collection_name=QDRANT_COLLECTION_NAME,
        points=points,
        wait=True
    )
    
    print("Content ingestion and indexing complete.")

if __name__ == "__main__":
    main()
