# Feature Specification: RAG Chatbot for AI Book

**Feature Branch**: `1-rag-chatbot-ai-book`
**Created**: 2025-12-05
**Status**: Draft
**Input**: User description: "Generation (RAG) chatbot to be embedded inside the published AI Book website. The chatbot must use the Gemini LLM accessed strictly through the OpenAI Agents or ChatKit-compatible SDK endpoint for Gemini (which is free), not OpenAI’s paid models. The system must use FastAPI as the backend and Qdrant Cloud Free Tier as the vector database. All textbook pages located in the /docs directory must be embedded, chunked, and indexed into a Qdrant collection named “ai_book” with cosine similarity. The chatbot must answer user questions strictly based on the book’s content, and when the user highlights text, the chatbot must answer using only that selected text. If an answer falls outside the textbook contents, the chatbot must respond with: “This answer is not in the textbook content.” The system must include Qdrant indexing, embedding generation via Gemini’s embedding API through the OpenAI Agents SDK/ChatKit SDK, a retrieval pipeline, context building, a grounded RAG prompt, and a Gemini LLM call via OpenAI Agents SDK/ChatKit. The FastAPI backend must expose functional endpoints. The frontend chat widget must correctly call /ask, display a typing indicator, show streaming output if available, and support the ask-selected feature. The chatbot must follow strict grounding rules, prevent hallucinations, and operate reliably across all flows."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask a Question (Priority: P1)

As a user of the AI Book website, I want to ask questions about the book's content and receive accurate answers, so that I can quickly understand concepts and find information.

**Why this priority**: This is the core functionality and primary value proposition of the chatbot. Without it, the chatbot serves no purpose.

**Independent Test**: The user can ask a question related to the AI Book content, and the chatbot provides a correct, grounded answer based solely on the book's content.

**Acceptance Scenarios**:

1.  **Given** the user is on the AI Book website, **When** the user types a question related to the textbook content, **Then** the chatbot responds with an answer derived strictly from the textbook.
2.  **Given** the user is on the AI Book website, **When** the user types a question whose answer is not present in the textbook content, **Then** the chatbot responds with: "This answer is not in the textbook content."
3.  **Given** the user is on the AI Book website, **When** the chatbot is generating a response, **Then** a typing indicator is displayed.
4.  **Given** the user is on the AI Book website, **When** the chatbot generates a response, **Then** the response is displayed as streaming output if available.

---

### User Story 2 - Ask Selected Text (Priority: P1)

As a user of the AI Book website, I want to highlight specific text and ask a question based only on that selected text, so that I can get highly focused answers.

**Why this priority**: This provides a unique and valuable interaction mode, enhancing the user's ability to deeply engage with specific parts of the book.

**Independent Test**: The user can highlight text and ask a question, and the chatbot provides an answer based *only* on the highlighted text, or indicates if the answer is not derivable from it.

**Acceptance Scenarios**:

1.  **Given** the user is on the AI Book website and has highlighted text, **When** the user asks a question while selected text is active, **Then** the chatbot responds with an answer derived strictly from the highlighted text.
2.  **Given** the user is on the AI Book website and has highlighted text, **When** the user asks a question whose answer is not present in the highlighted text, **Then** the chatbot responds with: "This answer is not in the textbook content."

---

### User Story 3 - Content Indexing and Search (Priority: P2)

As a system administrator, I want the AI Book's content to be accurately indexed and searchable, so that the chatbot can reliably retrieve relevant information to answer user questions.

**Why this priority**: This is a foundational system requirement that enables the core chatbot functionality. It's not a direct user interaction but crucial for the system's operation.

**Independent Test**: All textbook pages are successfully embedded, chunked, and indexed into the vector database, and relevant content can be retrieved for sample queries.

**Acceptance Scenarios**:

1.  **Given** new or updated textbook pages in the `/docs` directory, **When** the indexing process runs, **Then** all pages are chunked, embedded using Gemini's embedding API via OpenAI Agents SDK/ChatKit SDK, and indexed into a Qdrant collection named "ai_book" with cosine similarity.
2.  **Given** a query, **When** the retrieval pipeline is executed, **Then** relevant chunks of information are accurately retrieved from the "ai_book" Qdrant collection.

---

### Edge Cases

-   **What happens when network connectivity to Qdrant Cloud or Gemini API is lost?** The system should gracefully handle API failures and inform the user if the chatbot is temporarily unavailable.
-   **How does system handle very long user questions or selected text?** The system should handle input lengths within the limits of the embedding and LLM models, potentially truncating or summarizing if necessary, and informing the user.
-   **What if the `/docs` directory is empty or contains non-text files?** The indexing process should handle these cases without crashing, potentially skipping non-text files and reporting warnings.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST provide a RAG chatbot embedded within the AI Book website.
-   **FR-002**: The chatbot MUST use the Gemini LLM for conversational responses.
-   **FR-003**: The chatbot MUST access the Gemini LLM strictly through the OpenAI Agents or ChatKit-compatible SDK endpoint for Gemini (free tier).
-   **FR-004**: The chatbot MUST use Qdrant Cloud Free Tier as the vector database.
-   **FR-005**: All textbook pages located in the `/docs` directory MUST be chunked, embedded, and indexed into a Qdrant collection named “ai_book” with cosine similarity.
-   **FR-006**: The chatbot MUST answer user questions strictly based on the book’s content.
-   **FR-007**: When a user highlights text, the chatbot MUST answer using only that selected text.
-   **FR-008**: If an answer falls outside the textbook contents (or highlighted text), the chatbot MUST respond with: “This answer is not in the textbook content.”
-   **FR-009**: The system MUST include a retrieval pipeline for fetching relevant context.
-   **FR-010**: The system MUST include context building mechanism to prepare retrieved information for the LLM.
-   **FR-011**: The system MUST include a grounded RAG prompt to guide the LLM's response generation.
-   **FR-012**: The FastAPI backend MUST expose functional endpoints for chatbot interaction.
-   **FR-013**: The frontend chat widget MUST correctly call the `/ask` endpoint.
-   **FR-014**: The frontend chat widget MUST display a typing indicator when the chatbot is generating a response.
-   **FR-015**: The frontend chat widget MUST show streaming output if available from the backend.
-   **FR-016**: The frontend chat widget MUST support the "ask-selected" feature (asking questions based on highlighted text).
-   **FR-017**: The chatbot MUST follow strict grounding rules to prevent hallucinations.
-   **FR-018**: The chatbot MUST operate reliably across all flows.

### Key Entities *(include if feature involves data)*

-   **Textbook Page**: Represents a single page or document from the `/docs` directory. Key attribute: content, path.
-   **Text Chunk**: A segment of a textbook page, suitable for embedding. Key attributes: content, source (page, start/end).
-   **Vector Embedding**: A numerical representation of a text chunk, used for similarity search. Key attribute: vector.
-   **Qdrant Collection**: A storage for vector embeddings and associated metadata. Key attribute: "ai_book".
-   **User Query**: The text input from the user, either a direct question or a question based on highlighted text.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: 95% of user questions related to textbook content receive accurate answers derived solely from the book.
-   **SC-002**: 100% of responses for questions outside textbook content correctly state: "This answer is not in the textbook content."
-   **SC-003**: The chatbot responds to a typical user question within 5 seconds (p90).
-   **SC-004**: All textbook pages in `/docs` are successfully indexed within 60 seconds of an indexing process run.
-   **SC-005**: The frontend chat widget correctly renders typing indicators and streaming responses in 100% of observed interactions.
-   **SC-006**: 98% of "ask-selected" queries produce answers grounded only in the selected text.
-   **SC-007**: Hallucination rate is less than 1% across all measured interactions.
