
class AgentRunner:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self, goal):
        return self.pipeline.run(goal) 
