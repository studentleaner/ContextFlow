import pytest
import asyncio
from contextflow.core.schema import ContextItem
from contextflow.mode import mode_registry
from contextflow.compression import compressor_registry
from contextflow.core.interfaces import Provider

class MockScorer:
    def __init__(self, scores):
        self.scores = scores
        self.calls = 0
        
    def __call__(self, goal, text):
        score = self.scores[self.calls]
        self.calls += 1
        return score

class MockProvider(Provider):
    async def arun(self, messages: list[ContextItem]) -> str:
        return f"Mock Distilled: {len(messages[0].content)} chars"

def test_semantic_mode():
    SemanticMode = mode_registry.get_class("semantic")
    
    # We will score the first user message 0.9 (keep) and the second 0.2 (drop)
    scorer = MockScorer([0.9, 0.2])
    mode = SemanticMode(scorer=scorer, threshold=0.5)
    
    messages = [
        ContextItem(role="system", content="System Prompt", priority=0),
        ContextItem(role="user", content="Relevant Context", priority=1),
        ContextItem(role="user", content="Irrelevant Context", priority=1),
        ContextItem(role="user", content="Goal Msg", priority=100)
    ]
    
    selected = mode.select(messages)
    
    assert len(selected) == 3
    assert selected[0].content == "System Prompt" # System preserved inherently
    assert selected[1].content == "Relevant Context" # Scored 0.9
    assert selected[2].content == "Goal Msg" # Goal kept (last msg)

def test_distillation_compressor():
    DistillationCompressor = compressor_registry.get_class("distillation")
    
    provider = MockProvider()
    compressor = DistillationCompressor(distillation_provider=provider, overflow_threshold=50)
    
    messages = [
        ContextItem(role="system", content="System messages should be preserved structurally regardless of size so they aren't compressed.", priority=0),
        ContextItem(role="user", content="Short", priority=1),
        ContextItem(role="user", content="This is a very long user message that should definitely exceed fifty characters and get safely distilled by the mock provider.", priority=1)
    ]
    
    compressed = asyncio.run(compressor.acompress(messages))
    
    assert len(compressed) == 3
    assert "System messages should be preserved" in compressed[0].content
    assert compressed[1].content == "Short"
    assert "Mock Distilled:" in compressed[2].content
    assert "[DISTILLED CONTEXT]:" in compressed[2].content
