---
id: 1
title: AI Book RAG Chatbot Specification
stage: spec
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-book-rag-chatbot
branch: 1-ai-book-rag-chatbot
user: default
command: /sp.specify
labels: ["rag", "chatbot", "spec"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-book-rag-chatbot/spec.md
  - specs/1-ai-book-rag-chatbot/checklists/requirements.md
tests:
  - N/A
---

## Prompt

"""Generation (RAG) chatbot to be embedded inside the published AI Book website. The chatbot must use the Gemini LLM accessed strictly through the OpenAI Agents or ChatKit-compatible SDK endpoint for Gemini (which is free), not OpenAI’s paid models. The system must use FastAPI as the backend and Qdrant Cloud Free Tier as the vector database. All textbook pages located in the /docs directory must be embedded, chunked, and indexed into a Qdrant collection named “ai_book” with cosine similarity. The chatbot must answer user questions strictly based on the book’s content, and when the user highlights text, the chatbot must answer using only that selected text. If an answer falls outside the textbook contents, the chatbot must respond with: “This answer is not in the textbook content.” The system must include Qdrant indexing, embedding generation via Gemini’s embedding API through the OpenAI Agents SDK/ChatKit SDK, a retrieval pipeline, context building, a grounded RAG prompt, and a Gemini LLM call via OpenAI Agents SDK/ChatKit. The FastAPI backend must expose functional endpoints. The frontend chat widget must correctly call /ask, display a typing indicator, show streaming output if available, and support the ask-selected feature. The chatbot must follow strict grounding rules, prevent hallucinations, and operate reliably across all flows. """

## Response snapshot

The agent generated the initial feature specification for the "AI Book RAG Chatbot" based on the user's description. The specification was then iteratively refined to remove implementation-specific details and ensure it was written for non-technical stakeholders, as per the project guidelines. A quality checklist was also generated and used to validate the spec, with all items passing after the necessary refinements. The feature branch `1-ai-book-rag-chatbot` was created and the spec and checklist files were written to `specs/1-ai-book-rag-chatbot/spec.md` and `specs/1-ai-book-rag-chatbot/checklists/requirements.md` respectively.

## Outcome

- ✅ Impact: The specification for the AI Book RAG Chatbot has been successfully created and validated, providing a clear and technology-agnostic definition of the feature.
- 🧪 Tests: All items in the `requirements.md` checklist have passed, validating the quality and completeness of the specification.
- 📁 Files: `specs/1-ai-book-rag-chatbot/spec.md` and `specs/1-ai-book-rag-chatbot/checklists/requirements.md` were created/modified.
- 🔁 Next prompts: The feature is now ready for the `/sp.clarify` or `/sp.plan` phase.
- 🧠 Reflection: The process of iteratively refining the spec to meet the "no implementation details" and "non-technical stakeholders" criteria was successful.

## Evaluation notes (flywheel)

- Failure modes observed: The `create-phr.sh` bash script failed to execute, requiring a fallback to agent-native PHR creation.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Investigate the `pwsh` and `.specify/scripts/bash/create-phr.sh` execution issues for future automation improvements.