from Action import Action
from State import State
from SpareTire import SpareTire


def is_relevant(state, add_list, delete_list):
    count = 0
    total = len(delete_list) + len(add_list)
    for pos in add_list:
        for pos_effect in state.positive_literals:
            if pos == pos_effect:
                count += 1
    for neg in delete_list:
        for neg_effect in state.negative_literals:
            if neg == neg_effect:
                count += 1
    if count > 0:
        return True
    else:
        return False

class block:

    def __init__(self, size):
        self.size = size
        self.blocks = []
        self.on = []
        self.under = []
        [self.blocks.append(chr(x)) for x in range(65, size + 65)]
        [self.on.append(chr(x)) for x in range(65, size + 65)]
        [self.under.append(chr(x)) for x in range(65, size + 65)]
        self.on.insert(0, 'clear')
        self.blocks.insert(0, 'table')
        self.all_actions = []
        self.goals = []
        self.init_state = State(None, None)

    def init(self):

        for b in self.blocks:
            for y in self.blocks:
                if b != y and b != self.blocks[0] and y != self.blocks[0]:
                    move_action = Action('move')
                    temp = ['on', b, 'table']
                    move_action.positive_precondition.append(temp)
                    temp = ['on', b, self.on[0]]
                    move_action.positive_precondition.append(temp)
                    temp = ['on', y, self.on[0]]
                    move_action.positive_precondition.append(temp)
                    temp = ['on', b, y]
                    move_action.add_list.append(temp)
                    temp = ['on', self.blocks[0], self.on[0]]
                    move_action.add_list.append(temp)
                    temp = ['on', b, self.on[0]]
                    move_action.delete_list.append(temp)
                    temp = ['on', y, self.on[0]]
                    move_action.delete_list.append(temp)
                    self.all_actions.append(move_action)

        for b in self.blocks:
            for x in self.blocks:
                if b != x and b != 'table' and x != 'table':
                    move_to_table = Action('move to table')
                    temp = ['on', b, x]
                    move_to_table.positive_precondition.append(temp)
                    temp = ['on', b, self.on[0]]
                    move_to_table.positive_precondition.append(temp)
                    temp = ['on', b, self.under[0]]
                    move_to_table.add_list.append(temp)
                    temp = ['on', x, self.on[0]]
                    move_to_table.add_list.append(temp)
                    temp = ['on', b, x]
                    move_to_table.delete_list.append(temp)
                    self.all_actions.append(move_to_table)

        for i in range(1, self.size):
            temp = ['on', self.blocks[i], self.blocks[i + 1]]
            self.goals.append(temp)

        temp = ['on', self.blocks[-1], self.blocks[1]]
        self.init_state.positive_literals.append(temp)
        temp = ['on', self.blocks[-1], self.on[0]]
        self.init_state.positive_literals.append(temp)

        for i in range(1, self.size):
            if i != 1:
                temp = ['on', self.blocks[i], self.on[0]]
                self.init_state.positive_literals.append(temp)

            temp = ['on', self.blocks[i], self.blocks[0]]
            self.init_state.positive_literals.append(temp)

    def ignore_preconditions(self, ):
        all_states = [self.init_state]
        start = 0

        for st in all_states:
            for action in self.all_actions:
                new_state = State(st, action)
                new_state.positive_literals.extend(action.add_list)
                new_state.negative_literals.extend(action.delete_list)

                intersection = [list(x) for x in set(tuple(x) for x in new_state.positive_literals).intersection(
                    set(tuple(x) for x in new_state.negative_literals))]
                sub = [x for x in new_state.positive_literals if x not in intersection]
                new_state.positive_literals = sub

                if st is not None:
                    new_state.positive_literals.extend(st.positive_literals)
                    new_state.negative_literals.extend(st.negative_literals)

                if self.goal_test(new_state):
                    print(action)
                    return

                all_states.append(new_state)
                start += 1

                temp = None
            new_state = None

    def goal_test(self, state):
        size = len(state.positive_literals)
        goal_count = len(self.goals)

        count = 0
        for goal in self.goals:
            for i in range(0, size):
                if goal == state.positive_literals[i] and goal not in state.negative_literals:
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

    def is_applicable(self, state=State, action=Action):
        positive_precond_count = len(action.positive_precondition)
        for pos_precond in action.positive_precondition:
            if pos_precond in state.positive_literals:
                positive_precond_count -= 1
        return positive_precond_count == 0

    def ignore_delete_list(self, state):
        all_states = [state]
        start = 0

        for st in all_states:
            for action in self.all_actions:
                if self.is_applicable(st, action):
                    new_state = State(st, action)
                    new_state.positive_literals.extend(action.add_list)
                    new_state.negative_literals.extend(action.delete_list)
                    # same_element = set(map(tuple, new_state.positive_literals)) & set(
                    #     map(tuple, new_state.negative_literals))
                    # if len(same_element) > 0:
                    #     new_state.positive_literals.remove(same_element)
                    if st is not None:
                        new_state.positive_literals.extend(st.positive_literals)
                        new_state.negative_literals.extend(st.negative_literals)
                    if start == 0:
                        new_state.positive_literals.extend(state.positive_literals)
                    if self.goal_test(new_state):
                        return
                    all_states.append(new_state)
                    start += 1


    def init_test(self, state, init_state):
        count = 0
        size = len(init_state.positive_literals)
        for pos in init_state.positive_literals:
            if pos in state.positive_literals:
                count += 1
        return count == size

    def backward(self, init_state):

        state = State(None, None)
        state.positive_literals.extend(self.goals)
        all_states = [state]

        for state in all_states:
            for action in self.all_actions:
                # print(action)
                if is_relevant(state, action.add_list, action.delete_list):

                    res = []
                    temp_state = State(state, action)

                    intersection1 = [list(x) for x in set(tuple(x) for x in state.positive_literals).intersection(
                        set(tuple(x) for x in action.add_list))]
                    sub1 = [x for x in state.positive_literals if x not in intersection1]
                    temp_state.positive_literals = sub1 + action.positive_precondition

                    [res.append(x) for x in temp_state.positive_literals if x not in res]
                    temp_state.positive_literals = (res)

                    res = []

                    intersection2 = [list(x) for x in set(tuple(x) for x in state.negative_literals).intersection(
                        set(tuple(x) for x in action.delete_list))]
                    sub2 = [x for x in state.negative_literals if x not in intersection2]

                    res = sub2 + action.negative_precondition
                    [res.append(x) for x in temp_state.negative_literals if x not in res]
                    temp_state.negative_literals = res

                    all_states.append(temp_state)

                    if self.init_test(temp_state, init_state):
                        print('FOUND')
                        self.print_action(temp_state)
                        return


if __name__ == '__main__':
    bl = block(3)
    bl.init()

    bl.backward(bl.init_state)
