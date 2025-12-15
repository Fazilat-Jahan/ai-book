import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

QDRANT_COLLECTION_NAME = "ai_book"
QDRANT_VECTOR_SIZE = 768  # Gemini embedding-001 size

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

def recreate_qdrant_collection():
    """
    Recreates the Qdrant collection, ensuring it's empty and has the correct configuration.
    """
    client = get_qdrant_client()
    
    # Delete collection if it already exists
    try:
        client.delete_collection(collection_name=QDRANT_COLLECTION_NAME)
        print(f"Collection '{QDRANT_COLLECTION_NAME}' deleted.")
    except Exception as e:
        print(f"Collection '{QDRANT_COLLECTION_NAME}' did not exist or could not be deleted: {e}")

    # Create collection
    client.create_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=VectorParams(size=QDRANT_VECTOR_SIZE, distance=Distance.COSINE),
    )
    print(f"Collection '{QDRANT_COLLECTION_NAME}' created with vector size {QDRANT_VECTOR_SIZE}.")

def upsert_points_to_qdrant(points: list[PointStruct]):
    """
    Upserts a list of PointStructs into the Qdrant collection.
    """
    if not points:
        print("No points to upsert. Skipping Qdrant upsert operation.")
        return None 

    client = get_qdrant_client()
    operation_info = client.upsert(
        collection_name=QDRANT_COLLECTION_NAME,
        wait=True,
        points=points,
    )
    print(f"Upserted {len(points)} points. Status: {operation_info.status}")
    return operation_info

def search_qdrant(query_vector: list[float], limit: int = 5):
    """
    Searches the Qdrant collection with a given query vector.
    """
    client = get_qdrant_client()
    search_result = client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
        with_payload=True
    )
    return search_result