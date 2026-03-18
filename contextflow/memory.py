from typing import List
from .schema import ContextItem

class SharedContextBank:
    """
    Acts as a central knowledge graph / memory bank for multi-agent loops.
    """
    def __init__(self):
        self.state = {}

    def insert(self, key, text):
        self.state[key] = text

    def read(self, keys: list):
        return [self.state[k] for k in keys if k in self.state]
        
    def generate_source(self, keys: list) -> List[ContextItem]:
        messages = []
        for k in keys:
            if k in self.state:
                messages.append(ContextItem(
                    role="system",
                    content=f"Shared Context [{k}]:\n{self.state[k]}",
                    priority=40
                ))
        return messages

class GraphContextBank:
    """
    A lightweight dictionary-based Knowledge Graph for ContextFlow.
    """
    def __init__(self):
        self.nodes = {} 
        self.edges = {} 

    def add_node(self, entity_id, context_text):
        self.nodes[entity_id] = context_text
        if entity_id not in self.edges:
            self.edges[entity_id] = []

    def add_edge(self, entity1, entity2):
        if entity1 in self.edges and entity2 in self.nodes:
            if entity2 not in self.edges[entity1]:
                self.edges[entity1].append(entity2)
        if entity2 in self.edges and entity1 in self.nodes:
            if entity1 not in self.edges[entity2]:
                self.edges[entity2].append(entity1)

    def compile_source(self, root_entities: list, max_depth=1) -> List[ContextItem]:
        visited = set()
        queue = [(e, 0) for e in root_entities if e in self.nodes]
        
        while queue:
            current, current_depth = queue.pop(0)
            if current not in visited:
                visited.add(current)
                if current_depth < max_depth:
                    for neighbor in self.edges.get(current, []):
                        if neighbor not in visited:
                            queue.append((neighbor, current_depth + 1))
                            
        messages = []
        for v in visited:
            messages.append(ContextItem(
                role="system", 
                content=f"Graph Memory Node [{v}]: {self.nodes[v]}",
                priority=30
            ))
        return messages
