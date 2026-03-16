
class ContextPipeline:

    def __init__(self, sources, mode, compressor, provider):
        self.sources = sources
        self.mode = mode
        self.compressor = compressor
        self.provider = provider

    def run(self, goal):

        messages = []

        for s in self.sources:
            messages.extend(s.load())

        messages.append({
            "role": "user",
            "content": goal,
        })

        messages = self.mode.select(messages)

        messages = self.compressor.compress(messages)

        return self.provider.chat(messages)
