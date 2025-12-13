import os
import sys
import glob
from typing import List
from qdrant_client.models import PointStruct
from uuid import uuid4
from dotenv import load_dotenv

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

load_dotenv(dotenv_path=os.path.join(project_root, 'backend', '.env'))

sys.path.insert(0, project_root)

from backend.app.document_parser import parse_document
from backend.app.chunking_service import chunk_text
from backend.app.embedding_service import generate_embeddings
from backend.app.qdrant_client import upsert_points_to_qdrant, recreate_qdrant_collection

DOCS_DIR = os.path.join(project_root, 'docs', 'docs')

def get_document_paths() -> List[str]:
    """Returns a list of paths to all .md and .mdx files in the docs directory."""
    paths = []
    for ext in ('**/*.md', '**/*.mdx'):
        paths.extend(glob.glob(os.path.join(DOCS_DIR, ext), recursive=True))
    return paths

def main():
    """
    Main function to run the indexing workflow.
    """
    print("Starting indexing workflow...")
    
    # Recreate collection
    recreate_qdrant_collection()

    doc_paths = get_document_paths()
    print(f"Found {len(doc_paths)} documents to index.")

    all_points = []
    for path in doc_paths:
        print(f"Processing {path}...")
        try:
            content = parse_document(path)
            chunks = chunk_text(content)
            
            if not chunks:
                print(f"No chunks generated for {path}.")
                continue

            embeddings = generate_embeddings(chunks)

            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                points.append(PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "file_path": path,
                        "chunk_index": i,
                        "text_content": chunk
                    }
                ))
            all_points.extend(points)
            print(f"Generated {len(points)} points for {path}.")

        except Exception as e:
            print(f"Error processing {path}: {e}")

    if all_points:
        print(f"Upserting {len(all_points)} points to Qdrant...")
        upsert_points_to_qdrant(all_points)
        print("Indexing workflow completed.")
    else:
        print("No points were generated to upsert.")

if __name__ == "__main__":
    main()
