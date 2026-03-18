import hashlib
from typing import List, Dict
from ..core.schema import ContextItem

class NativeCache:
    """
    Cryptographic caching for stateless pipeline compression phases.
    Prevents CPU-heavy regex routines from executing on static PDFs or System Prompts continuously.
    """
    def __init__(self):
        self.store: Dict[str, ContextItem] = {}

    def _hash(self, content: str) -> str:
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def get_or_set(self, item: ContextItem, compressor) -> ContextItem:
        # Skipping hash overhead for tiny chat inputs (under 500 characters)
        if len(item.content) < 500:
            return compressor.compress([item])[0]
            
        h = self._hash(item.content)
        if h in self.store:
            return self.store[h]
            
        compressed_item = compressor.compress([item])[0]
        self.store[h] = compressed_item
        return compressed_item
