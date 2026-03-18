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

class GraphContextBank:
    """
    A lightweight dictionary-based Knowledge Graph for ContextFlow.
    Allows agents to structure long-term memory spatially (Nodes + Edges)
    rather than linearly, preventing massive disorganized list arrays.
    """
    def __init__(self):
        self.nodes = {} 
        self.edges = {} 

    def add_node(self, entity_id, context_text):
        """Save a discrete concept or document chunk."""
        self.nodes[entity_id] = context_text
        if entity_id not in self.edges:
            self.edges[entity_id] = []

    def add_edge(self, entity1, entity2):
        """Connect two discrete context chunks associatively."""
        if entity1 in self.edges and entity2 in self.nodes:
            if entity2 not in self.edges[entity1]:
                self.edges[entity1].append(entity2)
        if entity2 in self.edges and entity1 in self.nodes:
            if entity1 not in self.edges[entity2]:
                self.edges[entity2].append(entity1)

    def compile_source(self, root_entities: list, max_depth=1):
        """
        Retrieves a spatially relevant sub-graph of memory based on active roots,
        returning it as a formatted array ready for the ContextPipeline.
        """
        visited = set()
        queue = [(e, 0) for e in root_entities if e in self.nodes]
        
        while queue:
            current, current_depth = queue.pop(0)
            if current not in visited:
                visited.add(current)
                # Expand neighbor frontier if we haven't hit the depth limit
                if current_depth < max_depth:
                    for neighbor in self.edges.get(current, []):
                        if neighbor not in visited:
                            queue.append((neighbor, current_depth + 1))
                            
        messages = []
        for v in visited:
            messages.append({
                "role": "system", 
                "content": f"Graph Memory Node [{v}]: {self.nodes[v]}"
            })
        return messages
