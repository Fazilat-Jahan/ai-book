from typing import List, Dict, Any

def build_context_from_chunks(
    retrieved_chunks: List[Dict[str, Any]],
    query: str = None,
    selected_text: str = None,
    max_context_length: int = 4000 # Approximate token limit for context
) -> str:
    """
    Constructs a context string from a list of retrieved chunks, prioritizing relevance.
    Each chunk's text content is combined, along with its source metadata.

    Args:
        retrieved_chunks: A list of dictionaries, where each dictionary represents a retrieved chunk.
                          Expected keys: 'text_content', 'file_path', 'page_number', 'chunk_index'.
        query: The original query string (optional, for potential future prioritization logic).
        selected_text: The text highlighted by the user (optional, for potential future prioritization logic).
        max_context_length: The maximum approximate length of the context string (in characters/words).
                            This is a simple approximation; true token counting would be more accurate.

    Returns:
        A single string representing the constructed context for the LLM.
    """
    if not retrieved_chunks:
        return ""

    context_parts = []
    current_context_length = 0

    # Sort chunks by relevance or proximity if needed (for now, just use the order from retrieval)
    # Future enhancement: Implement more sophisticated prioritization based on query/selected_text

    for i, chunk in enumerate(retrieved_chunks):
        chunk_text = chunk.get('text_content', '')
        file_path = chunk.get('file_path', 'N/A')
        page_number = chunk.get('page_number', 'N/A')
        chunk_index = chunk.get('chunk_index', 'N/A')

        source_info = f"[Source: {file_path} (Page {page_number}, Chunk {chunk_index}) ]"
        
        # Combine source info and chunk text
        formatted_chunk = f"{source_info}\n{chunk_text}\n"

        # Check if adding this chunk exceeds the max context length
        # Using len() as a rough approximation for token count
        if current_context_length + len(formatted_chunk) > max_context_length:
            print(f"Truncating context: Max length {max_context_length} reached. Skipping remaining chunks.")
            break
        
        context_parts.append(formatted_chunk)
        current_context_length += len(formatted_chunk)

    return "\n".join(context_parts).strip()

if __name__ == "__main__":
    # Example usage
    sample_chunks = [
        {
            "text_content": "This is the first chunk of text from document A, discussing AI concepts. It's quite informative.",
            "file_path": "docs/tutorial.md",
            "page_number": 1,
            "chunk_index": 0
        },
        {
            "text_content": "Document A continues with more details about machine learning algorithms. This is page 1, chunk 1.",
            "file_path": "docs/tutorial.md",
            "page_number": 1,
            "chunk_index": 1
        },
        {
            "text_content": "This chunk is from document B, on page 3, outlining hardware requirements for deep learning.",
            "file_path": "docs/hardware.pdf",
            "page_number": 3,
            "chunk_index": 0
        },
        {
            "text_content": "Further requirements from document B, page 3, related to GPU memory and processing power.",
            "file_path": "docs/hardware.pdf",
            "page_number": 3,
            "chunk_index": 1
        }
    ]

    test_query = "What are the hardware requirements?"
    
    # Test with full context
    context = build_context_from_chunks(sample_chunks, query=test_query, max_context_length=1000)
    print("\n--- Full Context ---")
    print(context)
    print(f"Context length: {len(context)}")

    # Test with truncated context
    context_truncated = build_context_from_chunks(sample_chunks, query=test_query, max_context_length=200)
    print("\n--- Truncated Context (max 200 chars) ---")
    print(context_truncated)
    print(f"Context length: {len(context_truncated)}")

    # Test with empty chunks
    context_empty = build_context_from_chunks([])
    print(f"\n--- Empty Context ---")
    print(f"Context: '{context_empty}'")
