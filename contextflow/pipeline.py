import time
import asyncio
from typing import List, Optional, Callable
from .schema import ContextItem

class ContextPipeline:
    def __init__(self, sources, mode, compressor, budget, provider, metrics=None,
                 on_before_mode: Optional[Callable] = None,
                 on_after_mode: Optional[Callable] = None,
                 on_before_provider: Optional[Callable] = None):
        """
        Orchestration class handling the flow of ContextItems.
        Added explicit event hooks to fulfill Phase 5 telemetry requirements.
        """
        self.sources = sources
        self.mode = mode
        self.compressor = compressor
        self.budget = budget
        self.provider = provider
        self.metrics = metrics
        
        self.on_before_mode = on_before_mode
        self.on_after_mode = on_after_mode
        self.on_before_provider = on_before_provider

    async def arun(self, goal: str) -> str:
        """Asynchronous execution for multi-agent loops like LangGraph or CrewAI."""
        messages: List[ContextItem] = []
        for s in self.sources:
            messages.extend(s.load())

        # 1. Prefix Caching Sequencer
        system_msgs = [m for m in messages if m.role == "system"]
        file_msgs = [m for m in messages if "File Content" in m.content]
        volatile_msgs = [m for m in messages if m not in system_msgs and m not in file_msgs]
        
        messages = system_msgs + file_msgs + volatile_msgs

        # Append execution goal with maximum priority
        messages.append(ContextItem(role="user", content=goal, priority=100))

        tokens_before = sum(len(m.content) // 4 for m in messages)
        start_time = time.time()

        # Telemetry Hook 1
        if self.on_before_mode:
            self.on_before_mode(messages)

        # 2. Mode Filter
        messages = self.mode.select(messages)

        # Telemetry Hook 2
        if self.on_after_mode:
            self.on_after_mode(messages)

        # 3. Deterministic Compression & Ranking Budget
        messages = self.compressor.compress(messages)
        messages = self.budget.enforce(messages)

        # Telemetry Hook 3
        if self.on_before_provider:
            self.on_before_provider(messages)

        tokens_after = sum(len(m.content) // 4 for m in messages)
        latency_ms = (time.time() - start_time) * 1000

        # Telemetry Record
        if self.metrics:
            self.metrics.record(tokens_before, tokens_after, latency_ms)

        # 4. Async Provider Call
        response = await self.provider.arun(messages)
        return response
        
    def run(self, goal: str) -> str:
        """Fallback synchronous method for legacy integrations."""
        return asyncio.run(self.arun(goal))
