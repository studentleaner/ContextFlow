import os
from typing import List
from ..core.interfaces import ContextSource
from ..core.schema import ContextItem
from ..core.registry import SourceRegistry

source_registry = SourceRegistry("source", ContextSource)

@source_registry.register("file")
class FileSource(ContextSource):
    """
    Native Source adapter that reads local markdown or log files directly into 
    the context array perfectly wrapped as an explicit System Prompt.
    """
    def __init__(self, filepaths: List[str]):
        self.filepaths = filepaths

    def load(self) -> List[ContextItem]:
        messages = []
        for filepath in self.filepaths:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                filename = os.path.basename(filepath)
                messages.append(ContextItem(
                    role="system",
                    content=f"File Content [{filename}]:\n{content}",
                    priority=50
                ))
        return messages
