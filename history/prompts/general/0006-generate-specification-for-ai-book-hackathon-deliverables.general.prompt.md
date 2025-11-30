---
id: 0006
title: Generate Specification for AI-book Hackathon Deliverables
stage: spec
date: 2025-11-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-book
branch: docs/update-constitution
user: unknown
command: "/sp.specify ai-book"
labels: ["specification","ai-book","hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- specs/ai-book/spec.md
tests:
- null
---

## Prompt

/spec.specify ai-book

Use the complete course details and hardware requirements of the Physical AI & Humanoid Robotics program as the input domain.

Follow the Constitution already created in this project.

Write a complete, testable Specification for the following deliverables required by the Hackathon:

1. AI-generated Docusaurus textbook
   - Intro + all 4 modules
   - Weekly Breakdown
   - Hardware Requirements
   - Assessments
   - Glossary
   - Course Summary

2. Integrated RAG chatbot
   - FastAPI backend
   - Qdrant Cloud indexing
   - Ask-selected feature
   - Chat widget for Docusaurus

3. Deployment
   - GitHub Pages
   - Folder structure

4. Bonus (optional)
   - Subagents
   - Skills
   - Urdu translation feature

Specification must include:
- Intent
- Inputs
- Constraints
- SMART success criteria
- Non-goals
- Scenarios
- Edge cases
- Acceptance tests

Make sure the spec is Constitution-aligned and does NOT include implementation details.

## Response snapshot

Creating specification for 'ai-book' feature.

## Outcome

- ✅ Impact: PHR created for spec generation request.
- 🧪 Tests: null
- 📁 Files: specs/ai-book/spec.md
- 🔁 Next prompts: Execute /sp.specify ai-book command.
- 🧠 Reflection: PHR successfully created with all relevant details.

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
