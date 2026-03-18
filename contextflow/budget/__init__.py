from typing import List
import tiktoken
from ..core.schema import ContextItem

class TokenEstimator:
    """Exact byte-pair encoding tracker responding to the OSS audit requests."""
    def __init__(self, model_name="gpt-4"):
        self.encoder = tiktoken.encoding_for_model(model_name)
    
    def estimate(self, text: str) -> int:
        return len(self.encoder.encode(text))

class TokenBudget:
    def __init__(self, max_tokens: int, estimator: TokenEstimator = None):
        self.max_tokens = max_tokens
        self.estimator = estimator or TokenEstimator()

    def enforce(self, messages: List[ContextItem]) -> List[ContextItem]:
        """
        Calculates exact tokens using tiktoken natively.
        Priority culling: drops priority=0 items entirely before relying on naive truncation.
        """
        for m in messages:
            if m.tokens is None:
                m.tokens = self.estimator.estimate(m.content)
                
        total_tokens = sum(m.tokens for m in messages)
        if total_tokens <= self.max_tokens:
            return messages

        # Strategy 1: Drop LOW PRIORITY (priority <= 0) elements completely
        out = []
        cull_budget = total_tokens
        for m in reversed(messages):
            if cull_budget > self.max_tokens and m.priority <= 0 and m.role != "system":
                cull_budget -= m.tokens
                continue
            out.insert(0, m)

        # Strategy 2: Absolute Limit (Naive Slicing if heavily overflowed despite priority fixes)
        final_out = []
        current_tokens = 0
        for m in reversed(out):
            # System Prompts legally circumvent standard truncation rules for Agent security
            if current_tokens + m.tokens <= self.max_tokens or m.role == "system":
                final_out.insert(0, m)
                current_tokens += m.tokens
            elif current_tokens < self.max_tokens:
                allowed_tokens = self.max_tokens - current_tokens
                if allowed_tokens > 10:
                    encoded = self.estimator.encoder.encode(m.content)
                    sliced_text = self.estimator.encoder.decode(encoded[:allowed_tokens])
                    sliced_item = ContextItem(
                        role=m.role, 
                        content=sliced_text + "... [TRUNCATED BUDGET]",
                        priority=m.priority,
                        tokens=allowed_tokens
                    )
                    final_out.insert(0, sliced_item)
                    current_tokens += allowed_tokens

        return final_out
