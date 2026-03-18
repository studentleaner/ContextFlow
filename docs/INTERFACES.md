# Core Interfaces

Because ContextFlow adheres strictly to Open/Closed SOLID design principles, behavior is overridden by extending the Python interfaces in `interfaces.py`.

## `ContextSource`
```python
class ContextSource:
    def load(self) -> list[dict]:
        """Must return a uniform array of dictionaries with 'role' and 'content' keys."""
        raise NotImplementedError
```

## `ContextMode`
```python
class ContextMode:
    def select(self, messages: list[dict]) -> list[dict]:
        """Accepts a full history and returns the structurally relevant subset."""
        raise NotImplementedError
```

## `Compressor` 
```python
class Compressor:
    def compress(self, messages: list[dict]) -> list[dict]:
        """Executes text-cleaning algorithms on the 'content' string attributes."""
        raise NotImplementedError
```

## `Provider`
```python
class Provider:
    def chat(self, messages: list[dict]) -> str:
        """The terminal API adapter sending the array over the network."""
        raise NotImplementedError
```
