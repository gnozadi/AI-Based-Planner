from Action import Action


class State:
    def __init__(self, parent, action=Action):
        self.parent = parent
        self.action = action
        self.positive_literals = []
        self.negative_literals = []
        self.hash_value = None
        # TODO: what should hash_value be?

    def __str__(self):
        return "(parent " + self.parent.__str__() + ") " + \
               " - literals " + self.negative_literals.__str__() + \
               " + literals " + self.positive_literals.__str__() + \
               " action" + self.action.__str__()
