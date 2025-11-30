# Implementation Plan: AI-Book Hackathon Deliverables

**Branch**: `docs/update-constitution` | **Date**: 2025-11-29 | **Spec**: specs/ai-book/spec.md
**Input**: Feature specification from `/specs/ai-book/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation for the AI-Book Hackathon deliverables: an AI-generated Docusaurus textbook, an integrated RAG chatbot with a FastAPI backend and Qdrant Cloud indexing, and deployment to GitHub Pages. The plan respects the Docusaurus architecture, RAG pipeline, GitHub Pages deployment flow, and optional bonus features as modules.

## Technical Context

**Language/Version**: Python 3.11 (for FastAPI, RAG backend), JavaScript/TypeScript (for Docusaurus frontend)
**Primary Dependencies**: FastAPI, Qdrant Client, Docusaurus, OpenAI Agents/ChatKit SDKs, Neon Serverless Postgres
**Storage**: Qdrant Cloud (vector embeddings for RAG), Neon Serverless Postgres (for any other persistent data, e.g., user preferences if bonus features are expanded, though not explicitly required for initial RAG setup).
**Testing**: `pytest` for Python backend, Jest, React Testing Library, Cypress/Playwright for Docusaurus frontend (specific strategy to be defined).
**Target Platform**: Google Cloud Run (primary), AWS Lambda with API Gateway (alternative) for FastAPI backend; GitHub Pages for Docusaurus frontend.
**Project Type**: Web application (frontend Docusaurus, backend FastAPI)
**Performance Goals**: RAG chatbot responds to user queries within an average of 3 seconds (SC-003).
**Constraints**: Deployment must utilize GitHub Pages (FR-006). AI-generated content must be based solely on provided course details and hardware requirements. RAG chatbot must only answer questions based on the content of the AI-generated Docusaurus textbook. "Ask-selected" feature correctly identifies selected text and initiates a chatbot query in 95% of attempts (SC-005). Deployment to GitHub Pages within 3 attempts (SC-004).
**Scale/Scope**: Physical AI & Humanoid Robotics program textbook and interactive chatbot.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**I. AI/Spec-Driven Book Creation**: The project adheres to this principle by using Claude Code and Spec-Kit Plus for the creation and maintenance of the book, ensuring a structured and consistent content generation process.

**II. Docusaurus & GitHub Pages Deployment**: This plan fully adheres by building the book using Docusaurus and deploying it to GitHub Pages for public accessibility, version control, and collaborative content management.

**III. Integrated RAG Chatbot Development**: The plan adheres by integrating a RAG chatbot utilizing OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant Cloud Free Tier, capable of answering questions about the book's content, including user-selected text.

**IV. Physical AI & Robotics Curriculum Focus**: The content generation for the book will strictly focus on the Physical AI and Humanoid Robotics curriculum, covering specified topics like ROS 2, Gazebo, NVIDIA Isaac, and VLA, aligning with the course's core themes.

**V. Test-First Development (NON-NEGOTIABLE)**: This principle will be strictly followed during the implementation phase for all code components, especially for the RAG chatbot and any custom development, by adhering to a Test-Driven Development (TDD) approach with a Red-Green-Refactor cycle.

## Project Structure

### Documentation (this feature)

```text
specs/ai-book/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
.
├── backend/                  # FastAPI backend for RAG chatbot
│   ├── src/
│   │   ├── api/              # FastAPI endpoints
│   │   ├── services/         # RAG logic, Qdrant interaction
│   │   └── models/           # Data models for RAG (e.g., query, response)
│   └── tests/                # Unit and integration tests for backend
├── docs/                     # Docusaurus project root
│   ├── src/                  # Docusaurus custom pages, components
│   ├── docs/                 # Markdown files for textbook content
│   ├── blog/                 # Blog posts (if applicable)
│   ├── static/               # Static assets
│   ├── docusaurus.config.js
│   └── package.json
├── scripts/                  # Deployment scripts, utility scripts
├── .github/                  # GitHub Actions workflows for CI/CD, GitHub Pages deployment
└── .specify/                 # SpecKit Plus configuration and templates
```

**Structure Decision**: The chosen structure separates the Docusaurus frontend (`docs/`) from the FastAPI backend (`backend/`), allowing independent development and deployment while maintaining clear integration points. This aligns with a typical web application architecture and facilitates GitHub Pages deployment for the static Docusaurus site and a separate cloud deployment for the FastAPI backend.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
