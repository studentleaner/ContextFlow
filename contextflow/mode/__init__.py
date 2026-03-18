from typing import List
from ..core.interfaces import ContextMode
from ..core.schema import ContextItem

class MinimalMode(ContextMode):
    """
    Strips out 'assistant' and 'tool' reasoning logs. 
    Only keeps user instructions and system constraints.
    """
    def select(self, messages: List[ContextItem]) -> List[ContextItem]:
        return [m for m in messages if m.role in ["user", "system"]]

class FullMode(ContextMode):
    """
    Leaves the context array entirely untouched, passing everything downstream.
    """
    def select(self, messages: List[ContextItem]) -> List[ContextItem]:
        return messages