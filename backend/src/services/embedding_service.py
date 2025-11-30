import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_embedding_model():
    """
    Initializes and returns the Gemini embedding model.
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY must be set in the environment.")

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('models/embedding-001')
    return model

def generate_embeddings(text: str):
    """
    Generates embeddings for the given text using the Gemini embedding model.
    """
    model = get_embedding_model()
    result = genai.embed_content(model=model, content=text)
    return result['embedding']

# Example usage (optional, for testing)
if __name__ == "__main__":
    try:
        test_text = "Hello, world!"
        embedding = generate_embeddings(test_text)
        print(f"Successfully generated embedding for '{test_text}'.")
        print(f"Embedding dimension: {len(embedding)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
