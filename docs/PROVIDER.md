# Execution Boundaries (Providers)

Rather than directly calling OpenAI APIs and enforcing monolithic vendor lock-in within your Agent, ContextFlow uses standard abstract Provider bridges.

## Non-Blocking I/O
Providers natively execute with `async def arun()`. This guarantees that your surrounding State Graph architecture (LangGraph) continues ticking async worker threads concurrently without locking the CPU while fetching network LLM requests.

## `MockProvider` (TDD Testing)
When constructing complex Graph loops, you can inject `MockProvider()` to run unit tests and latency traces natively over your pipeline arrays without utilizing a single real API token.

## `OpenAIProvider`
Using standard `openai.AsyncClient`, the wrapper automatically handles flattening ContextFlow Pydantic Arrays safely into standard `to_llm_dict()` requirements internally, dropping `tiktoken` byte identifiers and `priority` ranks natively prior to the network hop.
