# Architectural Plan: AI Book RAG Chatbot

**Feature Branch**: `1-ai-book-rag-chatbot`
**Created**: 2025-12-06
**Status**: Draft

## 1. Scope and Dependencies

### In Scope:
- RAG chatbot implementation for AI Book website.
- Answering user questions strictly based on book content.
- "Ask-selected" feature: answering questions using only highlighted text.
- Document processing: chunking, embedding, indexing.
- Retrieval pipeline, context building, grounded RAG prompt, LLM call.
- FastAPI backend with functional chat endpoints.
- React frontend chat widget with interactive features (typing indicator, streaming output).
- Compatibility with Qdrant Cloud free tier and Gemini LLM via OpenAI Agents SDK/ChatKit.
- CORS configuration, logging, request/response schemas, error handling, streaming output.
- API base URL configuration for production.

### Out of Scope:
- User authentication/authorization.
- Advanced chat features (e.g., chat history persistence beyond session, multi-turn conversations not directly related to book content).
- Content ingestion from sources other than the `/docs` directory.
- Complex UI customizations beyond basic chat widget functionality.
- High-availability or disaster recovery solutions beyond Qdrant Cloud free tier capabilities.

### External Dependencies:
- **Gemini LLM**: Provided by OpenAI Agents SDK/ChatKit-compatible SDK endpoint.
- **Qdrant Cloud**: Vector database (free tier).
- **FastAPI**: Python web framework for the backend.
- **React**: JavaScript library for the frontend.
- **Python libraries**: for document parsing (e.g., `pypdf`, `markdown-it-py`), text chunking, embedding generation, Qdrant client, OpenAI Agents SDK/ChatKit.

## 2. Key Decisions and Rationale

### LLM Integration Strategy:
- **Decision**: Use Gemini LLM through the OpenAI Agents SDK/ChatKit-compatible SDK endpoint.
- **Rationale**: Leverages existing OpenAI Agents SDK/ChatKit integration patterns, potentially simplifying setup and ensuring compatibility with an established ecosystem. Gemini LLM provides robust generation capabilities.
- **Alternatives Considered**: Direct Gemini API integration (more complex setup, less abstraction), other LLM providers (not specified in requirements).

### Embedding Generation Strategy:
- **Decision**: Utilize an LLM embedding API via the OpenAI Agents SDK/ChatKit-compatible SDK endpoint.
- **Rationale**: Ensures consistency with the chosen LLM integration and simplifies dependency management. Provides high-quality embeddings crucial for effective RAG.
- **Alternatives Considered**: Standalone embedding models (increased complexity), pre-computed embeddings (less flexible for dynamic content).

### Chunking Strategy:
- **Decision**: Implement a fixed-size chunking strategy with overlap, tuned to balance context coherence and retrieval granularity. Initial chunk size: ~500 tokens with ~100 token overlap.
- **Rationale**: Fixed-size chunks are simpler to implement and manage. Overlap helps maintain context across chunk boundaries, improving retrieval quality. Specific token counts will be fine-tuned during testing.
- **Alternatives Considered**: Semantic chunking (more complex, requires additional processing), paragraph-based chunking (variable size, can lead to very large or very small chunks).

### Metadata Schema for Qdrant:
- **Decision**: Each stored vector will include metadata: `{"file_path": "path/to/doc.pdf", "page_number": 1, "chunk_index": 0, "text_content": "original text chunk"}`.
- **Rationale**: Enables precise filtering during retrieval (e.g., by document or page), provides context for grounded prompting, and allows debugging by inspecting original text.
- **Alternatives Considered**: Minimal metadata (less filtering capability), external metadata store (increased complexity).

### Qdrant Collection Structure:
- **Decision**: A single dedicated collection named `ai_book_rag_chunks`. Configured with `Cosine` similarity metric.
- **Rationale**: Simplicity of a single collection. Cosine similarity is a standard and effective metric for text embeddings. Qdrant Cloud free tier is suitable for a single collection.
- **Alternatives Considered**: Multiple collections (more complex to manage for a single book), other similarity metrics (less commonly used for text embeddings).

### Indexing Workflow:
1.  **Read Documents**: Read all files from the `/docs` directory (e.g., `.md`, `.pdf`).
2.  **Parse Content**: Extract raw text from each document (using `pypdf` for PDFs, simple read for Markdown).
3.  **Chunk Text**: Apply the fixed-size chunking strategy with overlap.
4.  **Generate Embeddings**: For each chunk, call the LLM embedding API via OpenAI Agents SDK/ChatKit.
5.  **Store in Qdrant**: Upsert each embedding along with its metadata (file_path, page_number, chunk_index, text_content) into the `ai_book_rag_chunks` collection.
6.  **Error Handling**: Log errors during any step; implement retries for embedding API calls.

- **Rationale**: A clear, sequential process ensures all content is processed and indexed reliably. Decoupling parsing, chunking, and embedding allows for modularity and easier debugging.
- **Alternatives Considered**: Batch processing (more complex for initial implementation), real-time indexing (overkill for static book content).

## 3. Interfaces and API Contracts

### Public APIs (FastAPI Backend):

#### 1. `POST /ask`
- **Description**: Receives a user question and optionally highlighted text, returns a grounded response from the RAG chatbot.
- **Inputs**:
    - `question`: `str` (required) - The user's query.
    - `selected_text`: `Optional[str]` (default: `None`) - Text highlighted by the user.
- **Outputs (Streaming)**:
    - `response_chunk`: `str` - Streamed portions of the chatbot's answer.
    - `status`: `str` - "success" or "error".
- **Errors**:
    - `400 Bad Request`: Invalid input (e.g., empty question).
    - `500 Internal Server Error`: Backend processing failure, LLM error, Qdrant error.
    - `503 Service Unavailable`: External service (LLM/Qdrant) not reachable.

#### 2. `GET /health` (Optional but recommended)
- **Description**: Health check endpoint for monitoring.
- **Inputs**: None.
- **Outputs**: `{"status": "ok"}`
- **Errors**: `500 Internal Server Error`: If any critical dependency (e.g., Qdrant connection) is unhealthy.

### Versioning Strategy:
- **Decision**: Initial API will not have explicit versioning (e.g., `/v1`). If needed in the future, versioning will be introduced via path (`/api/v1/ask`).
- **Rationale**: Simplifies initial development.

### Idempotency, Timeouts, Retries:
- **Decision**:
    - **Idempotency**: Not directly applicable for chat interactions as each query is unique.
    - **Timeouts**: Configure reasonable timeouts for external LLM and Qdrant API calls (e.g., 30-60 seconds).
    - **Retries**: Implement exponential backoff retries for transient errors with LLM and Qdrant API calls (e.g., 3 retries).
- **Rationale**: Ensures robustness against transient network issues or service unavailability.

### Error Taxonomy with Status Codes:
- **400 Bad Request**: Malformed or invalid user input.
- **404 Not Found**: (Not directly applicable to `/ask`, but for other potential endpoints).
- **403 Forbidden**: (Not applicable for current scope without auth).
- **500 Internal Server Error**: Unhandled exceptions, logical errors in backend, LLM/Qdrant specific errors.
- **502 Bad Gateway**: Upstream service (LLM, Qdrant) returns an error.
- **503 Service Unavailable**: Upstream service is unreachable or unresponsive.

## 4. Non-Functional Requirements (NFRs) and Budgets

### Performance:
- **p95 latency**: < 5 seconds for standard queries (SC-002).
- **Throughput**: Support ~10-20 concurrent users for the initial free tier deployment.
- **Resource caps**: Monitor FastAPI process CPU/Memory usage to stay within free tier limits of hosting platform.

### Reliability:
- **SLOs**: 99% uptime for the `/ask` endpoint during operational hours.
- **Error budgets**: Track successful vs. error responses.
- **Degradation strategy**: If LLM/Qdrant services are degraded, return a polite error message to the user rather than crashing (e.g., "Sorry, I'm having trouble connecting to my knowledge base right now. Please try again later.").

### Security:
- **AuthN/AuthZ**: Not in scope for initial implementation.
- **Data handling**: No sensitive user data collected or stored. Input questions and selected text are processed in-memory for response generation.
- **Secrets**: LLM API keys and Qdrant API keys will be managed via environment variables (e.g., `.env` file for local development, secrets management service for deployment).
- **Auditing**: Basic logging of requests and responses for debugging and monitoring, but no personally identifiable information.

### Cost:
- **Unit economics**: Optimized for Qdrant Cloud free tier and cost-effective Gemini LLM usage. Monitor token usage for LLM calls.

## 5. Data Management and Migration

### Source of Truth:
- **Textbook Content**: `/docs` directory in the repository is the source of truth for the RAG content.
- **Embeddings/Vectors**: Qdrant collection is the source of truth for indexed embeddings.

### Schema Evolution:
- **Qdrant Metadata**: If metadata schema changes, a re-indexing process will be required to update existing vectors. Backward compatibility will be considered for minor changes.
- **Document Structure**: Changes to document structure in `/docs` will necessitate a full re-indexing.

### Migration and Rollback:
- **Indexing**: The indexing process is idempotent. Rerunning it will update/replace existing vectors.
- **Qdrant Collection**: For major schema changes, a new collection might be created, indexed, and then swapped. Old collections can be retained for rollback if needed.

### Data Retention:
- **Qdrant**: Data retained as long as the collection exists within Qdrant Cloud. No explicit retention policy for chat interactions (since not stored).

## 6. Operational Readiness

### Observability:
- **Logging**:
    - **Backend (FastAPI)**: Standard Python `logging` module. Log requests, responses, errors, LLM calls, Qdrant interactions, and performance metrics (e.g., query latency). Log level configurable (DEBUG, INFO, WARNING, ERROR).
    - **Frontend (React)**: Browser console logs for client-side errors and network requests.
- **Metrics**: Track API call counts, error rates, average response times for `/ask` endpoint.
- **Traces**: (Optional for initial scope) If performance issues arise, consider adding distributed tracing (e.g., OpenTelemetry) for complex interactions.

### Alerting:
- **Thresholds**: Alerts for sustained high error rates (e.g., 5xx errors > 5% for 5 minutes), service unavailability, or exceeding Qdrant/LLM rate limits.
- **On-call owners**: Standard operational procedures for alert handling (not specified here, but would be part of overall project ops).

### Runbooks for Common Tasks:
- **Indexing Runbook**: Step-by-step guide for re-indexing documents.
- **Troubleshooting Runbook**: Guide for common errors (e.g., LLM API key issues, Qdrant connection problems, content grounding failures).

### Deployment and Rollback strategies:
- **Deployment**: Containerized deployment (e.g., Docker) for both backend and frontend. CI/CD pipeline to deploy new versions.
- **Rollback**: Ability to quickly revert to a previous stable deployment (e.g., by deploying a previous Docker image).

### Feature Flags and compatibility:
- **Decision**: No feature flags for initial implementation.
- **Rationale**: Keep it simple for V1.

## 7. Risk Analysis and Mitigation

### Top 3 Risks:

1.  **LLM Hallucinations / Poor Grounding**:
    - **Blast Radius**: Chatbot provides incorrect or misleading information, eroding user trust.
    - **Mitigation**:
        - Strict grounded prompting (instruct LLM to answer only from provided context).
        - Fallback rule: "This answer is not in the textbook content." when no relevant chunks found or LLM explicitly refuses to answer from context.
        - Robust context window construction to prioritize relevant chunks.
        - Extensive testing with out-of-scope questions and challenging queries.
        - Continuous monitoring of LLM responses.

2.  **Qdrant Cloud Free Tier Limitations**:
    - **Blast Radius**: Service disruption if limits (e.g., storage, request rate) are hit, leading to unavailability.
    - **Mitigation**:
        - Monitor Qdrant usage metrics closely.
        - Optimize chunking strategy to minimize vector storage while maintaining quality.
        - Implement graceful degradation/error handling if limits are approached or exceeded.
        - Have a clear upgrade path documented for paid tiers.

3.  **Performance Degradation (Latency)**:
    - **Blast Radius**: Slow responses lead to poor user experience, potentially making the chatbot unusable.
    - **Mitigation**:
        - Optimize embedding generation (batching, efficient API calls).
        - Optimize Qdrant queries (index configuration, efficient filters).
        - Implement caching for frequently accessed information (if applicable, though RAG dynamically builds context).
        - Monitor p95 latency and throughput, identify bottlenecks through profiling.
        - Stream LLM output to provide immediate feedback to the user.

## 8. Evaluation and Validation

### Definition of Done (tests, scans):
- **Unit Tests**: For individual functions (chunking, embedding, Qdrant client interactions, FastAPI endpoints, React components).
- **Integration Tests**: For the RAG pipeline end-to-end (indexing process, `/ask` endpoint).
- **End-to-End (E2E) Tests**: Simulate user interactions with the frontend to verify the full flow, including "ask-selected" and streaming.
- **Performance Tests**: Benchmark `/ask` endpoint latency and throughput.
- **Security Scans**: (Optional for V1) Basic SAST/DAST scans for FastAPI backend.
- **Linter/Formatter Checks**: Ensure code quality and consistency.

### Output Validation for format/requirements/safety:
- **Groundedness Check**: Programmatic checks (or manual review in early stages) to ensure LLM responses are derived *only* from provided context.
- **Fallback Rule Validation**: Verify the "This answer is not in the textbook content." message is returned correctly for out-of-scope questions or irrelevant selected text.
- **API Schema Validation**: Ensure requests and responses adhere to defined OpenAPI schemas.
- **Frontend UI Validation**: Verify typing indicator, streaming, and "ask-selected" visual behavior.

## 9. Architectural Decision Record (ADR)

- 📋 Architectural decision detected: LLM Integration Strategy — Document reasoning and tradeoffs? Run `/sp.adr LLM Integration Strategy`
- 📋 Architectural decision detected: Embedding Generation Strategy — Document reasoning and tradeoffs? Run `/sp.adr Embedding Generation Strategy`
- 📋 Architectural decision detected: Chunking Strategy — Document reasoning and tradeoffs? Run `/sp.adr Chunking Strategy`
- 📋 Architectural decision detected: Qdrant Collection Structure — Document reasoning and tradeoffs? Run `/sp.adr Qdrant Collection Structure`
- 📋 Architectural decision detected: Indexing Workflow — Document reasoning and tradeoffs? Run `/sp.adr Indexing Workflow`
- 📋 Architectural decision detected: FastAPI Backend Architecture — Document reasoning and tradeoffs? Run `/sp.adr FastAPI Backend Architecture`
- 📋 Architectural decision detected: React Frontend Architecture — Document reasoning and tradeoffs? Run `/sp.adr React Frontend Architecture`
