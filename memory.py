import os

class SharedContextBank:
    """
    Acts as a central knowledge graph / memory bank for multi-agent loops.
    Instead of passing a 50k token array between Agent A and Agent B, both agents
    borrow specifically tagged context blocks directly into their pipeline sources.
    """
    def __init__(self):
        self.state = {}

    def insert(self, key, text):
        """Save an observation or document into the global state."""
        self.state[key] = text

    def read(self, keys: list):
        """Retrieve specifically requested strings for agent injection."""
        return [self.state[k] for k in keys if k in self.state]
        
    def generate_source(self, keys: list):
        """Returns a ContextSource-compatible array of mapped messages for pipeline consumption."""
        messages = []
        for k in keys:
            if k in self.state:
                messages.append({
                    "role": "system",
                    "content": f"Shared Context [{k}]:\n{self.state[k]}"
                })
        return messages
