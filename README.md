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

- Agents
- RAG systems
- Coding assistants
- DevOps / Runtime agents
- Long-running LLM loops
- Enterprise LLM backends
- Local / Cloud / Hybrid models

---

## 🚀 Why ContextFlow?

Modern LLM applications often fail not because of the model,
but because of **bad context**.

### The Problem

- 💸 Expensive  
  Sending redundant logs, memory, and filler text wastes tokens.

- 🐢 Slow  
  Large prompts increase latency and TTFT.

- 😵 Confused  
  Models lose focus when context is cluttered.

- 🔁 Unstable Agents  
  Context grows every loop until it breaks.

- 💥 Token Overflow  
  Context window exceeded → errors / truncation.

---

### The Solution

ContextFlow sits between your data sources and the LLM.
Sources → ContextFlow → LLM

It:

- selects only relevant data
- removes noise deterministically
- enforces token limits
- records metrics
- keeps prompts clean

Result:

It:

- selects only relevant data
- removes noise deterministically
- enforces token limits
- records metrics
- keeps prompts clean

Result:
Smaller prompt
Lower cost
Faster response
Better output
Stable agents


---

## 🧠 What is Context Engineering?

Context Engineering = controlling what the model sees.

ContextFlow implements:

ContextMode
Compression
TokenBudget
MetricsInterface:

chat(messages)

🤖 Agent Ready

Designed for loops.

observe
 → contextflow
 → LLM
 → action
 → repeat

Works with:

ReAct
LangGraph
CrewAI
custom agents
runtime systems

🗺 Roadmap
Stage 0–4

    Interfaces

    Pipeline

    ContextMode

    Compression

Stage 5–8

    TokenBudget

    Metrics

    Provider

    Config

Stage 9–11

    Advanced modes

    Benchmarks

    Agent integration

Upcoming

    Semantic compression

    Distillation

    Multi-agent context

    Cache / KV reuse

    Context graphs

🧱 Design Principles

Simple > clever
Deterministic > magic
Small core > big framework
Context > prompt
Less tokens > more tokens

🤝 Contributing

Before contributing, read:

ARCHITECTURE.md
PIPELINE.md

Rules:

    keep it simple

    no heavy framework

    no hidden state

    no magic globals

📄 License

MIT License
🌊 ContextFlow

Better Context > Bigger Models.


---

✅ This is ready to paste into GitHub README.md  
✅ Proper badges  
✅ Proper formatting  
✅ Detailed  
✅ OSS style  
✅ Clean architecture  
✅ Matches your project  

---

If you want next, I can make:

- ARCHITECTURE.md detailed
- PIPELINE.md detailed
- diagram ascii / svg
- logo for ContextFlow

Just say.
Provider
Pipeline


Pipeline:

Sources
→ Mode
→ Compression
→ Budget
→ Provider
→ Metrics


This is the missing layer in most LLM apps.

---

## ✨ Core Features

| Feature | Description |
|--------|-------------|
| Context Modes | Select only relevant messages |
| Deterministic Compression | Remove filler & duplicates safely |
| Token Budgeting | Hard limit to avoid overflow |
| Metrics & Telemetry | Track tokens, latency, cost |
| Provider Agnostic | OpenAI / Claude / Ollama / local |
| Agent Ready | Works in loops & investigations |
| SOLID Architecture | Clean, extensible design |
| Fast | No ML in compression path |

---

## 📦 Installation

```bash
git clone https://github.com/studentleaner/ContextFlow.git
cd ContextFlow
pip install -e .

⚡ Quick Start
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

response = pipeline.run(
    goal="Summarize the system errors from the logs."
)

print(response)

🏛 Architecture

ContextFlow follows a simple SOLID architecture.
Sources
   ↓
ContextMode
   ↓
Compressor
   ↓
TokenBudget
   ↓
Provider
   ↓
Metrics

| Component     | Purpose                    |
| ------------- | -------------------------- |
| ContextSource | Load memory / logs / files |
| ContextMode   | Select relevant messages   |
| Compressor    | Remove noise               |
| TokenBudget   | Fit context window         |
| Provider      | Call LLM                   |
| Metrics       | Track usage                |
| Pipeline      | Orchestrate flow           |

🧩 Context Modes

Modes define how context is selected.

Examples:
MinimalMode
FullMode
InvestigationMode
AgentMode
RuntimeMode

Example:
InvestigationMode
 → goal
 → hops
 → memory
 → tools

🧹 Deterministic Compression

AgentReady-style compression.

Removes:

whitespace

duplicate lines

filler words

boilerplate

empty lines

Keeps:

code

numbers

URLs

structure

Goal:
Same meaning
Fewer tokens

📏 Token Budget

Prevents overflow.
max_tokens
truncate
drop old messages
fit window

Works with:
OpenAI
Claude
Gemini
Ollama
local models

📊 Metrics

ContextFlow records:
tokens_before
tokens_after
compression_ratio
latency
mode
provider
cost_estimate

Used for:
debug
optimization
benchmark
monitoring

🔌 Provider Agnostic

Supports any LLM.

Adapters:
OpenAIProvider
AnthropicProvider
OllamaProvider
vLLMProvider
MockProvider

Interface:

chat(messages)
🤖 Agent Ready

Designed for loops.

observe
 → contextflow
 → LLM
 → action
 → repeat

Works with:

ReAct
LangGraph
CrewAI
custom agents
runtime systems
🗺 Roadmap
Stage 0–4

Interfaces

Pipeline

ContextMode

Compression

Stage 5–8

TokenBudget

Metrics

Provider

Config

Stage 9–11

Advanced modes

Benchmarks

Agent integration

Upcoming

Semantic compression

Distillation

Multi-agent context

Cache / KV reuse

Context graphs

🧱 Design Principles
Simple > clever
Deterministic > magic
Small core > big framework
Context > prompt
Less tokens > more tokens
🤝 Contributing

Before contributing, read:

ARCHITECTURE.md
PIPELINE.md

Rules:

keep it simple

no heavy framework

no hidden state

no magic globals

📄 License

MIT License

🌊 ContextFlow

Better Context > Bigger Models.


---

✅ This is ready to paste into GitHub README.md  
✅ Proper badges  
✅ Proper formatting  
✅ Detailed  
✅ OSS style  
✅ Clean architecture  
✅ Matches your project  

---

