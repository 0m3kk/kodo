class ShortTermMemory:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history = []

    def get_history(self):
        return self.history

    def add_entry(self, data):
        self.history.append(data)
