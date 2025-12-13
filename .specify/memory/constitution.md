<!--
Sync Impact Report:
Version change: None -> 1.0.0
List of modified principles: All new
Added sections: Technology Stack and Tools, Learning Outcomes and Objectives
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ updated
  - .specify/templates/spec-template.md: ✅ updated
  - .specify/templates/tasks-template.md: ✅ updated
  - .specify/templates/commands/*.md: ✅ updated
  - README.md: ⚠ pending (manual follow-up suggested)
  - docs/quickstart.md: ⚠ pending (manual follow-up suggested)
Follow-up TODOs: None
-->
# Hackathon I: Physical AI & Humanoid Robotics Book Project Constitution

## Core Principles

### I. AI/Spec-Driven Book Creation
The book project MUST be created and maintained using Claude Code and Spec-Kit Plus, adhering to AI/Spec-Driven Development methodologies. This ensures a structured, consistent, and automatable content generation process.

### II. Docusaurus & GitHub Pages Deployment
The unified book project MUST be built using Docusaurus and deployed to GitHub Pages for public accessibility, version control, and collaborative content management. This enables clear documentation of course material and easy updates.

### III. Integrated RAG Chatbot Development
An integrated Retrieval-Augmented Generation (RAG) chatbot MUST be developed and embedded within the published book. This chatbot MUST utilize OpenAI Agents/ChatKit SDKs, FastAPI, and Qdrant Cloud Free Tier, capable of answering questions about the book's content, including user-selected text. This provides an interactive learning experience for students.

### IV. Physical AI & Robotics Curriculum Focus
The book content MUST focus on Physical AI and Humanoid Robotics, covering ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action (VLA) for embodied intelligence and control in simulated and real-world environments. This ensures alignment with the course's core themes and learning objectives.

### V. Test-First Development (NON-NEGOTIABLE)
All code components, especially for the RAG chatbot and any custom development, MUST follow a Test-Driven Development (TDD) approach. Tests MUST be written and approved before implementation, ensuring a strict Red-Green-Refactor cycle. This guarantees code quality, reliability, and maintainability.

## Technology Stack and Tools

### Book Creation
- Claude Code: For AI/Spec-Driven Development and content generation.
- Spec-Kit Plus: For structured specification, planning, and task management.
- Docusaurus: Static site generator for book publishing.
- GitHub Pages: For deployment and hosting of the book.

### RAG Chatbot
- OpenAI Agents/ChatKit SDKs: For chatbot logic and conversational AI.
- FastAPI: For building robust API endpoints.
- Qdrant Cloud Free Tier: For vector database and similarity search in RAG.

### Robotics Simulation & Control
- ROS 2: Middleware for robot control and communication.
- Gazebo: For physics simulation and environment building.
- Unity: For high-fidelity rendering and human-robot interaction simulation.
- NVIDIA Isaac Sim: Photorealistic simulation and synthetic data generation.
- Isaac ROS: Hardware-accelerated VSLAM and navigation.
- Nav2: Path planning for bipedal humanoid movement.
- OpenAI Whisper: For voice-to-action capabilities.

## Learning Outcomes and Objectives

### Core Learning Outcomes
- Understand Physical AI principles and embodied intelligence.
- Master ROS 2 (Robot Operating System) for robotic control.
- Simulate robots with Gazebo and Unity.
- Develop with NVIDIA Isaac AI robot platform.
- Design humanoid robots for natural interactions.
- Integrate GPT models for conversational robotics.

## Governance

This constitution supersedes all other project practices. Amendments require thorough documentation, approval by project leads, and a clear migration plan. All Pull Requests (PRs) and code reviews MUST verify compliance with these principles. Justification for any increased complexity is required, ensuring that simplicity and adherence to core principles are maintained.

**Version**: 1.0.0 | **Ratified**: 2025-11-28 | **Last Amended**: 2025-11-28
