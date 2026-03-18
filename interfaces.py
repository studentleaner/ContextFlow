
class ContextSource:
    def load(self):
        raise NotImplementedError


class ContextMode:
    def select(self, messages):
        raise NotImplementedError


class Compressor:
    def compress(self, messages):
        raise NotImplementedError


class Provider:
    def chat(self, messages):
        raise NotImplementedError 
