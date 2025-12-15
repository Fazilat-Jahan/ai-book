from typing import List
import os
from openai import OpenAI

def get_openai_client():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY must be set in the environment.")
    return OpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

def get_embedding_model_name():
    return 'embedding-001'

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    if not texts:
        return [] # Return empty list if no texts are provided for embedding

    client = get_openai_client()
    response = client.embeddings.create(
        model=get_embedding_model_name(),
        input=texts
    )
    return [item.embedding for item in response.data]

# Example usage (optional, for testing)
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    try:
        test_texts = ["Hello, world!", "Another text"]
        embeddings = generate_embeddings(test_texts)
        print(f"Successfully generated embeddings for {len(test_texts)} texts.")
        for i, embedding in enumerate(embeddings):
            print(f"Embedding {i+1} dimension: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")