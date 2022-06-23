import copy
from Action import Action
from State import State


def possible_action(action, state):
    print(action.name)

    for pp in action.positive_precondition:
        print(pp)
        print(state.positive_literals)
        if pp in state.positive_literals:
            return True

    return False


class SpareTire:
    ground = 'ground'

    def __init__(self, mode):
        # TODO: what if I put object(obj) and location(loc)
        #  used in defining preconditions and effects
        #  inside the following lists?
        self.tires = ['flat', 'spare']
        self.location = ['trunk', 'axle']
        self.all_actions = []
        self.mode = mode
        # TODO: goal?

    def define_actions(self):
        remove_action = Action('remove')
        temp = ['at', 'obj', 'loc']
        remove_action.positive_precondition.append(temp)
        temp = ['at', 'obj', self.ground]
        remove_action.delete_list.append(temp)
        self.all_actions.append(remove_action)

        putOn_action = Action('put on')
        temp = ['at', 'obj', self.ground]
        putOn_action.positive_precondition.append(temp)
        temp = ['at', self.tires[0], self.location[1]]
        putOn_action.negative_precondition.append(temp)
        temp = ['at', 't', self.ground]
        putOn_action.delete_list.append(temp)
        temp = ['at', 't', self.location[1]]
        putOn_action.add_list.append(temp)
        self.all_actions.append(putOn_action)

        leaveOvernight_action = Action('Leave overnight')
        temp = ['at', self.tires[1], self.ground]
        leaveOvernight_action.delete_list.append(temp)
        temp = ['at', self.tires[1], self.location[1]]
        leaveOvernight_action.delete_list.append(temp)
        temp = ['at', self.tires[1], self.location[0]]
        leaveOvernight_action.delete_list.append(temp)
        temp = ['at', self.tires[0], self.ground]
        leaveOvernight_action.delete_list.append(temp)
        temp = ['at', self.tires[0], self.location[1]]
        leaveOvernight_action.delete_list.append(temp)
        temp = ['at', self.tires[0], self.location[0]]
        leaveOvernight_action.delete_list.append(temp)
        self.all_actions.append(leaveOvernight_action)

    def ignore_preconditions(self, state):
        all_states = [state]
        i = 0
        for st in all_states:
            if i > 3:
                return None
            for action in self.all_actions:
                new_state = State(st, action)
                new_state.positive_literals.append(action.add_list)
                new_state.negative_literals.append(action.delete_list)
                print(new_state)
                all_states.append(new_state)
                temp = None
            new_state = None
            i += 1


    def forward(self):
        self.define_actions()
        actions_list = []
        current_state = State(None, None)
        s0 = State(None, None)
        temp = ['at', self.tires[0], self.location[1]]
        s0.positive_literals.append(temp)
        temp = ['at', self.tires[1], self.location[0]]
        s0.positive_literals.append(temp)

        if self.mode == 'precond':
            self.ignore_preconditions(current_state)

        #TODO: implement ignore_delete_list

        # for action in self.all_actions:
        #     print(possible_action(action, s0))
