
class State:

    def __init__(self, state, parent, move, depth, key):

        self.state = state

        self.parent = parent

        self.move = move

        self.depth = depth

        self.key = key

        if self.state:
            self.map = ''.join(str(e) for e in self.state)

        if 1 <= self.parent <= 6:
            self.cost = 1
        elif 7 <= self.parent <= 16:
            self.cost = 3
        else:
            self.cost = 15

    def __eq__(self, other):
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map


