# ContextFlow 🌊  
**Better Context > Bigger Models**

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-green)
![Architecture](https://img.shields.io/badge/design-SOLID-orange)
![LLM](https://img.shields.io/badge/LLM-context--engineering-purple)

ContextFlow is an experimental **Context Engine** for LLM systems (Pre-1.0).

It provides a stateful orchestration layer to **cache, rank, compress, and budget context** before injecting it into Large Language Models (LLMs).

Designed for:
- Agents (ReAct, LangGraph, CrewAI)
- RAG systems
- Coding assistants
- Long-running LLM loops

---

## 🚀 Why a Context Engine?

Modern LLM applications often fail not because of the model, but because of **bad context**. 
Massive contexts result in the "Lost in the Middle" phenomenon where models ignore relevant details.

**The Solution:** ContextFlow sits between your data sources and your orchestration layer. 
It deterministically removes noise, ranks memory by semantic relevance, cryptographically caches static files, and enforces hard `tiktoken` limits so you use fewer tokens, lower latency (TTFT), and reduce hallucination loops safely.

---

## 📚 Documentation

For a deep dive into how ContextFlow works and how to extend its architecture, explore the documentation:

1. [**Developer Usage & Extension Guide (`docs/USAGE.md`)**](docs/USAGE.md) - How to write code using ContextFlow, embed it in Agent loops, and write custom compression layers.
2. [Architectural Analysis (`docs/ANALYSIS.md`)](docs/ANALYSIS.md) - Why Context Engineering matters and our concept evaluation.
3. [Project Architecture (`docs/ARCHITECTURE.md`)](docs/ARCHITECTURE.md) - The SOLID pipeline design.
4. [Component Pipeline (`docs/PIPELINE.md`)](docs/PIPELINE.md) - How messages flow through the system.
5. [Interfaces (`docs/INTERFACES.md`)](docs/INTERFACES.md)
6. [Metrics & Telemetry (`docs/METRICS.md`)](docs/METRICS.md)

**API Data Contracts:**
7. [Message Schema (`docs/MESSAGE_SCHEMA.md`)](docs/MESSAGE_SCHEMA.md) - Pydantic definitions and Priority indexing.
8. [Tokenization Limits (`docs/TOKENIZATION.md`)](docs/TOKENIZATION.md) - Explicit Tiktoken constraints and algorithmic slicing.
9. [Filtering Modes (`docs/MODES.md`)](docs/MODES.md)
10. [Deterministic Compression (`docs/COMPRESSION.md`)](docs/COMPRESSION.md)
11. [Async Providers (`docs/PROVIDER.md`)](docs/PROVIDER.md)

---

## ✨ Core Features

| Feature | Description |
|--------|-------------|
| **Context Sessions** | Stateful wrapper for seamless multi-turn Agent memory |
| **Context Caching** | Cryptographic hashes skip CPU compression on static RAG items |
| **Context Ranking** | Dynamic scoring algorithms prioritizing TimeDecay over old logs |
| **Deterministic Compression** | Remove boilerplate safely without expensive LLM distillation latency |
| **Token Budgeting** | Hard `tiktoken` limits strictly prioritizing semantic retention |
| **Provider Agnostic** | Standard Async API adaptable for OpenAI, Claude, or local Ollama |

---

## 📦 Installation & Integration

ContextFlow is explicitly designed to support **both** public Open Source workflows (PyPI) and private internal Developer Integration (dropping it into your Monorepos).

### Option 1: Public PyPI (Recommended)
If you are building an external application, simply install the official package:
```bash
pip install contextflow
```

### Option 2: Local Internal Integration
If you are dropping ContextFlow into an existing secure company Monorepo:
```bash
git clone https://github.com/studentleaner/ContextFlow.git
cd ContextFlow
pip install -e .
```

## ⚡ Quick Start

```python
from contextflow.pipeline import ContextPipeline
from contextflow.mode import MinimalMode
from contextflow.compression import StandardCompressor
from contextflow.provider import MockProvider

pipeline = ContextPipeline(
    sources=[],
    mode=MinimalMode(),
    compressor=StandardCompressor(),
    provider=MockProvider(),
)

response = pipeline.run(goal="Summarize the system errors from the logs.")
print(response)
```

## 📄 License
MIT License
