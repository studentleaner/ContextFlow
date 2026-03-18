# ContextFlow: Technical Usage & Extension Guide

ContextFlow is a generic middleware designed to forcefully optimize token usage *before* data reaches your LLM. It is built entirely on SOLID principles, meaning every single step of the pipeline can be swapped or extended.

## 1. How to Use (Code Perspective)

### Basic Implementation
If you have raw data logs or chat history and just want to strip the noise out deterministically without relying on a slow summarization LLM:

```python
from contextflow import (
    ContextPipeline, MinimalMode, StandardCompressor, 
    TokenBudget, MockProvider, MetricsCollector
)

pipeline = ContextPipeline(
    sources=[], # We inject messages dynamically at the end
    mode=MinimalMode(), # Keeps only User and System Roles
    compressor=StandardCompressor(), # Trims whitespace, deduplicates, protects JSON
    budget=TokenBudget(max_tokens=2000), # Hard slice if it exceeds
    provider=MockProvider(), # (Optional) Sends directly to an LLM
    metrics=MetricsCollector()
)

# A massive, noisy context block
noisy_history = [
    {"role": "user", "content": "Analyze these logs: \n" + ("ERROR: RAM FULL\n" * 100) + "```json\n{ \"goal\": \"fix memory\" }\n```"}
]

# The pipeline instantly strips the 100 duplicate lines into 1 line natively,
# preserving the JSON string block perfectly.
compressed_state = pipeline.compressor.compress(noisy_history)
```

### LangGraph / Agentic Loop Integration
Agent loops (like LangGraph or CrewAI) generate massive state histories across cyclical nodes. ContextFlow sits natively between the Tool Execution node and the Reasoning LLM node as an interceptor.

```python
def node_context_middleware(state: AgentState):
    """LangGraph node that intercepts the state array to trim fat before LLM processing."""
    pipeline = ContextPipeline(
        sources=[], mode=MinimalMode(), compressor=StandardCompressor(),
        budget=TokenBudget(max_tokens=6000), metrics=MetricsCollector(), provider=MockProvider()
    )
    
    # Overwrite the state with the structurally safe compressed version
    state.messages = pipeline.compressor.compress(state.messages)
    return state
```

---

## 2. How to Extend the Architecture

ContextFlow operates on abstract base classes (`docs/INTERFACES.md`). To add custom logic for your specific company or data pipeline, simply inherit from the base classes and inject them into `ContextPipeline`.

### A. Extending the ContextSource (Custom Data Loaders)
Need to load memory from a VectorDB or an S3 bucket instead of a local file?

```python
from contextflow.interfaces import ContextSource

class S3DatabaseSource(ContextSource):
    def __init__(self, bucket_name):
        self.bucket = bucket_name
        
    def load(self):
        # Your custom retrieval logic
        data = fetch_from_s3(self.bucket)
        return [{"role": "system", "content": f"Database Document:\n{data}"}]

# Usage
pipeline = ContextPipeline(sources=[S3DatabaseSource("my-bucket")], ...)
```

### B. Extending the Compressor (Custom Stripping Logic)
Are your logs highly proprietary and you only want to compress lines that contain the word "TRACE"?

```python
from contextflow.interfaces import Compressor

class proprietary_log_compressor(Compressor):
    def compress(self, messages):
        output = []
        for m in messages:
            if m.get("role") == "user":
                # Filter out lines starting with TRACE
                clean_text = "\\n".join([line for line in m["content"].split("\\n") if not line.startswith("TRACE:")])
                output.append({"role": "user", "content": clean_text})
            else:
                output.append(m)
        return output
```

### C. Extending the ContextMode (Custom Message Filters)
Need a mode that drops all `assistant` messages older than 5 turns to save strictly on output history tokens?

```python
from contextflow.interfaces import ContextMode

class RecentMemoryMode(ContextMode):
    def select(self, messages):
        # Filter all messages, only keeping the 5 most recent
        return messages[-5:]
```

---

## 3. How to Use (Package Perspective)

If you are incorporating ContextFlow into a monorepo or a larger Python application without publishing it to PyPI:

1. Place the `contextflow/` directory alongside your core application.
2. Ensure you have `tiktoken` installed (`pip install tiktoken`).
3. You can now import it anywhere in your broader app:

```python
# Assuming your app structure is:
# /my_monorepo
#   /backend_api
#      main.py
#   /contextflow
#      __init__.py
#      pipeline.py

from contextflow import ContextPipeline
```

Because ContextFlow has minimal external dependencies, it operates flawlessly as an internal package layer decoupled from your framework orchestration.
