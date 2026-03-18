# Cache Contract

The NativeCache governs cryptographic hashing to bypass slow transformation node executions iteratively.

## Immutable Cache Key Rules
To prevent old cache values from breaking new engine representations or parameters changing, ContextFlow natively bakes invariants into the cache keys.
The exact cache key sequence relies on combining:

```python
hash(
    content + 
    ENGINE_VERSION + 
    CACHE_SCHEMA_VERSION + 
    compressor_name + 
    mode_name + 
    params
)
```

Direct modifications bypassing this hierarchy are forbidden to ensure stable scaling.
