---
adr_id: 0005
title: Qdrant Collection Structure
status: Proposed
date: 2025-12-06
---

## Context

The RAG chatbot requires a scalable vector database to store and retrieve document embeddings efficiently. Qdrant Cloud Free Tier has been chosen as the vector database. A clear structure for the collection is necessary to ensure effective retrieval and management of embedded textbook content.

## Decision

The chosen strategy is to use a single dedicated collection named `ai_book_rag_chunks` within Qdrant, configured with a `Cosine` similarity metric.

**Components of this decision:**
- **Number of Collections**: Single collection.
- **Collection Name**: `ai_book_rag_chunks`.
- **Similarity Metric**: `Cosine` similarity.

## Consequences

### Positive:
- **Simplicity**: Using a single collection simplifies the architecture, development, and maintenance, especially for an initial deployment with a single source of truth (the AI Book).
- **Qdrant Free Tier Compatibility**: A single collection aligns well with the limitations and offerings of the Qdrant Cloud Free Tier.
- **Effective Retrieval**: Cosine similarity is a widely accepted and highly effective metric for comparing text embeddings, providing accurate semantic search results.
- **Focused Data Management**: All RAG-related vector data is centralized, making indexing, querying, and updates more straightforward.

### Negative:
- **Scalability Limitation (Future)**: While suitable for the current scope, if the RAG system were to expand to multiple, vastly different knowledge bases, a single collection might become less efficient for distinct retrieval needs. This can be mitigated by adding filters in Qdrant queries.
- **Potential for Overload (Free Tier)**: If the textbook content grows significantly beyond initial expectations, the free tier limits (e.g., storage capacity) for a single collection could be reached, requiring an upgrade.

## Alternatives Considered

### 1. Multiple Qdrant Collections
- **Description**: Creating separate Qdrant collections for different logical segments of the book, different document types, or even different versions of the book.
- **Pros**:
    - Better logical separation of data, which could be beneficial for very complex knowledge bases.
    - Potentially allows for fine-tuning similarity metrics or indexing parameters per collection.
- **Cons**:
    - Increased management overhead for multiple collections.
    - May exceed Qdrant Cloud Free Tier limits more quickly.
    - Adds complexity to the retrieval pipeline, requiring logic to decide which collection to query.

### 2. Different Similarity Metrics (e.g., Dot Product, Euclidean Distance)
- **Description**: Using alternative vector similarity metrics provided by Qdrant.
- **Pros**:
    - Could be theoretically more appropriate for specific types of embeddings or use cases (e.g., Dot Product for certain recommendation systems).
- **Cons**:
    - Cosine similarity is the most common and robust choice for text embeddings due to its focus on direction rather than magnitude, which is generally desired in NLP tasks.
    - Using less common metrics might require additional research and validation to ensure optimal performance for RAG.

## References

- [Plan: Architectural Plan: AI Book RAG Chatbot](specs/1-ai-book-rag-chatbot/plan.md)
