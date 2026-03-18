# ContextFlow Roadmap & Next Steps

This roadmap outlines the evolution of the ContextFlow framework, prioritizing the major functional blocks required to make this production-ready for Agent developers.

---

## 🔴 Immediate Priorities

### 1. Granular Token Budgeting (`budget.py`)
Currently, `TokenBudget` truncates by removing whole messages from the array (`messages[-5:]`). This is a naive implementation.
- **Goal:** Integrate a tokenizer (e.g., `tiktoken` for OpenAI standard) that counts exact token usage. If the array exceeds the budget limit, it should intelligently truncate the strings *inside* the oldest messages, preserving the most critical new information and the system instructions intact.

### 2. Provider Implementations (`provider.py`)
- **Goal:** Expand past the `MockProvider`. Create a base `OpenAIProvider` wrapping the standard async OpenAI python package, and an Anthropic/gemini equivalent, ensuring parameters (temperature, max_tokens) are passed through the pipeline appropriately.

### 3. Pipeline Execution Integration (`pipeline.py`)
- **Goal:** The core `ContextPipeline.run()` method must actively orchestrate the `TokenBudget` execution and capture operational telemetry via `MetricsCollector` (tokens in, tokens out, time saved).

---

## 🟡 Core Architecture Improvements 

### 1. JSON & Structured Data Preservation
As agents heavily utilize Tool Calling and JSON parsing, deterministic text compression (trimming spaces, deduplicating brackets) carries the risk of breaking valid JSON schemas.
- **Goal:** The `StandardCompressor` must be upgraded to detect JSON blobs and explicit Code Blocks (via regex or AST) and safely bypass aggressive whitespace/duplication compression on those specific blocks to prevent agent syntax failures.

### 2. Prefix Caching Awareness
Both Anthropic and OpenAI support prompt caching, drastically reducing costs if the prefix of a prompt remains perfectly static across sequential calls.
- **Goal:** Enforce a strict ordering in the pipeline where static assets (System Prompts, loaded core documents) are universally placed at the *start* of the message array, and volatile data (volatile memory, new observations) are strictly appended at the end.

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
