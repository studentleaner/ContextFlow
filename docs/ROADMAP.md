# ContextFlow Roadmap & Next Steps

This roadmap outlines the evolution of the ContextFlow framework, prioritizing the major functional blocks required to make this production-ready for Agent developers.

---

## 🟢 Phase 1: Core Framework Polish (**Completed**)
The objective of Phase 1 was making the theoretical stub files functional.
- [x] **Token Budgeting Overhaul:** Integrated `tiktoken` array slicing.
- [x] **Pipeline Execution Updates:** ContextPipeline strictly maps budgets and telemetry traces.
- [x] **First Real Provider:** `OpenAIProvider` adapting natively to OpenAI endpoints.

---

## 🟡 Phase 2: Agent Tooling & Robustness (**Current Focus**)
The objective of Phase 2 is to ensure ContextFlow can sit reliably underneath popular loops like LangGraph, ReAct, and CrewAI without breaking rigid JSON outputs.

- [x] **Config Module Implementation:** Pydantic-backed environment consumer for configs.
- [x] **Extensible Data Sources (`ContextSource`):** `FileSource` loads `.md` documents natively into contexts.
- [x] **Semantic / Advanced Compression Algorithms:** AST Regex safety mechanisms avoiding the destruction of nested Agent JSON schemas.
- [ ] **Unit Testing & Benchmarks:** Expanded unit testing suite ensuring Semantic logic works correctly.

---

## 🔵 Advanced Evolution (TDD / Future)

### 1. Test-Driven Development (TDD) Suites
- TDD is uniquely suited for ContextFlow because deterministic compression and modes have clear, mathematical input/output structures (unlike stochastic LLMs). 
- We will build unit test suites verifying token counts and exact string mutations.

### 2. Metric Visibility (`metrics.py`)
- *Are there admin pages?* No. ContextFlow is a headless library. 
- *How is it measurable?* Everything should be measurable via STDOUT logs, structured JSON logging, or emitted OpenTelemetry traces. Developers can plug these logs into Datadog, Grafana, or LangSmith.

### 3. Config Overhaul (`config.py`)
- Move towards Pydantic `BaseSettings` for rigid, typed configuration of max context lengths, active modes, and provider keys.
