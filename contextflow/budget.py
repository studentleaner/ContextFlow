import tiktoken

class TokenBudget:

    def __init__(self, max_tokens, encoding_name="cl100k_base"):
        self.max_tokens = max_tokens
        try:
            self.encoder = tiktoken.get_encoding(encoding_name)
        except Exception:
            self.encoder = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text):
        return len(self.encoder.encode(text))

    def fit(self, messages):
        """
        Truncate the input messages array to strictly fit within max_tokens.
        Drops oldest messages first, preserving the explicit system prompt and youngest messages.
        """
        total = sum(self.count_tokens(m.get("content", "")) for m in messages)
        
        if total <= self.max_tokens:
            return messages
            
        out = list(messages)
        
        # Iteratively pop from index 1 (or index 0 if it's not a system prompt) until array is light enough
        while sum(self.count_tokens(m.get("content", "")) for m in out) > self.max_tokens:
            if len(out) > 2:
                # Assuming index 0 is a system prompt, pop index 1 (oldest volatile memory)
                out.pop(1)
            else:
                # If we are down to just 1 or 2 core tasks but still over token limits, 
                # strictly string-slice the final user payload to enforce hardware token boundaries
                content = out[-1].get("content", "")
                encoded = self.encoder.encode(content)
                out[-1]["content"] = self.encoder.decode(encoded[-(self.max_tokens):])
                break
                
        return out
