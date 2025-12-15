from typing import Optional

def build_rag_prompt(query: str, context: str, selected_text: Optional[str] = None) -> str:
    """
    Constructs a grounded RAG prompt for the LLM.

    Args:
        query: The user's query.
        context: The relevant chunks retrieved from the knowledge base, formatted into a single string.
        selected_text: Optional. Text highlighted by the user, if applicable.

    Returns:
        The complete prompt string for the LLM.
    """
    if selected_text:
        # Prompt for "ask with highlighted text"
        system_message = (
            "You are a helpful assistant. Answer the user's question ONLY based on the provided SELECTED TEXT. "
            "If the answer cannot be found in the selected text, explicitly state: "
            "'The answer to your question is not present in the selected text.'\n\n"
            "SELECTED TEXT:\n"
            f"{selected_text}\n\n"
        )
    elif context:
        # Prompt for general "ask a question" with context
        system_message = (
            "You are a helpful assistant. Answer the user's question ONLY based on the provided CONTEXT. "
            "If the answer cannot be found in the CONTEXT, explicitly state: "
            "'The answer to your question is not present in the textbook content.'\n\n"
            "CONTEXT:\n"
            f"{context}\n\n"
        )
    else:
        # Fallback if no context or selected text is provided
        system_message = (
            "You are a helpful assistant. I cannot answer your question as no relevant information "
            "was found in the textbook content. Please try asking a different question or provide more context.\n\n"
        )
    
    user_message = f"QUESTION: {query}"

    return f"{system_message}{user_message}"

# Example usage
if __name__ == "__main__":
    # General query with context
    query_general = "What are the main topics covered in the first chapter?"
    context_general = "Chapter 1 introduces artificial intelligence. Topics include machine learning and deep learning."
    prompt_general = build_rag_prompt(query_general, context_general)
    print("--- General RAG Prompt ---")
    print(prompt_general)

    # Query with selected text
    query_selected = "What does this paragraph say about AI?"
    selected_text_example = "Artificial intelligence (AI) is a rapidly evolving field that aims to create machines capable of intelligent behavior."
    prompt_selected = build_rag_prompt(query_selected, "some other context", selected_text=selected_text_example)
    print("\n--- Selected Text RAG Prompt ---")
    print(prompt_selected)

    # Query with no context
    query_no_context = "Tell me a joke."
    prompt_no_context = build_rag_prompt(query_no_context, "")
    print("\n--- No Context RAG Prompt ---")
    print(prompt_no_context)
