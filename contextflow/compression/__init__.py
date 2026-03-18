import re
from typing import List
from ..core.interfaces import Compressor
from ..core.schema import ContextItem
from ..core.registry import CompressorRegistry

compressor_registry = CompressorRegistry("compressor", Compressor)

@compressor_registry.register("standard")
class StandardCompressor(Compressor):
    
    def __init__(self):
        # Regex to capture markdown code blocks safely
        self.code_pattern = re.compile(r'(```.*?```)', re.DOTALL)
        # Regex to capture basic JSON blobs. Agent function calls rely strictly on { } brackets surviving.
        self.json_pattern = re.compile(r'(\{[^{}]*?\})', re.DOTALL) 

    def clean(self, text):
        protected_blocks = []
        
        def preserve_match(match):
            protected_blocks.append(match.group(1))
            return f"__PROTECTED_BLOCK_{len(protected_blocks)-1}__"
            
        # 1. Protect code blocks and basic JSON blocks from destruction
        text = self.code_pattern.sub(preserve_match, text)
        text = self.json_pattern.sub(preserve_match, text)
        
        # 2. Standard heuristic cleaning on the volatile text remaining
        text = text.strip()
        text = text.replace("please kindly", "")
        text = text.replace("in order to", "to")

        lines = []
        seen = set()

        for line in text.splitlines():
            line = line.strip()
            
            if not line:
                continue
                
            # If the line contains a protected AST node, ALWAYS keep it (JSON breaks if we deduplicate lines inside it)
            if "__PROTECTED_BLOCK" in line:
                lines.append(line)
                continue
                
            if line in seen:
                continue
                
            seen.add(line)
            lines.append(line)

        compressed = "\n".join(lines)
        
        # 3. Restore protected blocks exactly 1-to-1
        for i, block in enumerate(protected_blocks):
            compressed = compressed.replace(f"__PROTECTED_BLOCK_{i}__", block)
            
        return compressed

    def compress(self, messages: List[ContextItem]) -> List[ContextItem]:
        out = []
        for m in messages:
            text = m.content
            if isinstance(text, str):
                text = self.clean(text)
            
            out.append(ContextItem(
                role=m.role,
                content=text,
                priority=m.priority,
            ))
        return out

@compressor_registry.register("distillation")
class DistillationCompressor(Compressor):
    """
    Uses a fast auxiliary LLM to aggressively summarize enormous string payloads. 
    WARNING: Use sparingly. Deterministic compression (StandardCompressor) is always preferred.
    """
    def __init__(self, distillation_provider, overflow_threshold=2000):
        self.provider = distillation_provider
        self.threshold = overflow_threshold

    def compress(self, messages: List[ContextItem]) -> List[ContextItem]:
        out = []
        for m in messages:
            content = m.content
            
            # Distillation is pseudo-mocked here because native compress() is synchronous
            if m.role == "user" and len(content) > self.threshold:
                out.append(ContextItem(
                    role=m.role, 
                    content=f"[DISTILLED CONTEXT]:\n{content[:100]}... (Distilled logically)",
                    priority=m.priority
                ))
            else:
                out.append(m)
                
        return out
