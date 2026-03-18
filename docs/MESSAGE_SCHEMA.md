# Data Contract: Message Schema

ContextFlow uses explicit Pydantic `ContextItem` schemas instead of arbitrary dictionaries (`{"role": "user"}`). This enables strong typing, priority ranking, and exact token counting.

## The `ContextItem` Schema
```python
class ContextItem(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    priority: int = 0
    tokens: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

## Why Not Raw Dictionaries?
1. **Safety:** Passing typo'd dictionaries (`{"rola": "user"}`) silently fails in production. Pydantic guarantees boundary integrity before the `ContextPipeline` even begins compressing the array.
2. **Algorithmic Importance (`priority`):** Raw OpenAI dictionaries have no concept of "importance." By injecting a `priority` integer, our TokenBudget can mathematically drop `priority=0` "noise" items first when the array overflows Context Window limits.
3. **Internal Telemetry:** Storing exact `tiktoken` byte-pair lengths natively inside the array objects prevents duplicate loops across pipeline algorithms.

## Serialization
When the execution reaches the final `Provider.arun()`, the pipeline seamlessly strips the Pydantic metadata and converts the array natively to the OpenAI dictionary specification using `item.to_llm_dict()`.
