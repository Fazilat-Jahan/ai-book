import os
from typing import Iterator
from openai import OpenAI

def get_gemini_client():
    """
    Initializes and returns an OpenAI client configured for Gemini.
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY must be set in the environment.")
    return OpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

def get_llm_model_name():
    # As per ADR 0002, using a capable Gemini model for chat.
    # Assumes 'gemini-pro' or similar is the chat model.
    return "gemini-2.5-flash" # Or "gemini-1.5-pro", "gemini-1.5-flash" depending on availability and requirements

def generate_llm_response(prompt: str, stream: bool = False) -> str | Iterator[str]:
    """
    Generates a response from the LLM based on the provided prompt.

    Args:
        prompt: The full prompt string for the LLM.
        stream: If True, yields response chunks as they are generated.

    Returns:
        The complete response string or an iterator of response chunks.
    """
    client = get_gemini_client()
    model_name = get_llm_model_name()

    messages = [{"role": "user", "content": prompt}]

    try:
        if stream:
            response_stream = client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=True,
            )
            def generate_chunks():
                for chunk in response_stream:
                    if chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content
            return generate_chunks()
        else:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=False,
            )
            return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating LLM response: {e}")
        raise # Re-raise to be handled by calling function

if __name__ == "__main__":
    from dotenv import load_dotenv
    # Load environment variables from .env file
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    if os.path.exists(dotenv_path):
        print(f"Loading environment variables from {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)
    else:
        print("Warning: .env file not found. Please ensure your environment variables are set.")

    # Test non-streaming
    print("\n--- Testing non-streaming response ---")
    try:
        test_prompt = "Hello, what is the capital of France?"
        response = generate_llm_response(test_prompt, stream=False)
        print(f"LLM Response: {response}")
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Test streaming
    print("\n--- Testing streaming response ---")
    try:
        test_prompt_stream = "Explain the concept of large language models in a few sentences."
        stream_chunks = generate_llm_response(test_prompt_stream, stream=True)
        print("Streaming LLM Response: ", end="")
        full_response_streamed = ""
        for chunk in stream_chunks:
            print(chunk, end="")
            full_response_streamed += chunk
        print("\n(Stream complete)")
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
