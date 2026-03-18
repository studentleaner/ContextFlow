import re

class StandardCompressor:
    
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

    def compress(self, messages):
        out = []
        for m in messages:
            text = m.get("content", "")
            if isinstance(text, str):
                text = self.clean(text)
            
            out.append({
                "role": m.get("role", "user"),
                "content": text,
            })
        return out

class DistillationCompressor:
    """
    Uses a fast auxiliary LLM (like GPT-4o-mini or a local Ollama model) to aggressively 
    summarize enormous string payloads. 
    WARNING: Use sparingly. Deterministic compression (StandardCompressor) is always 
    preferred over LLM distillation due to latency and hallucination risks.
    """
    def __init__(self, distillation_provider, overflow_threshold=2000):
        self.provider = distillation_provider
        self.threshold = overflow_threshold

    def compress(self, messages):
        out = []
        for m in messages:
            content = m.get("content", "")
            
            # Only distill massive user blocks that threaten to blow up context limit
            if m.get("role") == "user" and len(content) > self.threshold:
                distilled = self.provider.chat([
                    {"role": "system", "content": "Summarize the following text extremely densely. You MUST retain all exact nouns, IDs, JSON schemas, URL links, and code blocks perfectly."},
                    {"role": "user", "content": content}
                ])
                out.append({"role": m.get("role", "user"), "content": f"[DISTILLED CONTEXT]:\n{distilled}"})
            else:
                out.append(m)
                
        return out
