# Tasks: AI-Book Hackathon Deliverables

**Feature Branch**: `0001-ai-book-hackathon` | **Date**: 2025-11-29 | **Plan**: specs/ai-book/plan.md
**Input**: Feature specification (`specs/ai-book/spec.md`), Implementation Plan (`specs/ai-book/plan.md`), Data Model (`specs/ai-book/data-model.md`), API Contracts (`specs/ai-book/contracts/chatbot-api.yaml`), Research Findings (`specs/ai-book/research.md`)

## Summary

This document outlines the atomic development tasks for the AI-Book Hackathon project, broken down into phases corresponding to user stories and project milestones. Each task is designed to be 15-30 minutes, have a single acceptance criterion, and produce a verifiable output.

## Implementation Strategy

The project will be implemented incrementally, prioritizing core functionalities (User Stories 1, 2, 3) before optional bonus features (User Story 4). Tasks are ordered to manage dependencies, with opportunities for parallel execution identified.

---

## Phase 1: Setup & Architecture
**Checkpoint**: Initial project structure is established, basic Docusaurus and FastAPI setups are complete, and foundational configurations are in place.

### Foundational Tasks
- [ ] T000 [P] Place initial course details and hardware requirements in `data/raw/`
  - Acceptance: `data/raw/course_details.txt` and `data/raw/hardware_requirements.txt` exist.
  - Output: Project data files.
- [ ] T001 Create base project directories: `backend/`, `docs/`, `scripts/`, `.github/`, `data/raw/`
  - Acceptance: Directories exist at repository root.
  - Output: Project directory structure.
- [ ] T002 Initialize Docusaurus project in `docs/`
  - Acceptance: Docusaurus project is created and `npm install` runs successfully in `docs/`.
  - Output: `docs/package.json` and Docusaurus boilerplate files.
- [ ] T003 Configure `docusaurus.config.js` for GitHub Pages deployment
  - Acceptance: `baseUrl`, `projectName`, `organizationName` (if applicable) are correctly set in `docs/docusaurus.config.js`.
  - Output: Updated `docs/docusaurus.config.js`.
- [ ] T004 Initialize FastAPI project in `backend/`
  - Acceptance: Basic FastAPI application (`main.py`) and `requirements.txt` are set up in `backend/`.
  - Output: `backend/main.py`, `backend/requirements.txt`.
- [ ] T005 Create `backend/.env.template` with placeholders for `QDRANT_URL`, `QDRANT_API_KEY`, `OPENAI_API_KEY`
  - Acceptance: `.env.template` file exists in `backend/` with specified placeholders.
  - Output: `backend/.env.template`.
- [ ] T006 Install `uvicorn` and `python-dotenv` in `backend/`
  - Acceptance: `uvicorn` and `python-dotenv` are listed in `backend/requirements.txt`.
  - Output: `backend/requirements.txt` updated.
- [ ] T007 Create initial content ingestion script placeholder in `scripts/ingest_content.py`
  - Acceptance: An empty `ingest_content.py` file exists in `scripts/`.
  - Output: `scripts/ingest_content.py`.

---

## Phase 2: Module Content (Modules 1–4) [US1]
**User Story Goal**: A student or instructor needs to access the comprehensive AI-generated Docusaurus textbook to learn about the Physical AI & Humanoid Robotics program.
**Independent Test**: Navigate through the deployed Docusaurus site and verify that all specified content sections (Intro, modules, weekly breakdown, hardware, assessments, glossary, summary) are present and readable.
**Checkpoint**: All textbook content markdown files are generated and accessible within the Docusaurus development environment.

### Content Generation Tasks
- [ ] T008 [US1] Generate introduction content for Docusaurus textbook in `docs/docs/intro.md`
  - Dependencies: T000
  - Acceptance: `docs/docs/intro.md` contains a relevant introduction based on course details.
  - Output: `docs/docs/intro.md`.
- [ ] T009 [P] [US1] Generate Module 1 content in `docs/docs/module1.md`
  - Dependencies: T000
  - Acceptance: `docs/docs/module1.md` contains content for Module 1.
  - Output: `docs/docs/module1.md`.
- [ ] T010 [P] [US1] Generate Module 2 content in `docs/docs/module2.md`
  - Dependencies: T000
  - Acceptance: `docs/docs/module2.md` contains content for Module 2.
  - Output: `docs/docs/module2.md`.
- [ ] T011 [P] [US1] Generate Module 3 content in `docs/docs/module3.md`
  - Dependencies: T000
  - Acceptance: `docs/docs/module3.md` contains content for Module 3.
  - Output: `docs/docs/module3.md`.
- [ ] T012 [P] [US1] Generate Module 4 content in `docs/docs/module4.md`
  - Dependencies: T000
  - Acceptance: `docs/docs/module4.md` contains content for Module 4.
  - Output: `docs/docs/module4.md`.
- [ ] T013 [P] [US1] Generate Weekly Breakdown content in `docs/docs/weekly-breakdown.md`
  - Dependencies: T000
  - Acceptance: `docs/docs/weekly-breakdown.md` contains weekly breakdown information.
  - Output: `docs/docs/weekly-breakdown.md`.
- [ ] T014 [P] [US1] Generate Hardware Requirements content in `docs/docs/hardware-requirements.md`
  - Dependencies: T000
  - Acceptance: `docs/docs/hardware-requirements.md` contains hardware requirements.
  - Output: `docs/docs/hardware-requirements.md`.
- [ ] T015 [P] [US1] Generate Assessments content in `docs/docs/assessments.md`
  - Dependencies: T000
  - Acceptance: `docs/docs/assessments.md` contains assessment details.
  - Output: `docs/docs/assessments.md`.
- [ ] T016 [P] [US1] Generate Glossary content in `docs/docs/glossary.md`
  - Dependencies: T000
  - Acceptance: `docs/docs/glossary.md` contains glossary terms and definitions.
  - Output: `docs/docs/glossary.md`.
- [ ] T017 [P] [US1] Generate Course Summary content in `docs/docs/course-summary.md`
  - Dependencies: T000
  - Acceptance: `docs/docs/course-summary.md` contains a course summary.
  - Output: `docs/docs/course-summary.md`.
- [ ] T018 [US1] Update Docusaurus sidebar configuration for new content in `docs/sidebars.js`
  - Dependencies: T002, T008-T017
  - Acceptance: `docs/sidebars.js` is updated to include all generated markdown files.
  - Output: Updated `docs/sidebars.js`.

---

## Phase 3: RAG Chatbot Integration [US2]
**User Story Goal**: A student needs to ask questions about the textbook content and receive relevant, accurate answers through an integrated chatbot.
**Independent Test**: Interact with the chatbot widget on the deployed Docusaurus site, asking questions related to the textbook, and verifying the accuracy and relevance of the responses.
**Checkpoint**: The RAG chatbot API is functional, integrated with Qdrant, and the chat widget is present in Docusaurus.

### Backend Implementation Tasks
- [ ] T019 [US2] Create `backend/src/models/rag_models.py` for `ChatMessageRequest`, `AskSelectedRequest`, `ChatbotResponse`
  - Dependencies: T004
  - Acceptance: `rag_models.py` contains Pydantic models matching `chatbot-api.yaml` schemas.
  - Output: `backend/src/models/rag_models.py`.
- [ ] T020 [US2] Implement Qdrant client initialization and connection in `backend/src/services/qdrant_service.py`
  - Dependencies: T005, T006
  - Acceptance: `qdrant_service.py` establishes a connection to Qdrant Cloud using environment variables.
  - Output: `backend/src/services/qdrant_service.py`.
- [ ] T021 [US2] Implement embedding generation service using OpenAI API in `backend/src/services/embedding_service.py`
  - Dependencies: T005, T006
  - Acceptance: `embedding_service.py` contains a function to generate embeddings for text using OpenAI.
  - Output: `backend/src/services/embedding_service.py`.
- [ ] T022a [US2] Implement Qdrant content retrieval function in `backend/src/services/rag_service.py`
  - Dependencies: T020, T021
  - Acceptance: Function queries Qdrant and returns raw relevant content.
  - Output: `backend/src/services/rag_service.py` (updated).
- [ ] T022b [US2] Implement RAG content synthesis/response generation in `backend/src/services/rag_service.py`
  - Dependencies: T022a, T044
  - Acceptance: Function takes retrieved content and user query, generates a coherent `ChatbotResponse`.
  - Output: `backend/src/services/rag_service.py` (updated).
- [ ] T023 [US2] Create FastAPI endpoint `/chat` in `backend/src/api/chatbot.py`
  - Dependencies: T019, T022b
  - Acceptance: `/chat` endpoint accepts `ChatMessageRequest` and returns `ChatbotResponse` using RAG service.
  - Output: `backend/src/api/chatbot.py`.
- [ ] T024 [US2] Create FastAPI endpoint `/ask-selected` in `backend/src/api/chatbot.py`
  - Dependencies: T019, T022b
  - Acceptance: `/ask-selected` endpoint accepts `AskSelectedRequest` and returns `ChatbotResponse` using RAG service.
  - Output: `backend/src/api/chatbot.py` (updated).
- [ ] T025 [US2] Integrate `chatbot.py` API routes into `backend/main.py`
  - Dependencies: T023, T024
  - Acceptance: FastAPI app in `backend/main.py` includes routes from `chatbot.py`.
  - Output: `backend/main.py` updated.
- [ ] T026 [P] [US2] Develop custom React component for chat widget in `docs/src/components/ChatWidget.js` (or .tsx)
  - Dependencies: T002
  - Acceptance: `ChatWidget.js` renders a basic chat interface.
  - Output: `docs/src/components/ChatWidget.js`.
- [ ] T027 [P] [US2] Integrate chat widget into Docusaurus layout/pages in `docs/src/theme/Layout.js` (or .tsx)
  - Dependencies: T026
  - Acceptance: Chat widget is visible on Docusaurus pages.
  - Output: `docs/src/theme/Layout.js` updated.
- [ ] T028a [US2] Implement text selection event listener in `docs/src/theme/Root.js`
  - Dependencies: T027
  - Acceptance: Selecting text in Docusaurus triggers a console log with the selected text.
  - Output: `docs/src/theme/Root.js` (updated).
- [ ] T028b [US2] Implement "Ask Chatbot" UI overlay and API call for selected text in `docs/src/theme/Root.js`
  - Dependencies: T028a, T024
  - Acceptance: A button/menu appears on text selection, sending selected text to `/ask-selected` endpoint and displaying response.
  - Output: `docs/src/theme/Root.js` (updated).

### Content Ingestion Tasks (Dependencies: T000, T007)
- [ ] T029 [US2] Implement Markdown parsing and chunking in `scripts/ingest_content.py`
  - Dependencies: T000
  - Acceptance: Script can read markdown files and split content into suitable chunks for embedding.
  - Output: `scripts/ingest_content.py` updated.
- [ ] T030 [US2] Implement embedding generation and Qdrant indexing in `scripts/ingest_content.py`
  - Dependencies: T020 (via service), T021 (via service), T029
  - Acceptance: Script successfully converts markdown chunks to embeddings and indexes them in Qdrant.
  - Output: `scripts/ingest_content.py` updated, Qdrant collection populated.
- [ ] T030a [US2] Execute content ingestion script to populate Qdrant in `scripts/ingest_content.py`
  - Dependencies: T030
  - Acceptance: Qdrant Cloud collection is populated with embedded textbook content.
  - Output: Qdrant collection populated.

### Testing Tasks (Dependencies: As per individual task)
- [ ] T031 [US2] Write unit tests for `backend/src/models/rag_models.py`
  - Dependencies: T019
  - Acceptance: All Pydantic models have basic validation tests passing.
  - Output: `backend/tests/unit/test_rag_models.py`.
- [ ] T032 [US2] Write unit/integration tests for `backend/src/services/qdrant_service.py`
  - Dependencies: T020
  - Acceptance: Qdrant client connection and basic operations are tested successfully.
  - Output: `backend/tests/integration/test_qdrant_service.py`.
- [ ] T033 [US2] Write unit tests for `backend/src/services/embedding_service.py`
  - Dependencies: T021
  - Acceptance: Embedding generation function is tested with mock OpenAI API.
  - Output: `backend/tests/unit/test_embedding_service.py`.
- [ ] T034 [US2] Write unit/integration tests for `backend/src/services/rag_service.py`
  - Dependencies: T022b, T044
  - Acceptance: RAG logic for retrieval and synthesis is tested with mock Qdrant and LLM responses.
  - Output: `backend/tests/unit/test_rag_service.py`.
- [ ] T035 [US2] Write API integration tests for `/chat` and `/ask-selected` endpoints in `backend/src/api/chatbot.py`
  - Dependencies: T023, T024, T030a
  - Acceptance: API endpoints respond correctly to valid and invalid requests.
  - Output: `backend/tests/integration/test_chatbot_api.py`.
- [ ] T036 [US2] Write React component tests for `docs/src/components/ChatWidget.js` using Jest/RTL
  - Dependencies: T026
  - Acceptance: Chat widget component renders correctly and handles user input.
  - Output: `docs/tests/unit/ChatWidget.test.js`.
- [ ] T037 [US2] Write E2E tests for chatbot interaction in `docs/tests/e2e/chat.test.js` using Cypress/Playwright
  - Dependencies: T028b, T025, T030a
  - Acceptance: End-to-end user flow for chatting and ask-selected feature passes.
  - Output: `docs/tests/e2e/chat.test.js`.

### LLM Integration Task
- [ ] T044 [US2] Integrate LLM for response generation in `backend/src/services/rag_service.py`
  - Dependencies: T021, T022a
  - Acceptance: RAG service successfully uses an LLM to formulate coherent answers based on retrieved content.
  - Output: `backend/src/services/rag_service.py` (updated).

---

## Phase 4: Review & Finalization [US3, US4]
**User Story 3 Goal**: A hackathon judge or user needs to access the fully deployed Docusaurus textbook and RAG chatbot solution on GitHub Pages.
**User Story 4 Goal**: A user or developer wants to explore the optional bonus features.
**Independent Test (US3)**: Verify Docusaurus site and chatbot are accessible and functional via GitHub Pages URLs.
**Independent Test (US4)**: Verify functionality of implemented bonus features (e.g., Urdu translation) if enabled.
**Checkpoint**: Solution is deployed, accessible, and all core/bonus features are functional.

### Deployment & Verification Tasks
- [ ] T045 [US3] Create GitHub Actions workflow for Docusaurus deployment to GitHub Pages in `.github/workflows/docusaurus-deploy.yml`
  - Dependencies: T003
  - Acceptance: Workflow successfully builds and deploys Docusaurus to GitHub Pages.
  - Output: `.github/workflows/docusaurus-deploy.yml`.
- [ ] T046 [US3] Create GitHub Actions workflow for FastAPI backend deployment (e.g., to Google Cloud Run) in `.github/workflows/fastapi-deploy.yml`
  - Dependencies: T004
  - Acceptance: Workflow successfully builds and deploys FastAPI backend.
  - Output: `.github/workflows/fastapi-deploy.yml`.
- [ ] T047 [US3] Verify deployed Docusaurus site folder structure
  - Acceptance: Deployed site has an organized and logical folder structure matching plan.
  - Output: Manual verification.
- [ ] T048 [US3] Conduct end-to-end testing of Docusaurus frontend and RAG chatbot integration
  - Dependencies: T037, T043, T045, T046
  - Acceptance: All acceptance scenarios for US1, US2, US3 pass.
  - Output: Test report/results.

### Bonus Features (Optional) [US4]
- [ ] T049 [P] [US4] Implement basic Urdu translation feature for Docusaurus content in `docs/src/theme/DocItem/Content/index.js` (or similar component)
  - Dependencies: T002
  - Acceptance: A toggle allows switching content to a placeholder Urdu translation.
  - Output: `docs/src/theme/DocItem/Content/index.js` updated.
- [ ] T050 [P] [US4] Integrate a subagent placeholder into RAG chatbot logic in `backend/src/services/rag_service.py`
  - Dependencies: T022b
  - Acceptance: RAG service can invoke a dummy subagent for specific query types.
  - Output: `backend/src/services/rag_service.py` updated.

---

## Task Dependencies & Parallel Opportunities

**Dependency Graph (High-Level User Story Order)**:
Phase 1 (Setup) -> Phase 2 (US1: Textbook Content) -> Phase 3 (US2: Chatbot Integration) -> Phase 4 (US3, US4: Deployment & Review)

**Parallel Execution Examples (within phases)**:
*   **Phase 1**: T001 (Base directories), T002 (Docusaurus init), T004 (FastAPI init), and T000 (Place data) can run in parallel. T005, T006, T007 can run after T004. T003 can run after T002.
*   **Phase 2 (US1)**: Tasks T008 through T017 (individual content generation) can be executed in parallel once T000, T002, T003 are complete.
*   **Phase 3 (US2)**: T020 (Qdrant client) and T021 (embedding service) can be developed in parallel after T005, T006. T019 can run after T004. T026 (ChatWidget component) can run in parallel with backend development after T002. Test tasks (T031-T037) can run in parallel with their respective implementation tasks once dependencies are met *after T030a completes*. T044 can run after T021, T022a. T022a, T022b can run after T020, T021. T023, T024 can run after T019, T022b. T025 runs after T023, T024. T027 runs after T026. T028a runs after T027. T028b runs after T028a, T024.
*   **Phase 4 (US4 - Bonus)**: T049 (Urdu translation) can be developed in parallel after T002. T050 (Subagent placeholder) can be developed in parallel after T022b.

## Summary of Tasks

*   **Total Tasks**: 46
*   **Tasks per User Story**:
    *   Phase 1 (Setup & Architecture): 8 tasks
    *   Phase 2 (US1: Module Content): 11 tasks
    *   Phase 3 (US2: RAG Chatbot Integration): 21 tasks (increased by 1)
    *   Phase 4 (US3, US4: Review & Finalization): 6 tasks
*   **Parallel Opportunities**: Identified multiple tasks that can run in parallel within and across phases.
*   **Independent Test Criteria**: Each user story has a clear, independent test criterion defined at the start of its phase.
*   **Suggested MVP Scope**: User Story 1 (AI-generated Docusaurus textbook) and User Story 3 (Deployment to GitHub Pages for Docusaurus) could form an initial MVP to demonstrate content delivery and accessibility. User Story 2 (RAG Chatbot Integration) would be the next critical addition.
