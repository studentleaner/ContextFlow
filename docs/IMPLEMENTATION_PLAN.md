# Phase 1: Immediate Priorities Implementation Plan

This plan addresses the three core development goals established in `ROADMAP.md` Phase 1.

## Proposed Changes

### 1. Granular Token Budgeting (`budget.py`)
- **Goal:** Use `tiktoken` to get exact encoding lengths. Truncate oldest messages or exact strings if array exceeds the `max_tokens` budget.

### 2. Concrete Provider (`provider.py`)
- **Goal:** Implement `OpenAIProvider` wrapping the official `openai` SDK, exposing the `.chat(messages)` interface. Keep `MockProvider` for testing.

### 3. Pipeline Integration (`pipeline.py`)
- **Goal:** 
  1. Inject `TokenBudget` and `MetricsCollector` into `ContextPipeline.__init__`.
  2. Implement an execution trace computing `tokens_before`, executing `mode` + `compressor` + `budget`, computing `tokens_after`, tracking `latency_ms`, logging to `metrics`, and finally calling `provider.chat(messages)`.

### 4. Dependencies
- Create `requirements.txt` to track `tiktoken` and `openai` library dependencies
