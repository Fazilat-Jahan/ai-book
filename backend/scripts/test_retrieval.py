import os
import sys
from dotenv import load_dotenv

from backend.embeddings import generate_embeddings
from backend.qdrant_client import search_qdrant

def test_retrieval():
    """
    Tests basic retrieval from Qdrant.
    """
    load_dotenv()

    # Check for necessary environment variables
    if not os.getenv("GEMINI_API_KEY") or not os.getenv("QDRANT_URL") or not os.getenv("QDRANT_API_KEY"):
        print("Error: GEMINI_API_KEY, QDRANT_URL, and QDRANT_API_KEY must be set in the environment.")
        return

    # 1. Define a simple query
    query = "What is a humanoid robot?"
    print(f"Testing retrieval with query: '{query}'")

    try:
        # 2. Generate an embedding for the query
        print("Generating embedding for the query...")
        query_embedding = generate_embeddings(query)
        print("Embedding generated successfully.")

        # 3. Search Qdrant for the most similar vectors
        print("Searching Qdrant for similar vectors...")
        search_results = search_qdrant(query_embedding, limit=3)
        print("Search complete.")

        # 4. Print the results
        if search_results:
            print("\n--- Search Results ---")
            for i, result in enumerate(search_results):
                print(f"Result {i+1}:")
                print(f"  Score: {result.score}")
                print(f"  Payload: {result.payload}")
        else:
            print("\n--- No results found ---")
            print("This might be because the collection is empty or the query has no matches.")

    except Exception as e:
        print(f"\nAn error occurred during the retrieval test: {e}")

if __name__ == "__main__":
    test_retrieval()
