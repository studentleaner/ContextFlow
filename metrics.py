
class MetricsCollector:

    def __init__(self):
        self.data = {}

    def record(self, key, value):
        self.data[key] = value
