# The Context Pipeline

The `pipeline.py` orchestrator is the execution heartbeat of ContextFlow.

## Run Loop Execution (`ContextPipeline.run()`)

When a developer triggers pipeline execution for a specific objective, the following sequential operations occur:

1. **Source Aggregation:** The pipeline iterates over all injected `ContextSource` instances and triggers `.load()`. This translates arbitrary logs and memory strings into uniform dictionary structures.
2. **Goal Injection:** The developer's ultimate query (`goal`) is actively appended to the end of the array.
3. **Filtering (`Mode.select()`):** The array is sliced down. For example, `MinimalMode` cuts the history to just the last 5 messages.
4. **Deterministic Trimming (`Compressor.compress()`):** The text payload inside each remaining dictionary is scraped clean of visual whitespace, conversational LLM filler ("please", "here is your code"), and duplicate console logs.
5. *(Future) Truncation (`TokenBudget.fit()`):* A tokenizer counts the total bits in the array. If it exceeds backend limits, it forces a targeted deletion of the oldest string contexts.
6. **Execution (`Provider.chat()`):** The minimized JSON array payload is sent asynchronously to the LLM backend.

## Why Sequential Iteration?
We actively avoid asynchronous, parallelized summarization at the compression layer because waiting on secondary LLM API calls introduces massive latency and breaks deterministic safety constraints. Sequence guarantees speed. 
