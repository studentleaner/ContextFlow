from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from .schema import ContextItem

class ContextSource(ABC):
    """Responsible for retrieving raw text (files, DBs, URLs) and structuring them."""
    @abstractmethod
    def load(self) -> List[ContextItem]:
        pass

class ContextMode(ABC):
    """Filters or ranks messages based on rules before compression."""
    @abstractmethod
    def select(self, messages: List[ContextItem]) -> List[ContextItem]:
        pass

class Compressor(ABC):
    """Deterministically identifies token-dense noise and strips it."""
    @abstractmethod
    def compress(self, messages: List[ContextItem]) -> List[ContextItem]:
        pass

class Provider(ABC):
    """Abstract interface for LLM endpoints ensuring strict mapping boundaries."""
    @abstractmethod
    async def arun(self, goal: str, messages: List[ContextItem]) -> str:
        pass
