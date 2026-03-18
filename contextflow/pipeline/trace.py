from pydantic import BaseModel

class TraceReport(BaseModel):
    response: str
    tokens_before: int
    tokens_after: int
    cache_hits: int
    dropped_items: int
    mode_used: str
