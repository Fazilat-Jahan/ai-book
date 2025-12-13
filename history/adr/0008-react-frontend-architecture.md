---
adr_id: 0008
title: React Frontend Architecture
status: Proposed
date: 2025-12-06
---

## Context

The RAG chatbot requires an interactive and responsive frontend chat widget to be embedded within the AI Book website. This widget needs to communicate with the FastAPI backend, display real-time feedback (typing indicators, streaming output), and support the "ask-selected" feature. React has been chosen as the JavaScript library for its component-based architecture and widespread adoption in modern web development.

## Decision

The chosen frontend architecture will be a React-based chat widget. It will be responsible for sending messages to the FastAPI backend, injecting selected text into requests, handling loading states and streaming output, and configuring the API base URL for production.

**Components of this decision:**
- **Frontend Framework**: React.
- **Backend Communication**: Fetch API or a library like Axios for `POST /ask`.
- **Selected Text Injection**: JavaScript DOM manipulation to capture selected text and include it in the request payload.
- **Loading State**: UI elements (e.g., spinner) to indicate when a response is pending.
- **Streaming Handling**: Processing streamed responses from FastAPI to update the UI incrementally.
- **API Base URL Configuration**: Environment variables or build-time configuration for different deployment environments.

## Consequences

### Positive:
- **Interactive User Experience**: React's component model facilitates building a highly interactive and dynamic chat interface with real-time updates (typing indicators, streaming).
- **Modularity and Reusability**: Components for chat input, message display, and loading states can be developed independently and reused.
- **Strong Ecosystem**: Access to a vast ecosystem of React libraries, tools, and community support for development and debugging.
- **Performance (Client-side)**: Efficient UI updates through React's virtual DOM, providing a smooth user experience.

### Negative:
- **Bundle Size**: React applications can have a larger initial bundle size compared to simpler JavaScript solutions, potentially impacting initial load times if not optimized.
- **Learning Curve**: For developers unfamiliar with React, there might be a learning curve for its concepts (hooks, state management, lifecycle).
- **Build Complexity**: Requires a build toolchain (e.g., Webpack, Vite) for development and production builds, which adds a layer of configuration.

## Alternatives Considered

### 1. Vanilla JavaScript/HTML/CSS
- **Description**: Implementing the chat widget purely with native browser technologies without a frontend framework.
- **Pros**:
    - Smallest possible bundle size and fastest initial load times.
    - No framework dependencies, offering maximum control.
- **Cons**:
    - Significantly higher development effort for complex interactive features, state management, and UI updates.
    - Prone to spaghetti code and difficult to maintain as the widget grows.
    - Lack of componentization makes reusability challenging.

### 2. Vue.js/Angular
- **Description**: Using other popular frontend frameworks like Vue.js or Angular.
- **Pros**:
    - **Vue.js**: Generally considered easier to learn than React, with good performance.
    - **Angular**: Comprehensive framework with strong opinions, good for large enterprise applications.
- **Cons**:
    - Choosing a different framework introduces a new learning curve and ecosystem, potentially fragmenting frontend expertise if other parts of the project use React.
    - While capable, React is a very strong choice for embedded widgets due to its flexibility and component model.

## References

- [Plan: Architectural Plan: AI Book RAG Chatbot](specs/1-ai-book-rag-chatbot/plan.md)
- [ADR-0007: FastAPI Backend Architecture](history/adr/0007-fastapi-backend-architecture.md)
