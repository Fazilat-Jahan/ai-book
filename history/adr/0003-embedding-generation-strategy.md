---
adr_id: 0003
title: Embedding Generation Strategy
status: Proposed
date: 2025-12-06
---

## Context

The RAG chatbot requires converting text chunks from the AI Book into vector embeddings for efficient retrieval from Qdrant. The project specification implies using an LLM embedding API through a compatible SDK, aligning with the chosen Gemini LLM integration.

## Decision

The chosen strategy is to utilize an LLM embedding API via the OpenAI Agents SDK/ChatKit-compatible SDK endpoint for generating embeddings.

**Components of this decision:**
- **Embedding Service**: LLM embedding API (e.g., from Gemini provider).
- **Integration Method**: OpenAI Agents SDK/ChatKit-compatible SDK endpoint.

## Consequences

### Positive:
- **Consistency**: Ensures a consistent integration approach with the chosen LLM for generation, potentially simplifying dependency management and API key handling.
- **High-Quality Embeddings**: LLM-based embedding APIs typically provide high-quality, contextually rich embeddings crucial for effective semantic search and retrieval in RAG systems.
- **Simplified Development**: The SDK abstraction can streamline the process of making embedding API calls, handling rate limits, and batching.

### Negative:
- **API Cost**: Embedding generation incurs API costs, which need to be monitored to stay within budget, especially during indexing and frequent updates.
- **Rate Limiting**: Potential for hitting API rate limits during large-scale indexing or high query volumes, requiring robust retry mechanisms.
- **Dependency**: Reliance on an external embedding service introduces an external dependency that could impact system availability and performance.

## Alternatives Considered

### 1. Standalone Embedding Models (e.g., Sentence-BERT, custom models)
- **Description**: Hosting and running a separate, open-source or custom-trained embedding model locally or on a dedicated service.
- **Pros**:
    - Potentially lower per-call cost after initial setup.
    - More control over the embedding model and its updates.
    - No external API rate limits (if self-hosted).
- **Cons**:
    - Increased operational complexity and maintenance overhead for hosting and managing the model.
    - Requires significant computational resources (GPU) for efficient embedding generation, especially for large datasets.
    - Initial development effort is higher to integrate and fine-tune a standalone model.

### 2. Pre-computed Embeddings
- **Description**: Generating all embeddings once and storing them, without re-generating on the fly.
- **Pros**:
    - Eliminates real-time embedding generation latency for queries.
    - Can reduce ongoing API costs if content is static and updates are infrequent.
- **Cons**:
    - Less flexible for dynamic content updates or changes to the embedding model.
    - Requires a robust storage and lookup mechanism for pre-computed embeddings.
    - Initial computation time can be significant for large datasets.

## References

- [Plan: Architectural Plan: AI Book RAG Chatbot](specs/1-ai-book-rag-chatbot/plan.md)
