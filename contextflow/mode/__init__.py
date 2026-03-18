from typing import List
from ..core.interfaces import ContextMode
from ..core.schema import ContextItem
from ..core.registry import ModeRegistry

mode_registry = ModeRegistry("mode", ContextMode)

@mode_registry.register("minimal")
class MinimalMode(ContextMode):
    """
    Strips out 'assistant' and 'tool' reasoning logs. 
    Only keeps user instructions and system constraints.
    """
    def select(self, messages: List[ContextItem]) -> List[ContextItem]:
        return [m for m in messages if m.role in ["user", "system"]]

@mode_registry.register("full")
class FullMode(ContextMode):
    """
    Leaves the context array entirely untouched, passing everything downstream.
    """
    def select(self, messages: List[ContextItem]) -> List[ContextItem]:
        return messages

@mode_registry.register("semantic")
class SemanticMode(ContextMode):
    """
    Selects context items based on their semantic relevance to the implicit goal.
    Expects a scorer function `scorer(goal: str, text: str) -> float` and a threshold.
    """
    def __init__(self, scorer, threshold: float = 0.5):
        self.scorer = scorer
        self.threshold = threshold

    def select(self, messages: List[ContextItem]) -> List[ContextItem]:
        if not messages:
            return messages
            
        goal_msg = messages[-1]
        goal_text = goal_msg.content
        
        out = []
        for m in messages[:-1]:
            if m.role == "system":
                out.append(m)
                continue
                
            score = self.scorer(goal_text, m.content)
            if score >= self.threshold:
                out.append(m)
                
        out.append(goal_msg)
        return out