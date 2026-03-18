# Configuration System

ContextFlow abstracts orchestration setup away from script boilerplates natively using the `ContextConfig` object.

## Bootstrapping Pipelines
To dynamically load context pipelines natively with registered components, use:
```python
from contextflow.config import ContextConfig
from contextflow import ContextPipeline

config = ContextConfig(
    mode="semantic",
    compressor="distill",
    budget=6000,
    cache=True,
    provider="openai"
)

pipeline = ContextPipeline.from_config(config)
```
This is the recommended standard wrapper logic for robust downstream engine configuration.
