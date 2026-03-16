
class Config:

    def __init__(self, data):
        self.data = data

    def get(self, key, default=None):
        return self.data.get(key, default)
