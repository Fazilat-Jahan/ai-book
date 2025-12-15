from typing import Optional, Dict, Any, Iterator
from app.retrieval_service import retrieve_relevant_chunks
from app.context_builder import build_context_from_chunks
from app.rag_prompt import build_rag_prompt
from app.llm_client import generate_llm_response

def get_rag_answer(query: str, selected_text: Optional[str] = None, stream: bool = False) -> str | Iterator[str]:
    """
    Orchestrates the RAG process to get an answer from the LLM.

    Args:
        query: The user's query.
        selected_text: Optional. Text highlighted by the user.
        stream: If True, yields response chunks as they are generated.

    Returns:
        The complete answer string or an iterator of response chunks.
    """
    retrieved_chunks = []
    context = ""

    # If selected_text is provided, prioritize it for context, do not retrieve other chunks
    if selected_text:
        # The rag_prompt will handle using selected_text directly, so we don't need
        # to retrieve general chunks in this specific case.
        pass
    else:
        # Retrieve relevant chunks if no selected text
        retrieved_chunks = retrieve_relevant_chunks(query)
        context = build_context_from_chunks(retrieved_chunks, query=query)

    # Build the RAG prompt
    prompt = build_rag_prompt(query, context, selected_text=selected_text)

    # Generate LLM response
    try:
        response = generate_llm_response(prompt, stream=stream)
        return response
    except Exception as e:
        print(f"Error generating LLM response in chat_service: {e}")
        # Fallback for LLM errors
        if stream:
            return iter(["Sorry, I'm having trouble generating a response right now. Please try again later."])
        else:
            return "Sorry, I'm having trouble generating a response right now. Please try again later."

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    # Load environment variables from .env file
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    if os.path.exists(dotenv_path):
        print(f"Loading environment variables from {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)
    else:
        print("Warning: .env file not found. Please ensure your environment variables are set.")
    
    # Example 1: General question (non-streaming)
    print("\n--- Testing General Question (Non-Streaming) ---")
    general_query = "What are the main principles of AI ethics?"
    answer_general = get_rag_answer(general_query, stream=False)
    print(f"Query: {general_query}")
    print(f"Answer: {answer_general}")

    # Example 2: General question (streaming)
    print("\n--- Testing General Question (Streaming) ---")
    general_query_stream = "Explain how large language models work."
    print(f"Query: {general_query_stream}")
    print("Answer (streaming): ", end="")
    streamed_answer_parts = get_rag_answer(general_query_stream, stream=True)
    full_streamed_answer = ""
    for part in streamed_answer_parts:
        print(part, end="")
        full_streamed_answer += part
    print("\n(Stream complete)")

    # Example 3: Question with selected text (non-streaming)
    print("\n--- Testing Question with Selected Text (Non-Streaming) ---")
    selected_text_example = "Artificial intelligence (AI) is a rapidly evolving field that aims to create machines capable of intelligent behavior. This includes learning, reasoning, problem-solving, perception, and language understanding."
    selected_query = "What capabilities does AI aim for based on the selected text?"
    answer_selected = get_rag_answer(selected_query, selected_text=selected_text_example, stream=False)
    print(f"Query: {selected_query}")
    print(f"Selected Text: {selected_text_example[:100]}...")
    print(f"Answer: {answer_selected}")

    # Example 4: Question with no relevant chunks or context (non-streaming)
    print("\n--- Testing Question with No Relevant Chunks (Non-Streaming) ---")
    no_context_query = "What is the meaning of life?"
    # To simulate no context, we would need to mock retrieve_relevant_chunks to return empty
    # For now, if the LLM gets an empty context, it should trigger the fallback in rag_prompt.py
    answer_no_context = get_rag_answer(no_context_query, stream=False)
    print(f"Query: {no_context_query}")
    print(f"Answer: {answer_no_context}")
