# Deterministic Compression

This is the absolute core of ContextFlow. Compressors programmatically strip redundant token pollution *before* calling an LLM, saving immense API costs and dropping Time-To-First-Token (TTFT) significantly.

## The `StandardCompressor`
Unlike traditional RAG systems that ask an LLM to "summarize this context," ContextFlow uses pure Python execution.

1. **AST Protection:** It maps regular expressions over the `ContextItem` text to physically remove and safely cache Fenced Code Blocks (` ```python `) and Agent Function Tool JSON blobs (`{ "action": "xyz" }`).
2. **Redundancy Scrubbing:** Once the fragile schema blocks are stored independently, the compressor iterates through the volatile text lines: removing whitespace, blank carriage returns, and completely ignoring cyclical linear duplicates commonly found in massive error crash-logs or LangGraph loop traces.
3. **Reassembly:** The clean AST schema blocks are instantly rewritten perfectly identically into the compressed volatile text.

## The `DistillationCompressor`
For absolute extreme edge cases (where files exceed 100,000 tokens), an alternate compressor exists which uses a fast auxiliary LLM (like `gpt-4o-mini`) to compress massive strings densely before inserting them into an expensive `Claude 3.5 Sonnet` or `GPT-4o` reasoning graph.
