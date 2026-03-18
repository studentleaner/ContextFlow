import unittest
import os
from contextflow.budget import TokenBudget
from contextflow.pipeline import ContextPipeline
from contextflow.mode import MinimalMode
from contextflow.compression import StandardCompressor
from contextflow.provider import MockProvider
from contextflow.metrics import MetricsCollector
from contextflow.core.schema import ContextItem

class TestContextFlow(unittest.TestCase):

    def setUp(self):
        self.pipeline = ContextPipeline(
            sources=[],
            mode=MinimalMode(),
            compressor=StandardCompressor(),
            budget=TokenBudget(max_tokens=50),
            provider=MockProvider(),
            metrics=MetricsCollector()
        )

    def test_pipeline_execution(self):
        goal = "Summarize errors"
        # The run method is the synchronous fallback executing the async loop natively
        response = self.pipeline.run(goal)
        self.assertIn("mock response", response)
        self.assertGreater(self.pipeline.metrics.data.get("tokens_before", 0), 0)

    def test_semantic_compression(self):
        compressor = StandardCompressor()
        messages = [
            ContextItem(role="user", content="System Log Output:\n" + ("redundant error\n" * 5) + "```\n{ \"type\": \"json\" }\n```")
        ]
        out = compressor.compress(messages)
        self.assertEqual(out[0].content.count("redundant error"), 1)
        self.assertIn("```\n{ \"type\": \"json\" }\n```", out[0].content)

    def test_file_source_loading(self):
        from contextflow.sources import FileSource
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as f:
            f.write("Some mock log data please kindly ignore.")
            filepath = f.name
            
        try:
            source = FileSource([filepath])
            messages = source.load()
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].role, "system")
            self.assertIn("mock log data", messages[0].content)
        finally:
            os.remove(filepath)

    def test_distillation_compressor(self):
        import asyncio
        from contextflow.compression import DistillationCompressor
        from contextflow.provider import MockProvider
        compressor = DistillationCompressor(MockProvider(), overflow_threshold=10)
        messages = [
            ContextItem(role="user", content="This is a massive block of text that exceeds the limit.")
        ]
        compressed = asyncio.run(compressor.acompress(messages))
        self.assertIn("[DISTILLED CONTEXT]", compressed[0].content)

    def test_graph_context_bank(self):
        from contextflow.memory import GraphContextBank
        graph = GraphContextBank()
        graph.add_node("Goal", "Analyze the user.")
        graph.add_node("User", "Pradeep")
        graph.add_node("Age", "30")
        graph.add_edge("Goal", "User")
        graph.add_edge("User", "Age")
        
        source1 = graph.compile_source(["Goal"], max_depth=1)
        contents = " ".join(m.content for m in source1)
        self.assertIn("Pradeep", contents)
        self.assertNotIn("30", contents)

        source2 = graph.compile_source(["Goal"], max_depth=2)
        contents2 = " ".join(m.content for m in source2)
        self.assertIn("30", contents2)

    def test_native_cache(self):
        from contextflow.cache import NativeCache
        from contextflow.compression import DistillationCompressor
        from contextflow.provider import MockProvider
        
        cache = NativeCache()
        compressor = StandardCompressor()
        
        big_string = "a" * 1000
        item = ContextItem(role="system", content=f"```python\n{big_string}\n```")
        cached1 = cache.get_or_set(item, compressor)
        cached2 = cache.get_or_set(item, compressor)
        
        self.assertIs(cached1, cached2) 
        
        # Verify semantic context invalidates hash keys
        distill_50 = DistillationCompressor(MockProvider(), overflow_threshold=50)
        distill_100 = DistillationCompressor(MockProvider(), overflow_threshold=100)
        
        h_std = cache._hash(item, compressor)
        h_50 = cache._hash(item, distill_50)
        h_100 = cache._hash(item, distill_100)
        
        self.assertNotEqual(h_std, h_50)
        self.assertNotEqual(h_50, h_100) 

    def test_ranking_time_decay(self):
        from contextflow.ranking import ContextRanker, TimeDecayScorer
        ranker = ContextRanker(TimeDecayScorer(base_priority=50, decay_rate=5))
        messages = [
            ContextItem(role="user", content="oldest turn"),
            ContextItem(role="assistant", content="old reply"),
            ContextItem(role="user", content="newest turn")
        ]
        
        ranked = ranker.apply(messages)
        self.assertEqual(ranked[0].priority, 35) # Penalty 15
        self.assertEqual(ranked[2].priority, 45) # Penalty 5

    def test_context_session(self):
        from contextflow.session import ContextSession
        session = ContextSession(self.pipeline, system_prompt="Be a helpful bot")
        session.add_turn("user", "Hello there!")
        
        response = session.resolve_sync("Can you summarize our chat?")
        self.assertIn("mock response", response)
        self.assertEqual(len(session.history), 4)

if __name__ == '__main__':
    unittest.main()