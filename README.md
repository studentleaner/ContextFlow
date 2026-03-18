# ContextFlow 🌊  
**Better Context > Bigger Models**

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-green)
![Architecture](https://img.shields.io/badge/design-SOLID-orange)
![LLM](https://img.shields.io/badge/LLM-context--engineering-purple)

ContextFlow is a lightweight, deterministic Python library for **Context Engineering**.

It provides a structured pipeline to **select, compress, budget, and send context** to Large Language Models (LLMs) in a clean, predictable, and cost-efficient way.

Designed for:
- Agents (ReAct, LangGraph, CrewAI)
- RAG systems
- Coding assistants
- Long-running LLM loops

---

## 🚀 Why ContextFlow?

Modern LLM applications often fail not because of the model, but because of **bad context**. 
Massive contexts result in the "Lost in the Middle" phenomenon where models ignore relevant details.

**The Solution:** ContextFlow sits between your data sources and the LLM. 
It deterministically removes noise, enforces token limits, and structures logs/memory so you use fewer tokens, lower latency (TTFT), and reduce hallucination loops.

---

## 📚 Documentation

For a deep dive into how ContextFlow works and our plans for the future, explore the documentation:

1. [Architectural Analysis (`docs/ANALYSIS.md`)](docs/ANALYSIS.md) - Why Context Engineering matters and our concept evaluation.
2. [Project Architecture (`docs/ARCHITECTURE.md`)](docs/ARCHITECTURE.md) - The SOLID pipeline design.
3. [Component Pipeline (`docs/PIPELINE.md`)](docs/PIPELINE.md) - How messages flow through the system.
4. [Project Roadmap (`docs/ROADMAP.md`)](docs/ROADMAP.md) - Immediate and future development focus.
5. [Interfaces (`docs/INTERFACES.md`)](docs/INTERFACES.md)
6. [Metrics & Telemetry (`docs/METRICS.md`)](docs/METRICS.md)

---

## ✨ Core Features

| Feature | Description |
|--------|-------------|
| **Context Modes** | Filter relevant messages before injection |
| **Deterministic Compression** | Remove boilerplate & duplicate logs safely without LLM latency |
| **Token Budgeting** | Hard token limits to prevent context overflow |
| **Provider Agnostic** | Standard API adaptable for OpenAI, Claude, or local Ollama models |

---

## 📦 Installation & Quick Start

```bash
git clone https://github.com/studentleaner/ContextFlow.git
cd ContextFlow
pip install -e .
```

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
