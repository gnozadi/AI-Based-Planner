from Action import Action
from State import State


class SpareTire:
    tires = ['flat', 'spare']
    location = ['trunk', 'axle']
    all_actions = []
    initial_state = State(None, None)

    def __init__(self):
        # TODO: what if I put object and location
        #  used in defining preconditions and effects
        #  inside the following lists?

        self.initial_state.positive_literals.add(self.tires[0] + 'at' + self.location[1])
        self.initial_state.positive_literals.add(self.tires[1] + 'at' + self.location[0])

        remove_action = Action('remove')
        remove_action.positive_precondition.add('obj'+'at'+'loc')
        remove_action.add_list.add('obj'+'at'+'Ground')
        remove_action.delete_list.add('obj'+'at'+'loc')
        self.all_actions.add(remove_action)

        putOn_action = Action('putOn')
        putOn_action.positive_precondition.add('obj'+'at'+'Ground')

