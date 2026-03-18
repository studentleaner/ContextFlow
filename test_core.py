import unittest
from budget import TokenBudget
from pipeline import ContextPipeline
from mode import MinimalMode
from compression import StandardCompressor
from provider import MockProvider
from metrics import MetricsCollector

class TestContextFlow(unittest.TestCase):

    def test_budget_array_truncation(self):
        budget = TokenBudget(max_tokens=20)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "This is an old long message we should probably drop."},
            {"role": "user", "content": "This is a new short message."}
        ]
        
        # total tokens roughly: system(5) + old(10) + new(6) = 21 > 20
        # should pop index 1
        fitted = budget.fit(messages)
        self.assertEqual(len(fitted), 2)
        self.assertEqual(fitted[1]["content"], "This is a new short message.")

    def test_budget_string_truncation(self):
        # Only 2 messages, but exceeds budget. Expected to slice the string.
        budget = TokenBudget(max_tokens=5)
        messages = [
            {"role": "system", "content": "System"},
            {"role": "user", "content": "This is a very long string that should be cut."}
        ]
        fitted = budget.fit(messages)
        self.assertEqual(len(fitted), 2)
        self.assertTrue(len(budget.encoder.encode(fitted[1]["content"])) <= 5)

    def test_pipeline_execution(self):
        metrics = MetricsCollector()
        pipeline = ContextPipeline(
            sources=[],
            mode=MinimalMode(),
            compressor=StandardCompressor(),
            provider=MockProvider(),
            budget=TokenBudget(max_tokens=100),
            metrics=metrics
        )
        
        res = pipeline.run("Test query")
        self.assertEqual(res, "mock response")
        self.assertTrue("latency_ms" in metrics.data)
        self.assertTrue("tokens_after" in metrics.data)

    def test_semantic_compression(self):
        compressor = StandardCompressor()
        messages = [
            {"role": "user", "content": "Here is a code block:\n```json\n{\n  \"key\": \"value\"\n}\n```\nAnd a loose object: { \"test\": 123 }\nplease kindly ignore filler."}
        ]
        compressed = compressor.compress(messages)
        content = compressed[0]["content"]
        
        # Exact markdown code block and exact json dict bracket string should remain perfectly untouched
        self.assertIn("```json\n{\n  \"key\": \"value\"\n}\n```", content)
        self.assertIn("{ \"test\": 123 }", content) 
        # Deterministic padding should vanish 
        self.assertNotIn("please kindly", content)

    def test_file_source_loading(self):
        from sources import FileSource
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("System Log: OOM Error occurred")
            filepath = f.name
            
        try:
            source = FileSource(filepath)
            data = source.load()
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["role"], "user")
            self.assertIn("OOM Error", data[0]["content"])
        finally:
            os.remove(filepath)

if __name__ == '__main__':
    unittest.main()
 