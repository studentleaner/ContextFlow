
class TokenBudget:

    def __init__(self, max_tokens):
        self.max_tokens = max_tokens

    def fit(self, messages):
        return messages[-self.max_tokens:]
