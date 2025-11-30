from .qdrant_service import get_qdrant_client
from .embedding_service import generate_embeddings
import google.generativeai as genai

QDRANT_COLLECTION_NAME = "ai-book-collection"

def retrieve_relevant_content(query: str, top_k: int = 5):
    """
    Retrieves relevant content from Qdrant based on the user's query.
    """
    qdrant_client = get_qdrant_client()
    query_embedding = generate_embeddings(query)

    search_result = qdrant_client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k
    )

    return [hit.payload['content'] for hit in search_result]

def generate_rag_response(query: str, relevant_content: list[str]):
    """
    Generates a response using the RAG model.
    """
    llm = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    You are a helpful assistant for the 'Physical AI & Humanoid Robotics Program' textbook.
    Answer the user's question based on the following context from the textbook.
    If the context doesn't contain the answer, say that you don't know.

    Context:
    {"".join(relevant_content)}

    Question:
    {query}

    Answer:
    """

    response = llm.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # This is for testing purposes.
    # You would need to have a populated Qdrant collection for this to work.
    query = "What is ROS?"
    # relevant_content = retrieve_relevant_content(query)
    # response = generate_rag_response(query, relevant_content)
    # print(response)
    print("RAG service module loaded.")
