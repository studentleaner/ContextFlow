import hashlib
from typing import List, Dict
from ..core.schema import ContextItem
from .. import __version__ as ENGINE_VERSION

class NativeCache:
    """
    Cryptographic caching for stateless pipeline compression phases.
    Prevents CPU-heavy regex routines from executing on static PDFs or System Prompts continuously.
    """
    def __init__(self, disable_cache: bool = False):
        self.store: Dict[str, ContextItem] = {}
        self.disable_cache = disable_cache

    def _hash(self, item: ContextItem, mode_name: str, compressor) -> str:
        CACHE_SCHEMA_VERSION = "0.6.1"
        compressor_name = compressor.__class__.__name__
        components = [item.content, ENGINE_VERSION, CACHE_SCHEMA_VERSION, compressor_name, mode_name]
        
        # Ensure instances dynamically report their state
        if hasattr(compressor, '__hash_context__'):
            components.append(str(compressor.__hash_context__))
        else:
            if hasattr(compressor, 'threshold'):
                components.append(f"threshold:{compressor.threshold}")
            if hasattr(compressor, 'provider') and hasattr(compressor.provider, 'model'):
                components.append(f"model:{compressor.provider.model}")
                
        base_str = "|".join(components)
        return hashlib.md5(base_str.encode('utf-8')).hexdigest()

    def get_or_set(self, item: ContextItem, mode_name: str, compressor) -> ContextItem:
        if self.disable_cache:
            return compressor.compress([item])[0]
            
        # Skipping hash overhead for tiny chat inputs (under 500 characters)
        if len(item.content) < 500:
            return compressor.compress([item])[0]
            
        h = self._hash(item, mode_name, compressor)
        if h in self.store:
            return self.store[h]
            
        compressed_item = compressor.compress([item])[0]
        self.store[h] = compressed_item
        return compressed_item

    async def aget_or_set(self, item: ContextItem, mode_name: str, compressor) -> ContextItem:
        if self.disable_cache:
            res = await compressor.acompress([item])
            return res[0]
            
        if len(item.content) < 500:
            res = await compressor.acompress([item])
            return res[0]
            
        h = self._hash(item, mode_name, compressor)
        if h in self.store:
            return self.store[h]
            
        res = await compressor.acompress([item])
        compressed_item = res[0]
        self.store[h] = compressed_item
        return compressed_item
