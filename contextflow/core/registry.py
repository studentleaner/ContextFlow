from typing import Dict, Type, Any, Optional

class PluginRegistry:
    """
    Base generic registry for ContextFlow plugins.
    Ensures safe type-checked extensibility natively.
    """
    def __init__(self, name: str, base_class: Type):
        self.name = name
        self.base_class = base_class
        self._plugins: Dict[str, Type] = {}

    def register(self, name: str):
        """Decorator to register a class as a plugin."""
        def decorator(cls: Type):
            if not issubclass(cls, self.base_class):
                raise TypeError(f"Plugin {cls.__name__} must subclass {self.base_class.__name__}")
            self._plugins[name] = cls
            return cls
        return decorator

    def discover(self):
        """Auto-discovers and registers external plugins securely via standard Python entry_points."""
        import importlib.metadata
        group_name = f"contextflow.plugins.{self.name}"
        
        try:
            # Python 3.10+ robust grouping
            eps = importlib.metadata.entry_points(group=group_name)
        except TypeError:
            eps = importlib.metadata.entry_points().get(group_name, [])
            
        for ep in eps:
            if ep.name not in self._plugins:
                try:
                    plugin_class = ep.load()
                    self.register(ep.name)(plugin_class)
                except Exception:
                    # Ignore crashing external modules strictly, isolating registry faults
                    pass

    def get(self, name: str, **kwargs) -> Any:
        """Instantiates and returns a plugin by registered name."""
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not found in registry '{self.name}'. Available: {list(self._plugins.keys())}")
        return self._plugins[name](**kwargs)

    def get_class(self, name: str) -> Type:
        """Returns the uninstantiated plugin class by name."""
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not found in registry '{self.name}'.")
        return self._plugins[name]

    def list_plugins(self) -> list[str]:
        """Returns string names of all registered plugins."""
        return list(self._plugins.keys())

# Type-specific Registry Subclasses
class ModeRegistry(PluginRegistry): pass
class CompressorRegistry(PluginRegistry): pass
class ProviderRegistry(PluginRegistry): pass
class SourceRegistry(PluginRegistry): pass
class ScorerRegistry(PluginRegistry): pass
