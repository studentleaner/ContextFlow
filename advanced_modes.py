
class InvestigationMode:
    def select(self, messages):
        return [m for m in messages if m.get("type") in ["goal","memory","hop"]]


class AgentMode:
    def select(self, messages):
        return messages[-10:]
