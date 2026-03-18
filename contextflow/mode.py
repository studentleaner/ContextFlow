
class MinimalMode:
    def select(self, messages):
        return messages[-5:]


class FullMode:
    def select(self, messages):
        return messages
 