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