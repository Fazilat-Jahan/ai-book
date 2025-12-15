import os
import sys
from typing import List, Dict, Any

# Add the backend directory to the Python path if necessary
# This might be needed if this service is called directly or from a script outside the app dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.embedding_service import generate_embeddings
from app.qdrant_client import search_qdrant

def retrieve_relevant_chunks(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieves relevant document chunks from Qdrant based on a query.

    Args:
        query: The user's query string.
        top_k: The number of top relevant chunks to retrieve.

    Returns:
        A list of dictionaries, where each dictionary represents a retrieved chunk
        with its text content and metadata.
    """
    if not query:
        return []

    try:
        # Generate embedding for the query
        query_embedding = generate_embeddings([query])[0]

        # Search Qdrant for similar vectors
        search_results = search_qdrant(query_embedding, limit=top_k)

        relevant_chunks = []
        for result in search_results:
            if result.payload:
                # The payload should contain file_path, page_number, chunk_index, text_content
                relevant_chunks.append(result.payload)
        
        return relevant_chunks

    except Exception as e:
        print(f"Error during retrieval: {e}")
        # Depending on desired error handling, you might want to re-raise,
        # return an empty list, or a specific error object.
        return []

if __name__ == "__main__":
    from dotenv import load_dotenv
    # Load environment variables from .env file
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    if os.path.exists(dotenv_path):
        print(f"Loading environment variables from {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)
    else:
        print("Warning: .env file not found. Please ensure your environment variables are set.")

    # Example usage
    test_query = "What is the course about?"
    chunks = retrieve_relevant_chunks(test_query)

    if chunks:
        print(f"\nRetrieved {len(chunks)} relevant chunks for query: '{test_query}'")
        for i, chunk in enumerate(chunks):
            print(f"\n--- Chunk {i+1} ---")
            print(f"File Path: {chunk.get('file_path')}")
            print(f"Page Number: {chunk.get('page_number')}")
            print(f"Chunk Index: {chunk.get('chunk_index')}")
            print(f"Content: {chunk.get('text_content', '')[:200]}...") # Print first 200 chars
    else:
        print(f"\nNo relevant chunks found for query: '{test_query}'")
