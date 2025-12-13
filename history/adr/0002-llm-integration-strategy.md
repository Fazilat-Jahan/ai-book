---
adr_id: 0002
title: LLM Integration Strategy
status: Proposed
date: 2025-12-06
---

## Context

The RAG chatbot requires integration with a Large Language Model (LLM) for generating responses. The project specification mandates using Gemini LLM through an OpenAI Agents SDK/ChatKit-compatible SDK endpoint for cost-effective AI integration. This decision impacts how the backend communicates with the LLM service and influences the overall architecture of the RAG pipeline.

## Decision

The chosen strategy is to use Gemini LLM accessed through an OpenAI Agents SDK/ChatKit-compatible SDK endpoint.

**Components of this decision:**
- **LLM Provider**: Gemini LLM
- **Integration Method**: OpenAI Agents SDK/ChatKit-compatible SDK endpoint

## Consequences

### Positive:
- **Simplified Integration**: Leverages existing OpenAI Agents SDK/ChatKit integration patterns, potentially simplifying setup and reducing development time due to familiarity with a common interface.
- **Cost-Effectiveness**: Aligns with the project requirement for cost-effective AI integration by utilizing Gemini.
- **Robust Generation**: Gemini LLM provides strong natural language understanding and generation capabilities suitable for RAG tasks.
- **Ecosystem Compatibility**: Ensures compatibility with an established SDK ecosystem, potentially allowing for easier future upgrades or changes.

### Negative:
- **SDK Dependency**: Reliance on a specific SDK might introduce a vendor lock-in risk or limit flexibility if the SDK's capabilities diverge significantly from direct API access.
- **Abstraction Layer**: The SDK adds an abstraction layer, which might obscure underlying LLM behaviors or introduce minor performance overhead compared to direct API calls.
- **Configuration Complexity**: May require careful configuration to ensure the OpenAI Agents SDK/ChatKit-compatible endpoint correctly routes to Gemini, adding a layer of setup complexity.

## Alternatives Considered

### 1. Direct Gemini API Integration
- **Description**: Directly calling the Gemini API without an intermediary SDK like OpenAI Agents SDK/ChatKit.
- **Pros**:
    - Full control over API calls and parameters.
    - Potentially minor performance gains by removing an abstraction layer.
    - No dependency on a third-party SDK for LLM interaction.
- **Cons**:
    - More complex setup and boilerplate code required for handling requests, responses, and error management.
    - May not align with the "compatible SDK endpoint" requirement as easily as the chosen approach.
    - Increased development effort for features like streaming or advanced prompt engineering that the SDK might simplify.

### 2. Other LLM Providers (e.g., Anthropic Claude, Azure OpenAI)
- **Description**: Utilizing a different LLM provider that might also offer compatible SDKs.
- **Pros**:
    - Diversification of LLM options.
    - Potential for different performance or cost profiles.
- **Cons**:
    - Not explicitly specified in the project requirements, which names Gemini.
    - Would require a different set of SDKs or integration patterns, potentially increasing development complexity or diverging from the specified path.

## References

- [Plan: Architectural Plan: AI Book RAG Chatbot](specs/1-ai-book-rag-chatbot/plan.md)
