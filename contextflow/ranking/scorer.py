from typing import List
from ..core.schema import ContextItem
from ..core.registry import ScorerRegistry

class Scorer:
    def score(self, item: ContextItem, index: int, total: int) -> int:
        raise NotImplementedError

scorer_registry = ScorerRegistry("scorer", Scorer)

@scorer_registry.register("time_decay")
class TimeDecayScorer(Scorer):
    """
    Automatically penalizes the priority of older contextual history dynamically.
    Ensures that fresh insights survive Budget constraints natively.
    """
    def __init__(self, base_priority: int = 50, decay_rate: int = 2):
        self.base_priority = base_priority
        self.decay_rate = decay_rate
        
    def score(self, item: ContextItem, index: int, total: int) -> int:
        # System constraints are fundamentally immune to all architectural decay
        if item.role == "system":
            return 100 
            
        distance_from_now = total - index
        penalty = distance_from_now * self.decay_rate
        return max(0, self.base_priority - penalty)

class ContextRanker:
    """Orchestration block modifying arrays linearly using assigned scoring heuristics."""
    def __init__(self, scorer: Scorer):
        self.scorer = scorer

    def apply(self, messages: List[ContextItem]) -> List[ContextItem]:
        total = len(messages)
        for i, m in enumerate(messages):
            m.priority = self.scorer.score(m, i, total)
        return messages
