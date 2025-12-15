from typing import List

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Splits a text into chunks of a specified size with overlap.
    """
    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("Overlap must be less than chunk_size to avoid infinite loops or malformed chunks.")

    words = text.split()
    chunks = []
    
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        
        if end >= len(words):
            break
        
        start += chunk_size - overlap

    return chunks
