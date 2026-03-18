# ContextFlow Engine Architecture

ContextFlow operates strictly as a Context Engine (messages \u2192 messages).

## Architectural Boundaries Let's Be Clear
ContextFlow **is not** a router, nor is it an agent framework, nor does it provide vector databases, planner orchestrations, tool systems, or graph execution loops. 
Those capabilities belong to the downstream system (LangChain, LangGraph, CrewAI). ContextFlow is purely focused on the deterministic routing and scaling of your LLM Context Windows.

## The Context Item Contract
Every transformation must yield `List[ContextItem]`. We operate strictly away from unchecked dictionaries in order to govern priorities and exact token slices cleanly.

## API Rules
- All `run` methods default to asynchronous natively.
- Only exact invariants are mapped safely (e.g., `pipeline.run(trace=True)` guarantees exact engine traceability).
