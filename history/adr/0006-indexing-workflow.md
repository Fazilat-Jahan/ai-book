---
adr_id: 0006
title: Indexing Workflow
status: Proposed
date: 2025-12-06
---

## Context

The RAG chatbot requires a robust and repeatable process to ingest raw textbook content from the `/docs` directory, process it into embeddings, and store it in the Qdrant vector database. This indexing workflow is foundational for the chatbot's knowledge base.

## Decision

The chosen indexing workflow consists of a sequential, multi-step process:
1.  **Read Documents**: Identify and read all relevant files from the `/docs` directory (e.g., Markdown, PDF).
2.  **Parse Content**: Extract raw text content from each document. This will involve using appropriate libraries for different file types (e.g., `pypdf` for PDFs, simple file read for Markdown).
3.  **Chunk Text**: Apply the fixed-size chunking strategy with overlap (as defined in ADR-0004) to divide the raw text into manageable segments.
4.  **Generate Embeddings**: For each text chunk, call the LLM embedding API via the OpenAI Agents SDK/ChatKit-compatible SDK (as defined in ADR-0003) to generate its vector representation.
5.  **Store in Qdrant**: Upsert each generated embedding along with its associated metadata (e.g., `file_path`, `page_number`, `chunk_index`, `text_content`) into the `ai_book_rag_chunks` collection in Qdrant (as defined in ADR-0005).
6.  **Error Handling**: Implement comprehensive error logging at each step. Incorporate retry mechanisms (e.g., exponential backoff) for transient issues with external API calls (embedding service, Qdrant).

## Consequences

### Positive:
- **Reliability**: A clear, sequential workflow with explicit error handling and retries ensures that the indexing process is robust and less prone to failures.
- **Modularity**: Decoupling parsing, chunking, embedding, and storage into distinct steps promotes modularity, making it easier to test, debug, and update individual components.
- **Data Integrity**: Storing relevant metadata alongside embeddings in Qdrant facilitates precise retrieval, debugging, and understanding of the source content for each chunk.
- **Idempotence**: The upsert operation in Qdrant means that re-running the indexing process will update or replace existing vectors, ensuring data consistency without creating duplicates.

### Negative:
- **Initial Setup Time**: Requires careful implementation and configuration of multiple steps and libraries, leading to a moderate initial setup time.
- **Resource Consumption**: Generating embeddings for all documents can be resource-intensive (API calls, processing) and might take a noticeable amount of time for a large corpus.
- **Complexity for Updates**: While idempotent, a full re-indexing is required for significant changes to source documents or the chunking strategy, which can be time-consuming.

## Alternatives Considered

### 1. Batch Processing / Asynchronous Indexing
- **Description**: Instead of a strict sequential flow for individual documents, process documents in batches or use asynchronous tasks for embedding generation and Qdrant upserts.
- **Pros**:
    - Potentially faster overall indexing time for very large datasets by parallelizing operations.
    - Can be more efficient in terms of API calls if the embedding service supports batch inference.
- **Cons**:
    - Significantly increases implementation complexity due to managing concurrent tasks, synchronization, and error handling across batches.
    - May not be necessary for the initial scope with a relatively static book content.
    - Harder to debug individual document processing failures.

### 2. Real-time / On-demand Indexing
- **Description**: Indexing documents only when they are requested or accessed by the chatbot, rather than pre-indexing the entire corpus.
- **Pros**:
    - Reduced upfront processing and storage costs.
    - Only indexes what is actually used.
- **Cons**:
    - Introduces latency for the first query of a new document, as indexing would happen synchronously.
    - Significantly complicates the retrieval and context-building pipeline, as it would need to handle both indexed and unindexed content.
    - Unsuitable for a RAG system that relies on a pre-built knowledge base for comprehensive answers.

## References

- [Plan: Architectural Plan: AI Book RAG Chatbot](specs/1-ai-book-rag-chatbot/plan.md)
- [ADR-0003: Embedding Generation Strategy](history/adr/0003-embedding-generation-strategy.md)
- [ADR-0004: Chunking Strategy](history/adr/0004-chunking-strategy.md)
- [ADR-0005: Qdrant Collection Structure](history/adr/0005-qdrant-collection-structure.md)
