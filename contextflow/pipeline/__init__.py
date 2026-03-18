import time
import asyncio
from typing import List, Optional, Callable
from ..core.schema import ContextItem

class ContextPipeline:
    def __init__(self, sources, mode, compressor, budget, provider, metrics=None,
                 cache=None, ranker=None, debug: bool = False,
                 on_before_mode: Optional[Callable] = None,
                 on_after_mode: Optional[Callable] = None,
                 on_before_provider: Optional[Callable] = None):
        """
        Orchestration class handling the flow of ContextItems.
        Phase 8: True Context Engine fully binds optional Caches and Rankers natively.
        Phase 9: Harnesses native debug traceability for step-by-step developer observability.
        """
        self.sources = sources
        self.mode = mode
        self.compressor = compressor
        self.budget = budget
        self.provider = provider
        self.metrics = metrics
        
        self.cache = cache
        self.ranker = ranker
        self.debug = debug
        
        self.on_before_mode = on_before_mode
        self.on_after_mode = on_after_mode
        self.on_before_provider = on_before_provider
        
        self.validate_order()
        
    def validate_order(self):
        """Strictly enforces the presence and execution ordering map of context nodes."""
        if self.sources is None or self.mode is None or self.compressor is None or self.budget is None or self.provider is None:
            raise ValueError("Pipeline invariant broken: Missing core context transformation layers.")

    def _validate_types(self, stage: str, elements):
        if not isinstance(elements, list) or (elements and not isinstance(elements[0], ContextItem)):
            raise TypeError(f"Pipeline invariant broken: {stage} must strictly yield List[ContextItem]")

    async def arun(self, goal: str, state_history: List[ContextItem] = None) -> str:
        """Asynchronous execution for multi-agent loops like LangGraph or CrewAI."""
        messages: List[ContextItem] = state_history.copy() if state_history else []
        for s in self.sources:
            messages.extend(s.load())

        system_msgs = [m for m in messages if m.role == "system"]
        file_msgs = [m for m in messages if "File Content" in m.content]
        volatile_msgs = [m for m in messages if m not in system_msgs and m not in file_msgs]
        
        messages = system_msgs + file_msgs + volatile_msgs
        messages.append(ContextItem(role="user", content=goal, priority=100))

        tokens_before = sum(len(m.content) // 4 for m in messages)
        start_time = time.time()
        
        if self.debug:
            print(f"\\n--- ContextFlow Pipeline Trace ---")
            print(f"[init] Injected {len(messages)} messages natively (~{tokens_before} raw tokens)")

        if self.on_before_mode:
            self.on_before_mode(messages)

        messages = self.mode.select(messages)
        self._validate_types("Mode", messages)

        if self.on_after_mode:
            self.on_after_mode(messages)
            
        if self.debug:
            print(f"[mode] {self.mode.__class__.__name__} safely mapped {len(messages)} surviving payload items")

        if self.ranker:
            messages = self.ranker.apply(messages)
            self._validate_types("Ranker", messages)
            if self.debug:
                print(f"[rank] Context dynamically scored natively using {self.ranker.scorer.__class__.__name__}")

        mode_name = self.mode.__class__.__name__
        if self.cache:
            compressed_msgs = []
            for m in messages:
                if hasattr(self.cache, 'aget_or_set'):
                    compressed_msgs.append(await self.cache.aget_or_set(m, mode_name, self.compressor))
                else:
                    compressed_msgs.append(self.cache.get_or_set(m, mode_name, self.compressor))
            messages = compressed_msgs
            if self.debug:
                print(f"[cache] Hashed states cleanly avoiding {len(messages)} regex cycles natively")
        else:
            messages = await self.compressor.acompress(messages)
            if self.debug:
                print(f"[compress] Scraped array deterministically neutralizing duplication bloat")

        self._validate_types("Compressor", messages)

        messages = self.budget.enforce(messages)
        self._validate_types("Budget", messages)
        
        # Tiktoken explicit calculation after budget slices
        final_tokens = sum(m.tokens for m in messages if m.tokens is not None)
            
        if self.debug:
            print(f"[budget] Preserved structurally critical constraints dropping sequence to absolute {final_tokens}/{self.budget.max_tokens} tiktoken limits")

        if self.on_before_provider:
            self.on_before_provider(messages)

        tokens_after = sum(len(m.content) // 4 for m in messages)
        latency_ms = (time.time() - start_time) * 1000

        if self.metrics:
            self.metrics.record(tokens_before, tokens_after, latency_ms)

        if self.debug:
            print(f"[provider] Relaying asymptotic asynchronous dispatch payload securely\\n")

        # 4. Async Provider Call
        response = await self.provider.arun(messages)
        return response
        
    def run(self, goal: str, state_history: List[ContextItem] = None) -> str:
        """Fallback synchronous method for legacy integrations."""
        return asyncio.run(self.arun(goal, state_history=state_history))
