# Telemetry & Metrics Output

## Dashboard Philosophy
ContextFlow operates exclusively as a **headless middleware Python library**. There are no integrated UI dashboards or web admin pages included in this repository.

## The `MetricsCollector`
For agent runners to confidently use this library, measuring efficiency is mandatory. Through dependency injection, developers can provide a `MetricsCollector` (`metrics.py`) instance to track deterministic variables during the pipeline sequence.

### Target Trace Metrics
* **`tokens_before`:** Total baseline token count from raw sources.
* **`tokens_after`:** The final token count mapped directly to the provider.
* **`compression_ratio`:** Representing the literal percentage of fat trimmed (`tokens_after / tokens_before`).
* **`latency_ms`:** How long the `Mode + Compressor` sequential execution takes. (Goal: <50ms standard)
* **`cost_savings_estimate`:** A computed translation of tokens saved vs. the Provider's standard $/1M token pricing bracket.

### Integration
Because the collector emits a standard dictionary state, teams are encouraged to sink this telemetry into backend enterprise platforms:
* LangSmith / Datadog
* Prometheus / Grafana stacks
* ElasticSearch logs
