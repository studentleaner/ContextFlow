import json

class MetricsCollector:
    """
    Headless logger tracking explicit Context Pipeline performance.
    In production, developers pipe this data cleanly into Datadog or LangSmith.
    """
    def __init__(self):
        self.data = {}

    def record(self, tokens_before: int, tokens_after: int, latency_ms: float = 0.0):
        self.data["tokens_before"] = tokens_before
        self.data["tokens_after"] = tokens_after
        self.data["latency_ms"] = latency_ms
        
        if tokens_before > 0:
            self.data["compression_ratio"] = tokens_after / tokens_before
        else:
            self.data["compression_ratio"] = 1.0

    def export(self) -> str:
        return json.dumps(self.data, indent=2)