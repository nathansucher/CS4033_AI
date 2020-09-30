import time
import sys
from copy import deepcopy

""" PriorityQueue structure
This will be used as the open_list for the breadth first search to hold StateNodes of possible moves
"""


class PriorityQueue(object):
    # PriorityQueue constructor
    def __init__(self):
        self.queue = []

    def getLength(self):  # Gets length of queue
        return len(self.queue)

    def isEmpty(self):  # Checks to see if queue is empty
        return len(self.queue) == []

    def insertValue(self, data):  # Enqueue data into queue
        self.queue.append(data)

    def getValue(self):  # Dequeue data from queue based on priority
        try:
            min = 0
            for i in range(len(self.queue)):
                if self.queue[i].priority < self.queue[min].priority and self.queue[i].depth <= self.queue[min].depth:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except:
            pass


""" StateNode structure
This structure represents a "state" or possible move from the previous StateNode that the search methods will use
to look for goal_state
"""


class State(object):
    stateID = 0
    parentID = 0
    g = 0
    f = g
    moves = []
    depth = 0

    rows = 6
    columns = 3

    def __init__(self, puzzleBoard, stateID, parentID, parent, g, move):
        self.puzzleBoard = puzzleBoard
        self.stateID = stateID
        self.parentID = parentID
        self.g = g
        self.priority = g

        if move == 1:
            self.move = "Up"
        elif move == 2:
            self.move = "Down"
        elif move == 3:
            self.move = "Right"
        elif move == 4:
            self.move = "Left"
        else:
            self.move = move

        self.parent = parent
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1
            self.moves = deepcopy(parent.moves)
            self.moves.append(self.move)

    def display_stats(self):
        print(f'\n======== State {str(self.stateID)} ========')
        print("State ID: " + str(self.stateID))
        print("Parent State ID: " + str(self.parentID))
        print("Depth: " + str(self.depth))
        print("Cost: " + str(self.priority))
        print("Last Move: " + str(self.move))
        print("Moves: " + str(self.moves))

    def getZeroLocation(self, board):
        for x in range(len(board)):
            try:
                if board[x].index(0) == 0 or board[x].index(0) == 1 or board[x].index(0) == 2:
                    zeroLocation = (x, board[x].index(0))
                    return zeroLocation
            except:
                continue
        return None

    def moveTiles(self, closedList, puzzleBoard):
        moves = PriorityQueue()
        state_id = self.stateID + 1
        for direction in range(1, 5):
            currentNode = deepcopy(self)
            tempBoard = deepcopy(puzzleBoard)
            zeroLocation = self.getZeroLocation(puzzleBoard)

            # Moving up
            if direction == 1:
                if zeroLocation[0] != 0:
                    calculatedQ = tempBoard[zeroLocation[0] - 1][zeroLocation[1]]
                    tempBoard[zeroLocation[0] - 1][zeroLocation[1]] = tempBoard[zeroLocation[0]][zeroLocation[1]]
                    tempBoard[zeroLocation[0]][zeroLocation[1]] = calculatedQ
            # Moving down
            elif direction == 2:
                if zeroLocation[0] != self.rows - 1:
                    calculatedQ = tempBoard[zeroLocation[0] + 1][zeroLocation[1]]
                    tempBoard[zeroLocation[0] + 1][zeroLocation[1]] = tempBoard[zeroLocation[0]][zeroLocation[1]]
                    tempBoard[zeroLocation[0]][zeroLocation[1]] = calculatedQ
            # Moving right
            elif direction == 3:
                if zeroLocation[1] != self.columns - 1:
                    calculatedQ = tempBoard[zeroLocation[0]][zeroLocation[1] + 1]
                    tempBoard[zeroLocation[0]][zeroLocation[1] + 1] = tempBoard[zeroLocation[0]][zeroLocation[1]]
                    tempBoard[zeroLocation[0]][zeroLocation[1]] = calculatedQ
            # Moving left
            elif direction == 4:
                if zeroLocation[1] != 0:
                    calculatedQ = tempBoard[zeroLocation[0]][zeroLocation[1] - 1]
                    tempBoard[zeroLocation[0]][zeroLocation[1] - 1] = tempBoard[zeroLocation[0]][zeroLocation[1]]
                    tempBoard[zeroLocation[0]][zeroLocation[1]] = calculatedQ

            if self.getZeroLocation(tempBoard) is not self.getZeroLocation(puzzleBoard):
                if 1 <= calculatedQ <= 6:
                    cost = currentNode.priority + 1
                elif 7 <= calculatedQ <= 16:
                    cost = currentNode.priority + 3
                else:
                    cost = currentNode.priority + 15

                if tempBoard not in closedList:
                    newNode = State(tempBoard, state_id, self.stateID, currentNode, cost, direction)
                    moves.insertValue(newNode)
                    state_id += 1
                    del newNode

        return moves



class Solver(object):
    # Creating the size of the puzzle (this one is a 3x6 board)
    rows = 6
    columns = 3

    def __init__(self, startStateInput, goalStateInput):
        self.startState = startStateInput
        self.goalState = goalStateInput
        self.puzzleBoard = []
        self.goalPuzzleBoard = []

        self.number_of_steps = 0
        self.nodes_generated = 0

        self.createBoards()

        self.startNode = State(self.puzzleBoard, 1, None, None, 0, " ")

    def createBoards(self):
        value = 0
        for x in range(self.rows):
            self.puzzleBoard.append([])
            self.goalPuzzleBoard.append([])
            for y in range(self.columns):
                self.puzzleBoard[x].append(self.startState[value])
                self.goalPuzzleBoard[x].append(self.goalState[value])
                value = value + 1

    def compareBoard(self, puzzleBoard):
        for i in range(self.rows):
            for j in range(self.columns):
                if puzzleBoard[i][j] != self.goalPuzzleBoard[i][j]:
                    return 0
        return 1

    def bfs(self):
        start = time.time()
        closedList = list()
        openList = PriorityQueue()

        openList.insertValue(self.startNode)
        cur_time = time.time()
        while True:
            if openList.isEmpty():
                return None

            currentState = openList.getValue()
            currentState.display_stats()

            if self.compareBoard(currentState.puzzleBoard):

                end = time.time()
                print("\n\n\n")
                print('\n======== Goal State Found! ========')
                print("Number of steps: ", self.number_of_steps)
                print("Open List Size: ", openList.getLength())
                print("Closed List Size: ", len(closedList))
                print("Elapsed Time (sec): ", end - start)
                print("Path:")
                currentState.display_stats()

                parentState = currentState.parent
                while parentState:
                    parentState.display_stats()
                    parentState = parentState.parent
                return 0

            elif currentState.puzzleBoard not in closedList:

                closedList.append(self.puzzleBoard)
                moves = currentState.moveTiles(closedList, self.puzzleBoard)
                for x in range(moves.getLength()):

                    self.nodes_generated = self.nodes_generated + 1
                    openList.insertValue(moves.getValue())

            self.number_of_steps = self.number_of_steps + 1
            cur_time = time.time()


def parse_input(input_string):
    parsed_vector = []

    str_array = input_string.split(' ')
    for x in str_array:
        if x != ' ':
            parsed_vector.append(int(x))

    return parsed_vector


if __name__ == "__main__":
    if len(sys.argv) > 2:  # User entered arguments
        start_state_input = sys.argv[1]
        goal_state_input = sys.argv[2]
    elif len(sys.argv) > 1 and sys.argv[1] == '1':
        # Start/Goal state input vector - use case c)i)
        start_state_input = '1 13 3 5 6 9 11 0 8 12 14 10 7 16 15 4 17 2'
        goal_state_input = '1 13 3 5 6 9 11 14 8 12 16 10 7 17 15 0 4 2'
    elif len(sys.argv) > 1 and sys.argv[1] == '2':
        # Start/Goal state input vector - use case c)ii)
        start_state_input = '1 13 3 5 17 9 11 0 8 12 14 10 7 16 15 4 6 2'
        goal_state_input = '5 1 3 13 17 9 11 0 8 12 14 10 7 16 15 4 6 2'
    else:  # Default
        # Start/Goal state input vector - use case c)i)
        start_state_input = '1 13 3 5 6 9 11 0 8 12 14 10 7 16 15 4 17 2'
        goal_state_input = '1 13 3 5 6 9 11 14 8 12 16 10 7 17 15 0 4 2'

    # Get parsed input arrays from input vectors
    start_state_array = parse_input(start_state_input)
    goal_state_array = parse_input(goal_state_input)

    # Create board object using start/goal states
    solver = Solver(start_state_array, goal_state_array)
    solver.bfs()

    # Creates search object with the created board as the input

    # Breadth First Search performed



