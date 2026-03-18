from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any

class ContextItem(BaseModel):
    """
    The fundamental unit of data flowing through the Context Pipeline.
    Replacing raw dictionaries guarantees safety, explicit token boundaries,
    and priority ranking capabilities for mathematical context tracking.
    """
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    priority: int = 0
    tokens: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_llm_dict(self) -> Dict[str, str]:
        """Flattens the object specifically for OpenAI/Anthropic API consumption."""
        return {
            "role": self.role,
            "content": self.content
        }
