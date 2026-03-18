import os

class FileSource:
    """Loads a physical local file into the standard context array payload."""
    
    def __init__(self, filepath, role="user"):
        self.filepath = filepath
        self.role = role

    def load(self):
        if not os.path.exists(self.filepath):
            # For robustness in agent loops, fail silently gracefully rather than throwing runtime errors
            return []
            
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return [{
            "role": self.role, 
            "content": f"File Content ({os.path.basename(self.filepath)}):\n{content}"
        }]
