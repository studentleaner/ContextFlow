import os
import sys

# Bind local package environment 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contextflow import (
    ContextPipeline, FullMode, StandardCompressor, 
    TokenBudget, MockProvider, MetricsCollector, ContextItem, NativeCache
)

def run_benchmark():
    print("====================================")
    print("   ContextFlow Hardening Benchmark  ")
    print("====================================\\n")

    # 1. Instantiate engine safely tracking absolute pipeline performance logs natively
    metrics = MetricsCollector()
    cache = NativeCache()
    pipeline = ContextPipeline(
        sources=[],
        mode=FullMode(),
        compressor=StandardCompressor(),
        budget=TokenBudget(max_tokens=2000), 
        provider=MockProvider(),
        metrics=metrics,
        cache=cache
    )

    # 2. Create explosive 10,000 token payload synthetically
    massive_noise = "error crash dump [sys.oom] \\n" * 500
    duplicate_noise = massive_noise * 10 # Massive deterministic redundancy

    state_history = [
        ContextItem(role="system", content="Never break code sequences", priority=100),
        ContextItem(role="user", content=f"Analyze massive payload:\\n{duplicate_noise}", priority=50)
    ]

    print("Injecting explosive repeating payload into Engine...")
    
    # 3. Execute synchronous performance tracker natively
    pipeline.run("What caused the crash?", state_history=state_history)

    # 4. Harvest the metrics payload structurally
    data = metrics.data
    tokens_before = data.get("tokens_before", 0)
    tokens_after = data.get("tokens_after", 0)
    latency = data.get("latency_ms", 0)
    
    print(f"\\n--- Benchmark Results ---")
    print(f"Input Tokens (Estimated):    {tokens_before}")
    print(f"Output Tokens (Tiktoken):    {tokens_after}")
    print(f"Total Tokens Erased Natively: {tokens_before - tokens_after}")
    print(f"Pipeline Deduplication Latency: {latency:.2f} ms")
    
    if tokens_before > 0:
        saved_percent = round((1 - (tokens_after / tokens_before)) * 100, 2)
        print(f"Token Compression Ratio:   {saved_percent}% Savings Natively")

if __name__ == "__main__":
    run_benchmark()
