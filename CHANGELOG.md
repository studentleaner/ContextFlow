# Changelog

## v0.6.0

ContextFlow natively introduces the Intelligence Layer to filter and compress context intelligently utilizing Semantic and Distillation logic.

**Added:**
- `SemanticMode` capable of structurally dropping uncorrelated chat history via goal-similarity.
- `DistillationCompressor` replacing rigid deterministic heuristics with natively awaited asynchronous LLM chunk summarization.
- `acompress()` hook dynamically inserted into the base `Compressor` interface explicitly enabling intelligent LLM pipeline compression securely.

**Refactored:**
- `ContextPipeline.arun()` and `NativeCache.aget_or_set()` natively await and cascade async implementations cleanly.
- `Provider` interface corrected to strictly parse flat message arrays natively, standardizing Prompt injection.

## v0.5.0

ContextFlow natively introduces Plugin Registries enabling infinite extensibility without modifying core architecture.

**Added:**
- `PluginRegistry` foundational pattern inside `core/registry.py`.
- `ModeRegistry`, `CompressorRegistry`, `ProviderRegistry`, `SourceRegistry`, and `ScorerRegistry` natively exporting decorators for dynamic logic insertion.
- Exhaustive test suite (`test_registry.py`) covering type-safe constraints and instantiation mechanisms natively.

**Refactored:**
- All built-in classes (`MinimalMode`, `OpenAIProvider`, `NativeCache` etc) register implicitly on import seamlessly.


## v0.4.0

ContextFlow natively transitions from a stateless pipeline array into a stateful Context Engine.

**Added:**
- `ContextSession` architectural wrapper capturing multi-turn integrations.
- `NativeCache` generating cryptographic hashes to safely bypass redundant execution.
- `ContextRanker` enabling mathematical arrays (via `TimeDecayScorer`).
- Native debug tracing telemetry (`pipeline = ContextPipeline(debug=True)`).
- Synthetic array benchmarks (`benchmarks/benchmark.py`).
- Standalone execution loops (`examples/agent_session.py`).

**Refactored:**
- Migrated flat Python module architecture into extensible nested sub-packages (`mode/`, `compression/`, `provider/`).
- Safely isolated shared schemas and interfaces inside a protected `core/` package.

**Improved:**
- Async Provider execution pathways ensuring asynchronous graph compatibility.
- `TokenBudget` enforcing structural retention limits using Priority-slicing metrics over standard deletion.
- Deterministic Compression safety guarding LangGraph JSON nodes from scraper mutations exactly.
