import copy
from Action import Action
from State import State


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
        self.goals = []

    def init(self):
        remove_action = Action('remove')
        temp = ['at', self.tires[0], self.location[0]]
        remove_action.positive_precondition.append(temp)
        remove_action.delete_list.append(temp)
        temp1 = ['at',self.tires[0], self.ground]
        remove_action.add_list.append(temp1)
        self.all_actions.append(remove_action)

        remove_action = Action('remove')
        temp = ['at', self.tires[1], self.location[0]]
        remove_action.positive_precondition.append(temp)
        remove_action.delete_list.append(temp)
        temp1 = ['at', self.tires[1], self.ground]
        remove_action.add_list.append(temp1)
        self.all_actions.append(remove_action)

        remove_action = Action('remove')
        temp = ['at', self.tires[0], self.location[1]]
        remove_action.positive_precondition.append(temp)
        remove_action.delete_list.append(temp)
        temp1 = ['at', self.tires[0], self.ground]
        remove_action.add_list.append(temp1)
        self.all_actions.append(remove_action)

        remove_action = Action('remove')
        temp = ['at', self.tires[1], self.location[1]]
        remove_action.positive_precondition.append(temp)
        remove_action.delete_list.append(temp)
        temp1 = ['at', self.tires[1], self.ground]
        remove_action.add_list.append(temp1)
        self.all_actions.append(remove_action)

        putOn_action = Action('put on')
        temp = ['at', self.tires[0], self.ground]
        putOn_action.positive_precondition.append(temp)
        temp = ['at', self.tires[0], self.location[1]]
        putOn_action.negative_precondition.append(temp)
        temp = ['at', self.tires[0], self.ground]
        putOn_action.delete_list.append(temp)
        temp = ['at', self.tires[0], self.location[1]]
        putOn_action.add_list.append(temp)
        self.all_actions.append(putOn_action)

        putOn_action = Action('put on')
        temp = ['at', self.tires[1], self.ground]
        putOn_action.positive_precondition.append(temp)
        temp = ['at', self.tires[0], self.location[1]]
        putOn_action.negative_precondition.append(temp)
        temp = ['at', self.tires[1], self.ground]
        putOn_action.delete_list.append(temp)
        temp = ['at', self.tires[1], self.location[1]]
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

        temp = ['at', self.tires[1], self.location[1]]
        self.goals.append(temp)

    def is_applicable(self, state=State, action=Action):
        positive_precond_count = len(action.positive_precondition)
        for pos_precond in action.positive_precondition:
            if pos_precond in state.positive_literals:
                positive_precond_count -= 1
        return positive_precond_count == 0

    def goal_test(self, state):
        size = len(state.positive_literals)
        goal_count = len(self.goals)
        count = 0
        for goal in self.goals:
            for i in range(0, size):
                if goal == state.positive_literals[i] and goal not in state.negative_literals:
                    count += 1
                elif (state.positive_literals[i][1] == 'obj' and state.positive_literals[i][2]==goal[2]) \
                        or (state.positive_literals[i][2] == 'loc' and state.positive_literals[i][1] == goal[1]):
                    count += 1
        if goal_count == count:
            print("finished")
            self.print_action(state)
            return True
        else:
            return False

    def print_action(self, state):
        if state is None:
            return
        print(state.action)
        self.print_action(state.parent)

    def ignore_preconditions(self, state=State):
        all_states = [state]
        start = 0

        for st in all_states:
            for action in self.all_actions:
                new_state = State(st, action)
                new_state.positive_literals.extend(action.add_list)
                new_state.negative_literals.extend(action.delete_list)

                if st is not None:
                    new_state.positive_literals.extend(st.positive_literals)
                    new_state.negative_literals.extend(st.negative_literals)
                if start == 0:
                    new_state.positive_literals.extend(state.positive_literals)
                if self.goal_test(new_state):
                    return

                all_states.append(new_state)
                start += 1

                temp = None
            new_state = None

    def ignore_delete_list(self, state):
        all_states = [state]
        start = 0

        for st in all_states:
            for action in self.all_actions:
                if self.is_applicable(st, action):
                    new_state = State(st, action)
                    new_state.positive_literals.extend(action.add_list)
                    new_state.negative_literals.extend(action.delete_list)
                    same_element = set(map(tuple, new_state.positive_literals)) & set(
                        map(tuple, new_state.negative_literals))
                    if len(same_element) > 0:
                        new_state.positive_literals.remove(same_element)
                    if st is not None:
                        new_state.positive_literals.extend(st.positive_literals)
                        new_state.negative_literals.extend(st.negative_literals)
                    if start == 0:
                        new_state.positive_literals.extend(state.positive_literals)
                    if self.goal_test(new_state):
                        print("YES")
                        return
                    all_states.append(new_state)
                    start += 1

    def forward(self):
        self.init()
        actions_list = []
        current_state = State(None, None)

        temp = ['at', self.tires[0], self.location[1]]
        current_state.positive_literals.append(temp)
        temp = ['at', self.tires[1], self.location[0]]
        current_state.positive_literals.append(temp)

        if self.mode == 'precond':
            self.ignore_preconditions(current_state)
        elif self.mode == 'delete-list':
            self.ignore_delete_list(current_state)

        # TODO: implement ignore_delete_list

        # for action in self.all_actions:
        #     print(possible_action(action, s0))
