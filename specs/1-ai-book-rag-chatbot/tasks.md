# Feature Tasks: AI Book RAG Chatbot Debugging and Repair

**Feature Branch**: `1-ai-book-rag-chatbot`
**Created**: 2025-12-06
**Status**: In Progress

## Dependencies

User Story 3 (Indexing) is a prerequisite for User Story 1 (Ask Question) and User Story 2 (Ask with Highlighted Text).

## Parallel Execution Opportunities

- Tasks within the FastAPI Backend debugging can often be parallelized if they involve different files or independent modules.
- Frontend tasks can be parallelized with backend tasks once the backend API contracts are stable.

## Implementation Strategy

The approach will be an iterative debugging and repair process, focusing on foundational components first and then moving to user-facing features. Each phase will aim for an independently verifiable set of fixes.

---

## Phase 1: Setup

- [ ] T001 Verify project structure and essential files (e.g., `main.py`, `package.json`, `requirements.txt`).
- [ ] T002 Install/verify all backend dependencies from `requirements.txt` (or equivalent).
- [ ] T003 Install/verify all frontend dependencies from `package.json` (or equivalent).

## Phase 2: Foundational Debugging & Verification

### Independent Test:
Verify that LLM integration, embedding generation, Qdrant collection creation, and retrieval of relevant chunks are functional at a basic level, and no OpenAI paid models are being used.

- [ ] T004 [P] Verify Gemini LLM is correctly called via OpenAI Agents SDK/ChatKit-compatible endpoint, ensuring no OpenAI paid models are used. Inspect relevant backend files (e.g., `backend/app/llm_client.py`).
- [ ] T005 [P] Verify embedding generation properly utilizes the LLM embedding API. Inspect `backend/app/embedding_service.py`.
- [ ] T006 [P] Verify Qdrant collection `ai_book_rag_chunks` is created with `Cosine` similarity. Inspect `backend/app/qdrant_client.py` and Qdrant Cloud dashboard. (Note: collection name in code is `ai_book`)
- [ ] T007 [P] Test basic retrieval from Qdrant to ensure relevant chunks are returned for simple queries. Implement a temporary script for this (e.g., `backend/scripts/test_retrieval.py`). (Blocked: Gemini API quota exceeded)

## Phase 3: User Story 3 - Indexing and Embedding Documents (Debugging & Repair)

**Story Goal**: The system processes all textbook pages, chunks them, generates embeddings, and indexes them into Qdrant.
**Independent Test**: Run the indexing process and verify that the `ai_book_rag_chunks` collection exists in Qdrant and contains embedded and chunked documents from `/docs` with appropriate metadata.

- [ ] T008 [P] [US3] Debug and repair document parsing logic for Markdown and PDF files in `backend/app/document_parser.py`.
- [ ] T009 [P] [US3] Debug and repair text chunking strategy (500 tokens, 100 overlap) in `backend/app/chunking_service.py`.
- [ ] T010 [P] [US3] Debug and repair embedding generation calls for text chunks in `backend/app/embedding_service.py`.
- [ ] T011 [P] [US3] Debug and repair upsert logic for storing embeddings and metadata in Qdrant in `backend/app/qdrant_client.py`.
- [ ] T012 [US3] Implement and debug the end-to-end indexing workflow script (e.g., `backend/scripts/index_documents.py`).
- [ ] T013 [US3] Verify metadata schema correctness for indexed vectors (file_path, page_number, chunk_index, text_content). Inspect Qdrant collection.

## Phase 4: User Story 1 - Ask a Question (Debugging & Repair)

**Story Goal**: A user asks a question, and the chatbot provides an answer strictly based on the book's content or the specified fallback.
**Independent Test**: Ask a question related to the book content and verify an accurate, grounded response. Ask an out-of-scope question and verify the fallback message: "This answer is not in the textbook content."

- [ ] T014 [P] [US1] Debug and repair the retrieval pipeline to fetch relevant chunks for a given query in `backend/app/retrieval_service.py`.
- [ ] T015 [P] [US1] Debug and repair context window construction to prioritize relevant chunks for the LLM in `backend/app/context_builder.py`.
- [ ] T016 [P] [US1] Debug and repair the grounded RAG prompt, ensuring the LLM is instructed to answer strictly from provided context in `backend/app/rag_prompt.py`.
- [ ] T017 [P] [US1] Debug and repair the LLM call for response generation in `backend/app/llm_client.py`.
- [ ] T018 [US1] Implement and debug the fallback rule: "This answer is not in the textbook content." when no relevant content is found or the LLM cannot answer from context. Inspect `backend/app/chat_service.py`.

## Phase 5: User Story 2 - Ask with Highlighted Text (Debugging & Repair)

**Story Goal**: A user highlights text and asks a question, and the chatbot answers using *only* the selected text.
**Independent Test**: Highlight text and ask a question that can only be answered by the selected text, verifying the response is strictly grounded. Ask a question outside selected text (even if in book) and verify the fallback.

- [ ] T019 [P] [US2] Modify the retrieval pipeline to prioritize or exclusively use selected text for context when provided. Inspect `backend/app/retrieval_service.py` and `backend/app/context_builder.py`.
- [ ] T020 [P] [US2] Adjust the grounded RAG prompt to explicitly instruct the LLM to answer *only* from the highlighted text if available. Inspect `backend/app/rag_prompt.py`.
- [ ] T021 [US2] Verify the fallback rule for "ask-selected" when the answer is not in the highlighted text. Inspect `backend/app/chat_service.py`.

## Phase 6: FastAPI Backend (Debugging & Repair)

- [ ] T022 [P] Debug and repair existing FastAPI `/ask` endpoint logic to correctly integrate with RAG services. Inspect `backend/app/main.py`.
- [ ] T023 [P] Ensure FastAPI endpoint correctly handles incoming `question` and `selected_text` parameters. Inspect `backend/app/main.py` and Pydantic models.
- [ ] T024 [P] Verify and fix CORS configuration to allow requests from the frontend domain. Inspect `backend/app/main.py`.
- [ ] T025 [P] Implement comprehensive structured logging for requests, responses, and errors in the FastAPI application. Inspect `backend/app/main.py` and create `backend/app/logger.py`.
- [ ] T026 [P] Debug and repair error handling mechanisms in FastAPI to return appropriate HTTP status codes and informative messages. Inspect `backend/app/main.py` and custom exception handlers.
- [ ] T027 [P] Implement streaming output from FastAPI for LLM responses, including a placeholder/typing indicator. Inspect `backend/app/main.py` and streaming response logic.
- [ ] T028 [P] Resolve all general errors causing "something went wrong" messages across backend modules. Conduct a general code review of `backend/app/`.

## Phase 7: React Frontend (Debugging & Repair)

- [ ] T029 [P] Debug and repair the React chat widget to correctly send `POST` requests to the FastAPI `/ask` endpoint. Inspect relevant React component (e.g., `frontend/src/components/ChatWidget.js`).
- [ ] T030 [P] Implement/repair the logic to capture and inject selected text into the `/ask` request payload. Inspect `frontend/src/components/ChatWidget.js` or a utility file.
- [ ] T031 [P] Implement/repair the loading state display (e.g., typing indicator) in the chat widget. Inspect `frontend/src/components/ChatWidget.js`.
- [ ] T032 [P] Implement/repair the handling of streamed responses from the backend, updating the chat UI incrementally. Inspect `frontend/src/components/ChatWidget.js`.
- [ ] T033 [P] Configure the API base URL in the frontend for production deployment. Inspect `frontend/src/config.js` or environment variables setup.
- [ ] T034 [P] Resolve general frontend errors or UI glitches causing unexpected behavior.

## Phase 8: Polish & Cross-Cutting Concerns

- [ ] T035 Perform end-to-end verification of the entire RAG chatbot flow, from indexing to asking questions (general and selected text).
- [ ] T036 Conduct a final code review for cleanliness, adherence to architectural plan, and potential security vulnerabilities in both frontend and backend.
- [ ] T037 Update documentation (if necessary) with any significant changes or usage instructions.
- [ ] T038 Ensure all functional and non-functional requirements (SC-001 to SC-006) from `specs/1-ai-book-rag-chatbot/spec.md` are met.
