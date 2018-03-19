from gameBoard import Board
import heapq
class Massacre(object):
    def __init__(self,node):
        # create an empty min heap priority queue for A*, dijkstra, greedy search algorithm implementation
        self.heapq = []

        # create an empty queue for BFS
        self.queue = []

        # create an empty stack for DFS

        self.stack = []

        # create a visited set to mark all visited board configurations/nodes such that we don't expand
        # previously expanded nodes -- stops infinite loops from occuring
        self.visitedSet = set()

        # create a list to store all moves
        self.reconstructPath = []

    # define a heuristic for A*
    def heuristic(self):
        pass

    # iterative deepening search
    def ITDS(self,node):
