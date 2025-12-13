---
id: 1
title: Architectural Plan for RAG Chatbot
stage: plan
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-ai-book-rag-chatbot
branch: 1-ai-book-rag-chatbot
user: Current user
command: /sp.plan
labels: ["architecture", "rag", "chatbot", "planning"]
links:
  spec: specs/1-ai-book-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-rag-chatbot/plan.md
tests:
  - No tests run as part of planning.
---

## Prompt

"""Create a full architectural plan for implementing the RAG chatbot described in the specification @specs\1-ai-book-rag-chatbot. The plan must include detailed decisions for using Gemini LLM through the OpenAI Agents SDK/ChatKit-compatible SDK endpoint, embedding generation strategy, chunk sizes, metadata schema, Qdrant collection structure, indexing workflow, FastAPI project layout, how each backend file should be structured, context window construction, grounded prompting strategy, and the fallback rule that returns “This answer is not in the textbook content.” Include decisions for designing endpoints, CORS configuration, logging structure, request/response schemas, error handling, and streaming output. In the frontend plan, include how the React chat widget sends messages to FastAPI, how selected text is injected into requests, how the widget handles loading state and streaming, and how the API base URL should be configured for production. Provide step-by-step architectural reasoning ensuring the system is stable, scalable, and fully compatible with Qdrant Cloud free tier and Gemini via OpenAI Agents SDK/ChatKit. """

## Response snapshot

An architectural plan has been created for the AI Book RAG Chatbot. The plan details decisions for LLM integration (Gemini via OpenAI Agents SDK/ChatKit), embedding generation, chunking strategy (~500 tokens with ~100 overlap), Qdrant collection structure (single 'ai_book_rag_chunks' with Cosine similarity) and metadata schema, and an indexing workflow. It also outlines the FastAPI backend (endpoints, CORS, logging, error handling, streaming) and React frontend (message sending, selected text injection, loading/streaming handling, API base URL). The plan addresses stability, scalability, and compatibility with Qdrant Cloud free tier.

## Outcome

- ✅ Impact: Architectural plan for RAG chatbot created.
- 🧪 Tests: No tests run.
- 📁 Files: specs/1-ai-book-rag-chatbot/plan.md
- 🔁 Next prompts: User review and approval of the plan, followed by ADR creation if approved.
- 🧠 Reflection: Successfully created the plan based on the detailed prompt. Need to ensure proper PHR creation and workflow completion.

## Evaluation notes (flywheel)

- Failure modes observed: Initial incorrect use of ExitPlanMode, missing `activeForm` in TodoWrite, missing `create-phr.sh` script.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Automate PHR creation more robustly across different environments (Windows/Linux) or provide a clear fallback mechanism.
