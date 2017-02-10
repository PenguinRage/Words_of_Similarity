import bisect


class DFA(object):
    def __init__(self, start_state):
        self.start_state = start_state
        self.transitions = {}
        self.defaults = {}
        self.final_states = set()

    def add_transition(self, src, input, dest):
        self.transitions.setdefault(src, {})[input] = dest

    def set_default_transition(self, src, dest):
        self.defaults[src] = dest

    def add_final_state(self, state):
        self.final_states.add(state)

    def is_final(self, state):
        return state in self.final_states

    def next_state(self, src, input):
        state_transitions = self.transitions.get(src, {})
        return state_transitions.get(input, self.defaults.get(src, None))

    def next_valid_string(self, input):
        state = self.start_state
        stack = []

        # Evaluate the DFA as far as possible
        for i, x in enumerate(input):
            stack.append((input[:i], state, x))
            state = self.next_state(state, x)
            if not state: break
        else:
            stack.append((input[:i + 1], state, None))

        if self.is_final(state):
            # Input word is already valid
            return input

        # Perform a 'wall following' search for the lexicographically smallest
        # accepting state.
        while stack:
            path, state, x = stack.pop()
            x = self.find_next_edge(state, x)
            if x:
                path += x
                state = self.next_state(state, x)
                if self.is_final(state):
                    return path
                stack.append((path, state, None))
        return None

    def find_next_edge(self, s, x):
        if x is None:
            x = u'\0'
        else:
            x = chr(ord(x) + 1)
        state_transitions = self.transitions.get(s, {})
        if x in state_transitions or s in self.defaults:
            return x
        labels = sorted(state_transitions.keys())
        pos = bisect.bisect_left(labels, x)
        if pos < len(labels):
            return labels[pos]
        return None
