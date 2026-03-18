# Changelog

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
