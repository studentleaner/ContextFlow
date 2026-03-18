import unittest
import os
from contextflow.budget import TokenBudget
from contextflow.pipeline import ContextPipeline
from contextflow.mode import MinimalMode
from contextflow.compression import StandardCompressor
from contextflow.provider import MockProvider
from contextflow.metrics import MetricsCollector
from contextflow.schema import ContextItem

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
        from contextflow.compression import DistillationCompressor
        from contextflow.provider import MockProvider
        compressor = DistillationCompressor(MockProvider(), overflow_threshold=10)
        messages = [
            ContextItem(role="user", content="This is a massive block of text that exceeds the limit.")
        ]
        compressed = compressor.compress(messages)
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

if __name__ == '__main__':
    unittest.main()