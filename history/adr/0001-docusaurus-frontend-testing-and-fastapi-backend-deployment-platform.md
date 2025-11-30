# ADR-0001: Docusaurus Frontend Testing and FastAPI Backend Deployment Platform

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Proposed
- **Date:** 2025-11-29
- **Feature:** ai-book
- **Context:** The AI-Book Hackathon project requires an AI-generated Docusaurus textbook with an integrated RAG chatbot (FastAPI backend with Qdrant Cloud indexing) and deployment to GitHub Pages. Key architectural decisions are needed for frontend testing strategies to ensure quality and for the backend deployment platform to ensure cost-effectiveness, scalability, and performance.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- **Docusaurus Frontend Testing**: A combined strategy using Jest for unit testing, React Testing Library (RTL) for component/integration testing, and Cypress or Playwright for end-to-end (E2E) testing.
- **FastAPI Backend Deployment Platform**: Google Cloud Run is chosen as the primary recommended platform, with AWS Lambda + API Gateway as a strong alternative.

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

- **Robust Frontend Quality**: Jest, RTL, and Cypress/Playwright provide comprehensive testing coverage, leading to a high-quality, stable Docusaurus frontend and integrated chat widget.
- **Cost-Effective and Scalable Backend**: Google Cloud Run (and AWS Lambda) offer serverless, pay-as-you-go models, ensuring optimal cost-effectiveness and automatic scaling to handle varying workloads for the FastAPI backend.
- **Simplified Deployment for Backend**: Cloud Run's native support for containerized applications and FastAPI simplifies deployment and management compared to traditional VM setups.
- **Developer Focus**: Serverless deployments allow developers to concentrate on business logic rather than infrastructure management.
- **Optimized Qdrant Integration**: Both chosen platforms support efficient integration with Qdrant Cloud, especially with singleton client instances, improving performance and reducing resource consumption.

<!-- Example: Integrated tooling, excellent DX, fast deploys, strong TypeScript support -->

### Negative

- **Learning Curve**: Adopting multiple testing frameworks (Jest, RTL, Cypress/Playwright) might introduce an initial learning curve for developers unfamiliar with them.
- **Platform Specifics**: While serverless, there are still platform-specific configurations and potential vendor lock-in aspects to consider for Google Cloud Run (or AWS).
- **Complexity of Integration**: Integrating multiple testing frameworks and two separate deployment environments (GitHub Pages for frontend, Cloud Run for backend) adds some architectural complexity.

<!-- Example: Vendor lock-in to Vercel, framework coupling, learning curve -->

## Alternatives Considered

- **Docusaurus Frontend Testing Alternatives**:
    - **Enzyme**: Rejected in favor of RTL due to RTL's user-centric approach and better alignment with modern React practices.
    - **Manual testing only**: Rejected due to lack of scalability, repeatability, and increased risk of regressions.
- **FastAPI Backend Deployment Platform Alternatives**:
    - **Azure App Service**: Rejected as it is not strictly a serverless *function* offering and might require more explicit optimization for Qdrant client usage.
    - **Traditional VM/Container deployments (e.g., EC2, GCE, Kubernetes)**: Rejected due to higher operational overhead, less inherent cost-effectiveness for fluctuating workloads, and increased management complexity not ideal for a hackathon project.

<!-- Group alternatives by cluster:
     Alternative Stack A: Remix + styled-components + Cloudflare
     Alternative Stack B: Vite + vanilla CSS + AWS Amplify
     Why rejected: Less integrated, more setup complexity
-->

## References

- Feature Spec: `specs/ai-book/spec.md`
- Implementation Plan: `specs/ai-book/plan.md`
- Research Findings: `specs/ai-book/research.md`
- Related ADRs: N/A
- Evaluator Evidence: `history/prompts/ai-book/0007-generate-ai-book-architectural-plan.plan.prompt.md`
