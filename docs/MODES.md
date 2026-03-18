# Pipeline Modes

A `ContextMode` identifies *which* messages are legally allowed to enter the expensive compression phase. Modifying modes allows developers to radically change Agent behavior without touching the underlying LangGraph logic.

## Abstract Interface
```python
class ContextMode(ABC):
    @abstractmethod
    def select(self, messages: List[ContextItem]) -> List[ContextItem]:
        pass
```

## Core Modes
1. **`FullMode`:** Complete passthrough. Sends 100% of the messages to the LLM. Appropriate for generalized chatting.
2. **`MinimalMode`:** Strips out `assistant` reasoning and `tool` output histories. Ideal for long-running Agent cyclomatic loops that typically crash from OOM if reasoning isn't scrubbed between state node resets.

## Extension Ideas (Relevance Scoring)
Production pipelines should inherit `ContextMode` to create a `RelevanceMode`, running VectorDB cosine-similarity checks inside the `select` method to pull `k=5` strings based on the currently defined `Goal`.
