class State:
    def __init__(self, parent, action):
        self.parent = parent
        self.action = action
        self.positive_literals = []
        self.negative_literals = []
        self.hash_value = None
        # TODO: what should hash_value be?


