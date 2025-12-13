---
adr_id: 0004
title: Chunking Strategy
status: Proposed
date: 2025-12-06
---

## Context

To effectively utilize the RAG pipeline, the raw textbook content must be divided into smaller, manageable pieces (chunks) suitable for embedding and retrieval. The chunking strategy significantly impacts the relevance and coherence of retrieved information and must be tuned to optimize LLM context windows.

## Decision

The chosen strategy is to implement a fixed-size chunking strategy with overlap. The initial chunk size will be approximately 500 tokens with an overlap of about 100 tokens.

**Components of this decision:**
- **Chunking Method**: Fixed-size chunking.
- **Chunk Size**: Approximately 500 tokens.
- **Overlap**: Approximately 100 tokens.

## Consequences

### Positive:
- **Simplicity**: Fixed-size chunking is straightforward to implement and manage, reducing development complexity.
- **Context Coherence**: Overlap between chunks helps to ensure that critical information or context that might span a chunk boundary is not lost, improving retrieval quality.
- **Optimized for LLM Context**: Provides chunks of a consistent size that can be easily managed within the LLM's context window, maximizing the amount of relevant information passed to the LLM.
- **Fine-tuning Capability**: The specific token counts can be easily adjusted and fine-tuned during testing to achieve optimal performance and grounding.

### Negative:
- **Potential for Arbitrary Breaks**: Fixed-size chunks may cut through sentences or paragraphs, potentially leading to less coherent individual chunks if not carefully managed (though overlap mitigates this). However, in RAG, the LLM aggregates information from multiple chunks.
- **Suboptimal Semantic Grouping**: May not always capture semantically complete units of information as effectively as more advanced chunking methods.
- **Token Limit Considerations**: If a single chunk is too large, it might exceed the embedding model's or LLM's token limits, requiring adjustments.

## Alternatives Considered

### 1. Semantic Chunking
- **Description**: A strategy that attempts to divide text into chunks based on semantic meaning or logical breaks (e.g., chapters, sections, paragraphs).
- **Pros**:
    - Chunks are more likely to represent complete ideas or topics.
    - Can potentially lead to more precise retrieval if semantic boundaries are clear.
- **Cons**:
    - More complex to implement, often requiring natural language processing (NLP) techniques or rule-based systems.
    - Variable chunk sizes can be challenging to manage within fixed LLM context windows.
    - Might require additional processing overhead.

### 2. Paragraph-based Chunking
- **Description**: Dividing the text solely based on paragraph breaks.
- **Pros**:
    - Simple to implement.
    - Each chunk is a naturally cohesive unit.
- **Cons**:
    - Highly variable chunk sizes: some paragraphs can be very short, others extremely long, leading to inefficient use of context windows or chunks exceeding token limits.
    - Lack of overlap can lead to loss of context if a critical idea spans multiple paragraphs.

## References

- [Plan: Architectural Plan: AI Book RAG Chatbot](specs/1-ai-book-rag-chatbot/plan.md)
