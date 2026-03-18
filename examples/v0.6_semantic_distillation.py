import asyncio
from contextflow.pipeline import ContextPipeline
from contextflow.mode import mode_registry
from contextflow.compression import compressor_registry
from contextflow.provider import MockProvider
from contextflow.budget import TokenBudget
from contextflow.core.schema import ContextItem

# Retrieve natively registered Intelligence Layer nodes
SemanticMode = mode_registry.get_class("semantic")
DistillationCompressor = compressor_registry.get_class("distillation")

# Simple mock string-matching logic representing a Semantic Scorer
def mock_scorer(goal: str, text: str) -> float:
    return sum(1 for word in goal.lower().split() if word in text.lower())

async def main():
    mode = SemanticMode(scorer=mock_scorer, threshold=1.0)
    
    # We enforce aggressive summarization on any individual chunk > 50 chars natively
    compressor = DistillationCompressor(distillation_provider=MockProvider(), overflow_threshold=50)

    pipeline = ContextPipeline(
        sources=[],
        mode=mode,
        compressor=compressor,
        budget=TokenBudget(max_tokens=1000),
        provider=MockProvider(),
        debug=True # Traceability explicitly toggled
    )

    history = [
        ContextItem(role="system", content="You are a data extraction bot.", priority=0),
        # This will be dropped by the Semantic node for having 0 matches to "Find server data errors"
        ContextItem(role="user", content="Here is irrelevant conversational chitchat about birds singing.", priority=1),
        # This surpasses 50 characters, triggering asynchronous MockProvider distillation summarizations
        ContextItem(role="user", content="Here is a massive block of server logs containing data errors. " * 5, priority=2)
    ]

    print("--- Executing ContextFlow v0.6.0 Intelligence Pipeline ---")
    response = await pipeline.arun(goal="Find server data errors", state_history=history)
    print("\n--- Pipeline Yield ---")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
