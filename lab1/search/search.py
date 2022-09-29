# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal .
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of  that solves tinyMaze.  For any other maze, the
    sequence of  will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    visited = [problem.getStartState()]
    stack.push(problem.getStartState())
    state = problem.getStartState()
    moves = {}
    route = []

    while not problem.isGoalState(state):
        state = stack.pop()
        successors = problem.getSuccessors(state)

        for move in successors:
            place = list(move)[0]  # place of successor in the maze
            if place not in visited:
                moves[place] = [state, list(move)[1]]  # key is the place, value`s an array where 0- parent place,
                                                       # 1- direction from parent to successor
                stack.push(place)
                visited.append(place)

    move = moves.pop(state)
    while True:
        route.append(move[1])
        if move[0] in moves.keys():
            move = moves.pop(move[0])
        else:
            break
    route.reverse()
    return route

    # util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    queue = util.Queue()
    visited = [problem.getStartState()]
    queue.push(problem.getStartState())
    state = problem.getStartState()
    moves = {}
    route = []

    while not problem.isGoalState(state):
        state = queue.pop()
        successors = problem.getSuccessors(state)

        for move in successors:
            place = list(move)[0]  # place of successor in the maze
            if place not in visited:
                moves[place] = [state, list(move)[1]]  # key is the place, value`s an array where 0- parent place,
                # 1- direction from parent to successor
                queue.push(place)
                visited.append(place)

    move = moves.pop(state)
    while True:
        route.append(move[1])
        if move[0] in moves.keys():
            move = moves.pop(move[0])
        else:
            break
    route.reverse()
    return route
    #util.raiseNotDefined()


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    priorityQueue = util.PriorityQueue()

    startPosition = problem.getStartState()

    h = heuristic(problem.getStartState(), problem)

    start = [startPosition, (), 0, h, 'NONE']  # 0 - position, 1 - parent node, 2 - g(distance between root and element)
                                               # 3 - f, 4 - direction

    visitedPositions = {startPosition: start}  # map in which key is a position
                           # and value is an array consisting of ancestor and f value

    priorityQueue.push(startPosition, h)
    route = []  # array of directions

    q = visitedPositions.get(startPosition)

    while not priorityQueue.isEmpty():
        q = priorityQueue.pop()

        if problem.isGoalState(q):
            break

        qData = visitedPositions.get(q)
        qAncestor = qData[1]

        qSuccessors = problem.getSuccessors(q)
        for successor in qSuccessors:
            successorConvertedIntoList = list(successor)
            position = successorConvertedIntoList[0]
            direction = successorConvertedIntoList[1]

            g = qData[2] + successorConvertedIntoList[2]
            h = heuristic(position, problem)
            f = g + h

            node = [position, q, g, f, direction]

            existingPosition = visitedPositions.get(position)
            if existingPosition is not None:
                existingF = existingPosition[3]

                if existingF > f:
                    print('true')
                    visitedPositions[position] = node
                    priorityQueue.update(position, f)
            else:
                visitedPositions[position] = node
                priorityQueue.push(position, f)

    move = visitedPositions.get(q)
    while True:
        if move[4] == "NONE":
            # print(route)
            # print("done")

            break
        route.append(move[4])
        # print(move)
        move = visitedPositions.pop(move[1])
    route.reverse()

    return route
    #util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
