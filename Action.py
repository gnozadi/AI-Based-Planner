class Action:

    def __init__(self, name):
        self.name = name
        self.negative_precondition = []
        self.positive_precondition = []
        self.add_list = []
        self.delete_list = []

    def set_preconditions(self, negative_precond, positive_precond):
        self.negative_precondition = negative_precond
        self.positive_precondition = positive_precond

    def set_effects(self, positive_effect, negative_effect):
        self.add_list = positive_effect
        self.delete_list = negative_effect

    def __str__(self):
        return "name " + self.name + \
               " - precond " + self.negative_precondition.__str__() +\
               " + precond " + self.positive_precondition.__str__() + \
               " add list " + self.add_list.__str__() +\
               "delete list " + self.delete_list.__str__()
