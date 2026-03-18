import os

class MockProvider:
    def chat(self, messages):
        return "mock response"

class OpenAIProvider:
    def __init__(self, model="gpt-4o"):
        import openai
        self.model = model
        # Initialize client. Requires OPENAI_API_KEY to be set in local environment.
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def chat(self, messages):
        # Format map mapping our pipeline dictionaries direct to the official OpenAI schema
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
