from typing import List
from ..core.schema import ContextItem

class ContextSession:
    """
    State-wrapper hiding explicit array mapping overhead from internal pipelines.
    Allows cyclomatic generation environments to effortlessly push turns iteratively natively.
    """
    def __init__(self, pipeline, system_prompt: str = ""):
        self.pipeline = pipeline
        self.history: List[ContextItem] = []
        if system_prompt:
            self.history.append(ContextItem(role="system", content=system_prompt, priority=100))
            
    def add_turn(self, role: str, content: str, priority: int = 50):
        self.history.append(ContextItem(role=role, content=content, priority=priority))
        
    async def resolve(self, goal: str) -> str:
        """
        Executes the explicit history payload through the attached pipeline architecture natively,
        while seamlessly caching the successful output turn.
        """
        response = await self.pipeline.arun(goal, state_history=self.history)
        self.history.append(ContextItem(role="user", content=goal))
        self.history.append(ContextItem(role="assistant", content=response))
        return response
        
    def resolve_sync(self, goal: str) -> str:
        import asyncio
        return asyncio.run(self.resolve(goal))
