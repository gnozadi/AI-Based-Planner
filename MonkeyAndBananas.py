from Action import Action
from State import State


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


def init_test(state, init_state):
    count = 0
    size = len(init_state.positive_literals)
    for pos in init_state.positive_literals:
        if pos in state.positive_literals:
            count += 1
    return count == size


class MonkeyAndBananas:

    def __init__(self):
        self.items = ['monkey', 'banana', 'box']
        self.positions = ['A', 'B', 'C']
        self.height = ['low', 'high']
        self.all_actions = []
        self.goals = []
        self.init_state = State(None, None)

    def init(self):

        for x in self.positions:
            for y in self.positions:
                if x != y:
                    go = Action('go from ' + x + ' to ' + y)
                    temp = ['at', self.items[0], x]
                    go.positive_precondition.append(temp)
                    temp = ['atHeight', self.items[0], self.height[0]]
                    go.positive_precondition.append(temp)
                    temp = ['at', self.items[0], y]
                    go.add_list.append(temp)
                    temp = ['at', self.items[0], x]
                    go.delete_list.append(temp)

        for x in self.positions:
            for y in self.positions:
                if x != y:
                    push = Action('push box from ' + x + ' to ' + y)
                    temp = ['at', self.items[0], x]
                    push.positive_precondition.append(temp)
                    temp = ['atHeight', self.items[0], self.height[0]]
                    push.positive_precondition.append(temp)
                    temp = ['at', self.items[2], x]
                    push.positive_precondition.append(temp)
                    temp = ['atHeight', self.items[2], self.height[0]]
                    push.positive_precondition.append(temp)

                    temp = ['at', self.items[2], y]
                    push.add_list.append(temp)
                    temp = ['at', self.items[0], y]
                    push.add_list.append(temp)
                    temp = ['at', self.items[2], x]
                    push.delete_list.append(temp)
                    temp = ['at', self.items[0], x]
                    push.delete_list.append(temp)
                    self.all_actions.append(push)

        for x in self.positions:
            climb_up = Action('Climb Up box in ' + x)
            temp = ['at', self.items[0], x]
            climb_up.positive_precondition.append(temp)
            temp = ['atHeight', self.items[0], self.height[0]]
            climb_up.positive_precondition.append(temp)
            temp = ['at', self.items[2], x]
            climb_up.positive_precondition.append(temp)
            temp = ['atHeight', self.items[2], self.height[0]]
            climb_up.positive_precondition.append(temp)

            temp = ['at', self.items[0], self.items[2]]
            climb_up.add_list.append(temp)
            temp = ['atHeight', self.items[0], self.height[0]]
            climb_up.delete_list.append(temp)
            temp = ['atHeight', self.items[0], self.height[1]]
            climb_up.add_list.append(temp)
            self.all_actions.append(climb_up)

        for x in self.positions:
            for h in self.height:
                grasp = Action('grasp banana from ' + x + ' in level ' + h)
                temp = ['at', self.items[0], x]
                grasp.positive_precondition.append(temp)
                temp = ['atHeight', self.items[0], h]
                grasp.positive_precondition.append(temp)
                temp = ['at', self.items[1], x]
                grasp.positive_precondition.append(temp)
                temp = ['atHeight', self.items[1], h]
                grasp.positive_precondition.append(temp)

                temp = ['have', self.items[0], self.items[1]]
                grasp.add_list.append(temp)
                temp = ['at', self.items[1], x]
                grasp.delete_list.append(temp)
                temp = ['atHeight', self.items[1], h]
                grasp.delete_list.append(temp)
                self.all_actions.append(grasp)

        temp = ['at', self.items[0], self.positions[0]]
        self.init_state.positive_literals.append(temp)
        temp = ['at', self.items[1], self.positions[1]]
        self.init_state.positive_literals.append(temp)
        temp = ['at', self.items[2], self.positions[2]]
        self.init_state.positive_literals.append(temp)
        temp = ['atHeight', self.items[0], self.height[0]]
        self.init_state.positive_literals.append(temp)
        temp = ['atHeight', self.items[2], self.height[0]]
        self.init_state.positive_literals.append(temp)
        temp = ['atHeight', self.items[1], self.height[1]]
        self.init_state.positive_literals.append(temp)

        temp = ['have', self.items[0], self.items[1]]
        self.goals.append(temp)

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

    def ignore_delete_list(self):
        all_states = [self.init_state]
        start = 0
        print(len(self.all_actions))
        for st in all_states:
            for action in self.all_actions:
                if self.is_applicable(st, action):
                    print("HI")
                    new_state = State(st, action)
                    new_state.positive_literals.extend(action.add_list)
                    new_state.negative_literals.extend(action.delete_list)

                    if st is not None:
                        new_state.positive_literals.extend(st.positive_literals)
                        new_state.negative_literals.extend(st.negative_literals)
                    if start == 0:
                        new_state.positive_literals.extend(self.init_state.positive_literals)
                    if self.goal_test(new_state):
                        return
                    all_states.append(new_state)
                    start += 1

    def backward(self, init_state):
        state = State(None, None)
        state.positive_literals.extend(self.goals)
        all_states = [state]

        for state in all_states:
            for action in self.all_actions:

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

                    if init_test(temp_state, init_state):
                        print('FOUND')
                        self.print_action(temp_state)
                        return


if __name__ == '__main__':
    mb = MonkeyAndBananas()
    mb.init()
    # mb.ignore_preconditions()
    mb.ignore_delete_list()
    # mb.backward(mb.init_state)
