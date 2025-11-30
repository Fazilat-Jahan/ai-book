import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

def get_qdrant_client():
    """
    Initializes and returns a Qdrant client.
    """
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in the environment.")

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
    )
    return client

# Example usage (optional, for testing)
if __name__ == "__main__":
    try:
        qdrant_client = get_qdrant_client()
        print("Successfully connected to Qdrant.")
        # You can add more tests here, like listing collections
        # collections = qdrant_client.get_collections()
        # print(f"Available collections: {collections}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
