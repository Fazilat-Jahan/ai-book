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

def generate_embeddings(text: str):
    client = get_openai_client()
    response = client.embeddings.create(
        model=get_embedding_model_name(),
        input=text
    )
    return response.data[0].embedding

# Example usage (optional, for testing)
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    try:
        test_text = "Hello, world!"
        embedding = generate_embeddings(test_text)
        print(f"Successfully generated embedding for '{test_text}'.")
        print(f"Embedding dimension: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")