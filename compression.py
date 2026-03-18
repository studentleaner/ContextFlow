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
