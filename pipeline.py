import time

class ContextPipeline:

    def __init__(self, sources, mode, compressor, provider, budget=None, metrics=None):
        self.sources = sources
        self.mode = mode
        self.compressor = compressor
        self.provider = provider
        self.budget = budget
        self.metrics = metrics

    def run(self, goal):
        
        messages = []
        for s in self.sources:
            messages.extend(s.load())

        messages.append({
            "role": "user",
            "content": goal,
        })

        # Track initial theoretical token count for metrics (rough estimate by characters if budget module isn't strictly available yet, or let budget do it)
        tokens_before = sum(len(m.get("content", "")) // 4 for m in messages)

        start_time = time.time()

        # 1. Mode Filter
        messages = self.mode.select(messages)

        # 2. Sequential String Compression
        messages = self.compressor.compress(messages)

        # 3. Token Truncation Budget
        if self.budget is not None:
            messages = self.budget.fit(messages)

        latency_ms = (time.time() - start_time) * 1000

        # Attempt to track exact tokens saved
        tokens_after = sum(len(m.get("content", "")) // 4 for m in messages)
        if hasattr(self.budget, "count_tokens") and self.budget:
            tokens_before = self.budget.count_tokens(" ".join(m.get("content","") for m in self.sources)) + self.budget.count_tokens(goal)
            tokens_after = self.budget.count_tokens(" ".join(m.get("content","") for m in messages))

        # 4. Telemetry Logging
        if self.metrics is not None:
            self.metrics.record("tokens_before", tokens_before)
            self.metrics.record("tokens_after", tokens_after)
            ratio = 0 if tokens_before == 0 else (tokens_after / tokens_before)
            self.metrics.record("compression_ratio", ratio)
            self.metrics.record("latency_ms", latency_ms)

        # 5. Network Provider Call
        return self.provider.chat(messages)
