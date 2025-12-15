import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.embedding_service import generate_embeddings
from app.qdrant_client import search_qdrant

def test_retrieval(query: str):
    """
    Tests the retrieval of documents from Qdrant based on a query.

    Args:
        query: The query string to test.
    """
    print(f"Testing retrieval for query: '{query}'")

    try:
        # 1. Generate embedding for the query
        print("Generating embedding for the query...")
        query_embedding = generate_embeddings([query])[0]
        print(f"Embedding generated with dimension: {len(query_embedding)}")

        # 2. Search Qdrant for similar vectors
        print("Searching Qdrant for relevant documents...")
        search_results = search_qdrant(query_embedding, limit=3)
        print(f"Found {len(search_results)} results.")

        # 3. Print the results
        if not search_results:
            print("No results found.")
            return

        for i, result in enumerate(search_results):
            print(f"\nResult {i+1}:")
            print(f"  ID: {result.id}")
            print(f"  Score: {result.score:.4f}")
            if result.payload:
                print("  Payload:")
                for key, value in result.payload.items():
                    # Truncate long text for readability
                    if isinstance(value, str) and len(value) > 150:
                        value = value[:150] + "..."
                    print(f"    {key}: {value}")
            else:
                print("  No payload found.")

    except Exception as e:
        print(f"\nAn error occurred during the retrieval test: {e}")
        print("Please check your environment variables (GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY) and ensure the Qdrant collection is populated.")

if __name__ == "__main__":
    # Load environment variables from .env file
    # Assumes the .env file is in the root of the 'backend' directory
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    if os.path.exists(dotenv_path):
        print(f"Loading environment variables from {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)
    else:
        print("Warning: .env file not found. Please ensure your environment variables are set.")

    # Example query
    test_query = "What are the hardware requirements for the course?"

    # Run the test
    test_retrieval(test_query)