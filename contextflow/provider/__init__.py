import asyncio
from typing import List
from ..core.schema import ContextItem

class Provider:
    """Abstract base definition handling LLM executions asymptotically."""
    async def arun(self, messages: List[ContextItem]) -> str:
        raise NotImplementedError

class MockProvider(Provider):
    async def arun(self, messages: List[ContextItem]) -> str:
        await asyncio.sleep(0.5) # Properly simulate network latency without blocking the loop
        return "{ \"status\": \"success\", \"message\": \"mock response\" }"

class OpenAIProvider(Provider):
    """Async provider bridging exactly with the OpenAI AsyncClient"""
    def __init__(self, api_key: str, model: str):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def arun(self, messages: List[ContextItem]) -> str:
        # Map our schema dicts natively to OpenAI's required format
        api_messages = [m.to_llm_dict() for m in messages]
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=api_messages
        )
        return response.choices[0].message.content
