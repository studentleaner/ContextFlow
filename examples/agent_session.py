import asyncio
import sys
import os

# Emulate production pip layout natively mapping bridging namespaces internally
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contextflow import (
    ContextPipeline, ContextSession, ContextRanker, NativeCache,
    TimeDecayScorer, StandardCompressor, MinimalMode, TokenBudget, MockProvider
)

async def main():
    print("--- ContextFlow True Session Lifecycle Demo ---")
    
    # 1. Instantiate the explicit Engine Architectures natively
    pipeline = ContextPipeline(
        sources=[],
        mode=MinimalMode(),
        compressor=StandardCompressor(),
        budget=TokenBudget(max_tokens=4000),
        provider=MockProvider(),
        cache=NativeCache(),
        ranker=ContextRanker(TimeDecayScorer(base_priority=50)),
        debug=True  # Enables Trace Visibility natively
    )
    
    # 2. Wrap it natively inside a Stateful ContextSession matrix
    session = ContextSession(pipeline, system_prompt="You are an explicitly Purist Context Assistant.")
    
    # 3. Add explosive multi-turn Agent noise natively mimicking cyclomatic graphs
    print("\\n[Simulating 5 turns of historical graph noise...]")
    for i in range(5):
        session.add_turn("user", "Hello there " * 50)
        session.add_turn("assistant", f"I am a cyclical log message from tick [{i}]")

    print(f"\\nRaw Tracking State Length inside object: {len(session.history)} matrix components")
    print("Initiating Native Resolution matrix...\\n")

    # 4. Seamless Pipeline Execution (Watch the Pipeline Debug Trace output!)
    response = await session.resolve("Summarize the ultimate context vector.")
    print(f"\\nAgent Output: {response}")

if __name__ == "__main__":
    asyncio.run(main())
