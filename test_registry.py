import pytest
from contextflow.core.registry import PluginRegistry
from contextflow.mode import mode_registry, MinimalMode, FullMode
from contextflow.compression import compressor_registry, StandardCompressor, DistillationCompressor
from contextflow.provider import provider_registry, MockProvider, OpenAIProvider
from contextflow.sources import source_registry, FileSource
from contextflow.ranking import scorer_registry, TimeDecayScorer

class DummyBase:
    pass

def test_generic_registry():
    registry = PluginRegistry("test", DummyBase)
    
    @registry.register("my_plugin")
    class MyPlugin(DummyBase):
        pass
        
    assert "my_plugin" in registry.list_plugins()
    assert registry.get_class("my_plugin") is MyPlugin
    instance = registry.get("my_plugin")
    assert isinstance(instance, MyPlugin)

def test_registry_type_checking():
    registry = PluginRegistry("test", DummyBase)
    
    with pytest.raises(TypeError):
        @registry.register("invalid")
        class InvalidPlugin:
            pass

def test_mode_registry():
    plugins = mode_registry.list_plugins()
    assert "minimal" in plugins
    assert "full" in plugins
    assert issubclass(mode_registry.get_class("minimal"), MinimalMode)

def test_compressor_registry():
    plugins = compressor_registry.list_plugins()
    assert "standard" in plugins
    assert "distillation" in plugins
    assert issubclass(compressor_registry.get_class("standard"), StandardCompressor)

def test_provider_registry():
    plugins = provider_registry.list_plugins()
    assert "mock" in plugins
    assert "openai" in plugins

def test_source_registry():
    plugins = source_registry.list_plugins()
    assert "file" in plugins

def test_scorer_registry():
    plugins = scorer_registry.list_plugins()
    assert "time_decay" in plugins

def test_auto_discovery(monkeypatch):
    import importlib.metadata
    from contextflow.core.interfaces import ContextMode
    
    class MockMode(ContextMode):
        def select(self, messages): return messages
        
    class MockEntryPoint:
        def __init__(self, name):
            self.name = name
        def load(self):
            return MockMode
            
    def mock_entry_points(group=None):
        if group == "contextflow.plugins.mode":
            return [MockEntryPoint("mock_external")]
        return []
        
    monkeypatch.setattr(importlib.metadata, "entry_points", mock_entry_points)
    mode_registry.discover()
    
    assert "mock_external" in mode_registry.list_plugins()
    assert mode_registry.get_class("mock_external") is MockMode
