# Feature Specification: AI Book RAG Chatbot

**Feature Branch**: `1-ai-book-rag-chatbot`
**Created**: 2025-12-05
**Status**: Draft
**Input**: User description: "Generation (RAG) chatbot to be embedded inside the published AI Book website. A RAG (Retrieval Augmented Generation) chatbot to be embedded within the AI Book website. The chatbot will answer user questions strictly based on the book’s content. If an answer falls outside the textbook contents, the chatbot will respond with: “This answer is not in the textbook content.” When a user highlights text, the chatbot will answer using only that selected text. The system will include document processing (chunking, embedding, indexing), a retrieval pipeline, context building, a grounded RAG prompt, and an LLM call. The backend must expose functional chat endpoints, and the frontend chat widget will support interactive features like calling `/ask`, displaying a typing indicator, streaming output, and an "ask-selected" feature. The chatbot will adhere to strict grounding rules, prevent hallucinations, and operate reliably."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask a Question (Priority: P1)

A user asks a question to the chatbot, and the chatbot provides an answer strictly based on the content of the AI Book.

**Why this priority**: Core functionality of the RAG chatbot.

**Independent Test**: Can be fully tested by asking a question related to the book content and verifying the answer is accurate and grounded.

**Acceptance Scenarios**:

1.  **Given** the chatbot is initialized with the AI Book content, **When** a user asks "What is RAG?", **Then** the chatbot responds with an answer derived solely from the book.
2.  **Given** the chatbot is initialized with the AI Book content, **When** a user asks a question whose answer is *not* in the book, **Then** the chatbot responds with "This answer is not in the textbook content."

---

### User Story 2 - Ask with Highlighted Text (Priority: P1)

A user highlights specific text on a book page and asks a question, and the chatbot answers using *only* the selected text.

**Why this priority**: Critical for contextual grounding and user control.

**Independent Test**: Can be fully tested by highlighting text and asking a question that can only be answered by the selected text, verifying the response.

**Acceptance Scenarios**:

1.  **Given** a user has highlighted a paragraph about "Large Language Models", **When** the user asks "What are LLMs?", **Then** the chatbot responds using only information from the highlighted text.
2.  **Given** a user has highlighted text, **When** the user asks a question whose answer is not in the highlighted text (but might be elsewhere in the book), **Then** the chatbot responds with "This answer is not in the textbook content."

---

### User Story 3 - Indexing and Embedding Documents (Priority: P1)

The system processes all textbook pages in the `/docs` directory, chunks them, generates embeddings, and indexes them into a dedicated collection within the vector database, using a similarity metric suitable for text embeddings.

**Why this priority**: Foundational for the RAG functionality.

**Independent Test**: Can be tested by running the indexing process and verifying that a dedicated collection is created in the vector database and contains the embedded and chunked documents.

**Acceptance Scenarios**:

1.  **Given** the `/docs` directory contains textbook pages, **When** the indexing process runs, **Then** a dedicated collection is created in the vector database.
2.  **Given** the indexing process completes, **When** inspecting the collection, **Then** it contains embedded and chunked content from all `/docs` pages with a suitable similarity metric for vector comparison.

---

### Edge Cases

- What happens when no relevant content is found for a query within the textbook or selected text?
  - The chatbot must respond with: "This answer is not in the textbook content."
- How does the system handle very long textbook pages during chunking and embedding?
  - The system should chunk documents effectively to maximize relevance and minimize token limits for embeddings and LLM context.
- What happens if the vector database's free tier limits are exceeded?
  - The system should gracefully handle errors related to database limitations, possibly logging warnings.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The chatbot MUST use a large language model (LLM) accessed through a compatible SDK endpoint for cost-effective AI integration.
-   **FR-002**: The system MUST use a robust web framework for the backend.
-   **FR-003**: The system MUST use a scalable vector database, leveraging its free tier.
-   **FR-004**: All textbook pages located in the `/docs` directory MUST be embedded, chunked, and indexed into a dedicated collection within the vector database, using a similarity metric suitable for text embeddings.
-   **FR-005**: The chatbot MUST answer user questions strictly based on the book’s content.
-   **FR-006**: When the user highlights text, the chatbot MUST answer using only that selected text.
-   **FR-007**: If an answer falls outside the textbook contents, the chatbot MUST respond with: “This answer is not in the textbook content.”
-   **FR-008**: The system MUST include a document indexing pipeline.
-   **FR-009**: The system MUST include embedding generation via an LLM embedding API through a compatible SDK.
-   **FR-010**: The system MUST include a retrieval pipeline.
-   **FR-011**: The system MUST include a context building mechanism.
-   **FR-012**: The system MUST include a grounded RAG prompt.
-   **FR-013**: The system MUST include an LLM call via a compatible SDK.
-   **FR-014**: The backend MUST expose functional endpoints for chat interaction (e.g., `/ask`).
-   **FR-015**: The frontend chat widget MUST correctly call the `/ask` endpoint.
-   **FR-016**: The frontend chat widget MUST display a typing indicator.
-   **FR-017**: The frontend chat widget MUST show streaming output if available.
-   **FR-018**: The frontend chat widget MUST support the "ask-selected" feature.
-   **FR-019**: The chatbot MUST follow strict grounding rules.
-   **FR-020**: The chatbot MUST prevent hallucinations.
-   **FR-021**: The chatbot MUST operate reliably across all flows.

### Key Entities *(include if feature involves data)*

-   **Textbook Page**: A document (e.g., markdown, PDF) located in the `/docs` directory, containing content from the AI Book.
-   **Text Chunk**: A segment of a textbook page, suitable for embedding and retrieval.
-   **Embedding**: A vector representation of a text chunk, generated by an LLM embedding API.
-   **Vector Database Collection**: A dedicated collection within the vector database storing embeddings and associated metadata.
-   **User Question**: Natural language query from the user.
-   **Highlighted Text**: Specific text selected by the user on a book page.
-   **Chatbot Response**: The answer provided by the RAG system to the user.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: 95% of user questions whose answers are present in the textbook content receive accurate and grounded responses.
-   **SC-002**: Chatbot response time for standard queries is under 5 seconds (p95 latency).
-   **SC-003**: The chatbot accurately identifies and responds with "This answer is not in the textbook content" for 98% of questions whose answers are truly outside the book's scope.
-   **SC-004**: When using the "ask-selected" feature, 99% of responses are strictly based on the highlighted text, and if not, the system indicates that the answer is not available in the selected text.
-   **SC-005**: The document indexing process successfully embeds and indexes all `/docs` content without errors within a reasonable time frame (e.g., under 10 minutes for current book size).
-   **SC-006**: The frontend typing indicator and streaming output function correctly, enhancing user experience.