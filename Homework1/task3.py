import argparse
from copy import deepcopy
import time


# Priority Queue class
class PriorityQueue(object):
    # Initializing the class
    def __init__(self):
        self.queue = []

    # Insert (Enqueue) data into the queue
    def insertValue(self, data):
        self.queue.append(data)

    # Retrieve the data from the queue. Data with the lowest f value and depth are retrieved first
    def getValue(self):
        try:
            min = 0
            for i in range(len(self.queue)):
                if self.queue[i].f < self.queue[min].f:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except:
            pass


# State class for each move
class State(object):
    rows = 6
    columns = 3
    f = 0
    h = 0

    # Initialize the State class
    def __init__(self, puzzleBoard, stateID, parentID, parentNode, g, move):
        self.puzzleBoard = puzzleBoard
        self.ID = stateID
        self.parentID = parentID
        self.parentNode = parentNode
        self.g = g
        self.depth = 0
        self.moves = []

        # Replaces a number representing a move with a string
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

        # Sets depth based on parent node depth and transfers moves
        if parentNode is None:
            self.depth = 0
        else:
            self.depth = parentNode.depth + 1
            self.moves = parentNode.moves.copy()
            self.moves.append(self.move)

    # Finds the location for zero in the puzzle board
    def getZeroLocation(self, board):
        for x in range(len(board)):
            try:
                if board[x].index(0) == 0 or board[x].index(0) == 1 or board[x].index(0) == 2:
                    zeroLocation = (x, board[x].index(0))
                    return zeroLocation
            except:
                continue
        return None

    # Moves a tile on the board
    def moveTiles(self, closedList, puzzleBoard):
        moves = PriorityQueue()
        ID = self.ID + 1
        puzzlePiece = None

        # Attempts to move the tile in 4 directions (up, down, right, and left)
        for direction in range(1, 5):
            tempBoard = deepcopy(puzzleBoard)
            zeroLocation = self.getZeroLocation(puzzleBoard)

            # Moving up
            if direction == 1:
                # check if tile is not already at the top of the board
                if zeroLocation[0] != 0:
                    puzzlePiece = tempBoard[zeroLocation[0] - 1][zeroLocation[1]]
                    tempBoard[zeroLocation[0] - 1][zeroLocation[1]] = tempBoard[zeroLocation[0]][zeroLocation[1]]
                    tempBoard[zeroLocation[0]][zeroLocation[1]] = puzzlePiece
            # Moving down
            elif direction == 2:
                # check if tile is not already at the bottom of the board
                if zeroLocation[0] != self.rows - 1:
                    puzzlePiece = tempBoard[zeroLocation[0] + 1][zeroLocation[1]]
                    tempBoard[zeroLocation[0] + 1][zeroLocation[1]] = tempBoard[zeroLocation[0]][zeroLocation[1]]
                    tempBoard[zeroLocation[0]][zeroLocation[1]] = puzzlePiece
            # Moving right
            elif direction == 3:
                # check if tile is not already on right side of board
                if zeroLocation[1] != self.columns - 1:
                    puzzlePiece = tempBoard[zeroLocation[0]][zeroLocation[1] + 1]
                    tempBoard[zeroLocation[0]][zeroLocation[1] + 1] = tempBoard[zeroLocation[0]][zeroLocation[1]]
                    tempBoard[zeroLocation[0]][zeroLocation[1]] = puzzlePiece
            # Moving left
            elif direction == 4:
                # check if tile is not already on left side of board
                if zeroLocation[1] != 0:
                    puzzlePiece = tempBoard[zeroLocation[0]][zeroLocation[1] - 1]
                    tempBoard[zeroLocation[0]][zeroLocation[1] - 1] = tempBoard[zeroLocation[0]][zeroLocation[1]]
                    tempBoard[zeroLocation[0]][zeroLocation[1]] = puzzlePiece

            # Assign cost of moving if zero location of new board is not the same as old
            # Only want to add to list if move hasn't been completed yet
            if self.getZeroLocation(tempBoard) != self.getZeroLocation(puzzleBoard):
                if 1 <= puzzlePiece <= 6:
                    gValue = self.g + 1
                elif 7 <= puzzlePiece <= 16:
                    gValue = self.g + 3
                else:
                    gValue = self.g + 15

                # If we haven't seen this board yet, add to list
                if tempBoard not in closedList:
                    moves.insertValue(State(tempBoard, ID, self.ID, self, gValue, direction))
                    ID += 1

        return moves


# Runs the methods to solve the board
class Solver(object):
    rows = 6
    columns = 3

    # Initializes the Solver class
    def __init__(self, startStateInput, goalStateInput, maxRunTime):
        self.startState = startStateInput
        self.goalState = goalStateInput
        self.maxRunTime = int(maxRunTime)
        self.puzzleBoard = []
        self.goalPuzzleBoard = []

        self.createBoards()

    # Creates the starting board and goal board
    def createBoards(self):
        value = 0
        for x in range(self.rows):
            self.puzzleBoard.append([])
            self.goalPuzzleBoard.append([])
            for y in range(self.columns):
                self.puzzleBoard[x].append(self.startState[value])
                self.goalPuzzleBoard[x].append(self.goalState[value])
                value = value + 1

    # Compares the current board to the goal board
    def compareBoard(self, puzzleBoard):
        equalCount = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if puzzleBoard[i][j] == self.goalPuzzleBoard[i][j]:
                    equalCount += 1

        return True if equalCount == (self.rows * self.columns) else False

    # Finds the location of a puzzle piece
    def find(self, puzzleBoard, puzzlePiece):
        for x in range(self.rows):
            for y in range(self.columns):
                if puzzleBoard[x][y] == puzzlePiece:
                    return x, y

    # First heuristic function
    def h1(self, state):
        x = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if state.puzzleBoard[i][j] != self.goalPuzzleBoard[i][j] and state.puzzleBoard[i][j] != '0':
                    x += 1
        state.h = x
        state.f = state.h + state.g

    # Second heuristic function
    def h2(self, state):
        x = 0
        for i in range(1, self.rows * self.columns):
            currentX, currentY = self.find(state.puzzleBoard, i)
            goalX, goalY = self.find(self.goalPuzzleBoard, i)
            x += abs((goalX - currentX) + (goalY - currentY))
        state.h = x
        state.f = state.h + state.g

    # Method to run breath first search
    def bfs(self):
        startTime = time.time()
        # Create open list as a priority queue and add initial state to queue
        openList = PriorityQueue()
        openList.insertValue(State(self.puzzleBoard, 1, None, None, 0, None))

        # Create closed list as a list
        closedList = list()

        stepCounter = 0
        nodesToOpenList = 0
        nodesToClosedList = 0
        notDone = True

        # Run while not finished finding optimal path
        while notDone:
            # Check is past the max run time
            if (startTime - time.time()) > self.maxRunTime:
                print("The max allotted run time of " + str(self.maxRunTime) + "seconds has been past.")
                print("No path was found in that time.")
                notDone = False
            # Can only execute is open list has values in queue
            elif len(openList.queue):
                # Gets the state from the open list with highest priority
                currentState = openList.getValue()

                # Checks to see if current state board is the goal board
                if self.compareBoard(currentState.puzzleBoard):
                    stopTime = time.time()
                    export(stepCounter, openList, nodesToOpenList, nodesToClosedList, currentState, stopTime - startTime)
                    notDone = False
                # Checks if the current puzzle board is not already in the closed list
                elif currentState.puzzleBoard not in closedList:
                    closedList.append(currentState.puzzleBoard)
                    nodesToClosedList += 1
                    stepCounter += 1
                    moves = currentState.moveTiles(closedList, currentState.puzzleBoard)
                    while len(moves.queue):
                        openList.insertValue(moves.getValue())
                        nodesToOpenList += 1

    # Method to run A* algorithm
    def astar(self):
        startTime = time.time()

        # Create open list as a priority queue and add initial state to queue
        openList = PriorityQueue()
        openList.insertValue(State(self.puzzleBoard, 1, None, None, 0, " "))

        # Create closed list as a list
        closedList = list()

        stepCounter = 0
        nodesToOpenList = 0
        nodesToClosedList = 0
        notDone = True

        while notDone:
            # Check is past the max run time
            if (startTime - time.time()) > self.maxRunTime:
                print("The max allotted run time of " + str(self.maxRunTime) + "seconds has been past.")
                print("No path was found in that time.")
                notDone = False

            # Can only execute is open list has values in queue
            elif len(openList.queue):
                # Gets the state from the open list with highest priority
                currentState = openList.getValue()

                # Checks to see if current state board is the goal board
                if self.compareBoard(currentState.puzzleBoard):
                    stopTime = time.time()
                    export(stepCounter, openList, nodesToOpenList, nodesToClosedList, currentState,
                           stopTime - startTime)
                    notDone = False
                # Checks if the current puzzle board is not already in the closed list
                elif currentState.puzzleBoard not in closedList:
                    closedList.append(currentState.puzzleBoard)
                    nodesToClosedList += 1
                    stepCounter += 1
                    moves = currentState.moveTiles(closedList, currentState.puzzleBoard)
                    while len(moves.queue):
                        currentMove = moves.getValue()
                        self.h2(currentMove)
                        openList.insertValue(currentMove)
                        nodesToOpenList += 1


# Exports results to file
def export(steps, openList, olCount, clCount, state, runTime):
    # Opens file to write to
    file = open('output.txt', 'w')
    file.write("         DONE        ")
    file.write("\n-------------------------------")
    file.write("\nNumber of steps: " + str(steps))
    file.write("\nPath to Goal: " + str(state.moves))
    file.write("\nTime: " + str(runTime) + " seconds")
    file.write("\nOpen List Size: " + str(len(openList.queue)))
    file.write("\nNodes Added to Open List: " + str(olCount))
    file.write("\nNodes Added to Closed List: " + str(clCount))
    file.write("\n-------------------------------\n")
    file.write("\nSteps From Goal to Start:")

    exportStateInfo(file, state)
    parentState = state.parentNode
    while parentState is not None:
        exportStateInfo(file, parentState)
        parentState = parentState.parentNode


# Writes state information to file
def exportStateInfo(file, state):
    file.write("\n--------------------------------")
    file.write("\nState ID: " + str(state.ID))
    file.write("\nParent State ID: " + str(state.parentID))
    file.write("\nG(n): " + str(state.g))
    file.write("\nH(n): " + str(state.h))
    file.write("\nF(n): " + str(state.f))
    file.write("\nDepth: " + str(state.depth))
    file.write("\nMove: " + str(state.move))
    file.write("\n--------------------------------")


# For reading the input arguments parsed by the program
def read(startConfig, goalConfig):
    startStateArray = []
    goalStateArray = []
    start = startConfig.split(",")
    goal = goalConfig.split(",")

    for x in start:
        startStateArray.append(int(x))
    for x in goal:
        goalStateArray.append(int(x))

    return startStateArray, goalStateArray


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('startstate')
    parser.add_argument('goalstate')
    parser.add_argument('runtime')
    arguments = parser.parse_args()

    # Parse input arguments
    startState, goalState = read(arguments.startstate, arguments.goalstate)

    # Create the solver class to run BFS
    solver = Solver(startState, goalState, arguments.runtime)
    solver.astar()



