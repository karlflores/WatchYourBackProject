import heapq
from node import Node
from copy import deepcopy
import constant


class Massacre(object):
    # constructor
    def __init__(self,node):
        # create an empty min heap priority queue for A*, greedy search algoriths if they were
        # to be implemented
        self.heapq = []

        # create an empty queue for BFS
        self.queue = []

        # create an empty stack for DFS
        self.stack = []

        # create a visited set to mark all visited board configurations/nodes such that we don't expand
        # previously expanded nodes -- stops infinite loops from occurring
        self.visitedSet = set()

        # create a list to store all moves
        self.reconstructPath = []

    # iterative deepening search algorithm
    def IDDFS(self,node):
        # copy the node to the start node of the search
        startNode = deepcopy(node)

        # iterate through the depths until max_depth
        for depth in range(constant.MAX_DEPTH):
            result = self.recursiveDLS(startNode,depth)
            if result is not constant.CUTOFF:
                return result

    def BFS(self,root):
        # copy the root to the starting node
        startNode = deepcopy(root)
        if startNode.isGoalState():
            return startNode

        # populate the queue with the successors of the starting node:
        for moves in root.board.availableMoves[constant.WHITE_PIECE]:
            if root.board.isLegalMove(moves[0],moves[1]):
                # create a new node
                newNode = self.createNode(startNode.board,moves,startNode.depth+1,startNode)

                if newNode.isGoalState():
                    return newNode

                # add new node to the queue
                self.queue.append(newNode)

        # add the board configuration of that node to the visited set list
        # we convert the boardState to a string such that it becomes hashable
        # then we add this to the list
        # therefore when we test for membership, need to remember to test the string version
        # of the boardState
        self.visitedSet.add(self.listToString(startNode))
        # dequeue an element from the node
        while len(self.queue) > 0:
            node = self.queue.pop(0)
            # add the node to the explored state
            if self.listToString(node.board.boardState) not in self.visitedSet:
                self.visitedSet.add(self.listToString(node.board.boardState))

            # test each of that nodes available actions
            for moves in node.board.availableMoves[constant.WHITE_PIECE]:
                # create a child node for this move
                child = self.createNode(node.board, moves, node.depth+1, node)

                # if a child node was not created, return no solution
                if child is None:
                    return None

                # if the child node is not in the visited set or in the frontier
                if self.listToString(child.board.boardState) not in self.visitedSet or child not in self.queue:

                    # test if the child node is the goal state
                    if child.isGoalState():
                        return child

                    # if it is not the goal state then append the child to the frontier queue
                    self.queue.append(child)

    # depth first search algorithm to search all possible moves
    def DFS(self,root):
        startNode = deepcopy(root)
        if startNode.isGoalState():
            return startNode

        # populate the stack with the successors of the starting node:
        for moves in root.board.availableMoves[constant.WHITE_PIECE]:
            if root.board.isLegalMove(moves[0],moves[1]):
                # create a new node
                newNode = self.createNode(startNode.board,moves,startNode.depth+1,startNode)

                if newNode.isGoalState():
                    return newNode

                # add new node to the queue
                self.stack.append(newNode)

        # add the board configuration of that node to the visited set list
        self.visitedSet.add(self.listToString(startNode))
        # pop an element from the stack
        while len(self.stack) > 0:
            node = self.stack.pop()
            # add the node to the explored state
            if self.listToString(node.board.boardState) not in self.visitedSet:
                self.visitedSet.add(self.listToString(node.board.boardState))

            # test each of that nodes available actions
            for moves in node.board.availableMoves[constant.WHITE_PIECE]:
                # create a child node for this move
                child = self.createNode(node.board, moves, node.depth+1, node)

                # if a child node was not created, return no solution
                if child is None:
                    return None

                # if the child node is not in the visited set or in the frontier
                if self.listToString(child.board.boardState) not in self.visitedSet or child not in self.stack:

                    # test if the child node is the goal state
                    if child.isGoalState():
                        return child

                    # if it is not the goal state then append the child to the frontier queue
                    self.stack.append(child)

    # For the IDDFS algorithm
    def recursiveDLS(self,node,depth):
        # BASE CASE
        # if the node is the goal state, we return the node
        if node.isGoalState():
            return node

        # if the depth of the call is 0 this is the cutoff values where we stop searching
        # so we return that the search has terminated at cutoff
        elif depth == 0:
            return constant.CUTOFF

        # if the depth is not at zero, we do the search
        # else we run DFS for depth -1 levels
        else:
            # set the cutoff flag to false -- if the search returns the cut off value we
            # return this value
            cutoffOccured = False

            # checks if the current node is a solvable node, if it is not, we return
            # a constant saying there is no solution at this node
            if node.isSolveable() is False:
                return constant.NO_SOLUTION

            # iterate through the successor nodes of the current node and run DFS on these
            # child nodes
            for move in node.board.availableMoves[constant.WHITE_PIECE]:
                # create a child node
                child = self.createNode(node.board, move, node.depth+1, node)
                # if the child node has not been visited before, recursively call recursiveDLS to
                # search the subtree of this child node

                resultDLS = self.recursiveDLS(child, depth-1)

                # change the cut off flag
                if resultDLS == constant.CUTOFF:
                    cutoffOccured = True
                # return the result if it is not a failed search
                elif resultDLS is not constant.FAILURE or resultDLS is not constant.NO_SOLUTION:
                    return resultDLS
        # if we have reached the depth and not have found the solution, return the cut off
        # value
        if cutoffOccured:
            return constant.CUTOFF
        else:
            # else return no solution/failure of the search
            return constant.FAILURE

    # Greedy Search implementation using a priority queue (BFS framework)
    def greedySearch(self,root):
        # copy the root to the starting node
        startNode = deepcopy(root)
        if startNode.isGoalState():
            return startNode
        # check if the root is actually solvable - ie. more than 2 white pieces on the board else return None
        if startNode.isSolveable() is False:
            return None

        # populate the queue with the successors of the starting node:
        for moves in root.board.availableMoves[constant.WHITE_PIECE]:
            if root.board.isLegalMove(moves[0],moves[1]):
                # create a new node
                newNode = self.createNode(startNode.board,moves,startNode.depth+1,startNode)
                # check if it is the goal state
                if newNode.isGoalState():
                    return newNode

                # check if the node is solvable, if it is add it to the heap
                if newNode.isSolveable():
                    heapq.heappush(self.heapq,newNode)

        # add the board configuration of that node to the visited set list
        self.visitedSet.add(self.listToString(startNode))
        # pop an element from the queue
        while len(self.heapq) > 0:
            node = heapq.heappop(self.heapq)

            # add the node to the explored state
            if self.listToString(node.board.boardState) not in self.visitedSet:
                self.visitedSet.add(self.listToString(node.board.boardState))

            # test each of that nodes available actions
            for moves in node.board.availableMoves[constant.WHITE_PIECE]:
                # create a child node for this move
                child = self.createNode(node.board, moves, node.depth+1, node)

                # if a child node was not created, return no solution
                if child is None:
                    return None

                # if the child node is not in the visited set or in the frontier
                if self.listToString(child.board.boardState) not in self.visitedSet or child not in self.heapq:

                    # test if the child node is the goal state
                    if child.isGoalState():
                        return child

                    # if it is not the goal state then append the child to the frontier queue
                    # only append the node if it is solvable
                    if child.isSolveable():
                        heapq.heappush(self.heapq,child)

    # creates a new node for search expansion
    @staticmethod
    def createNode(board,move,depth,parent):

        # instantiate a new node
        node = Node(board,move)

        if node is None:
            return None

        # update the parent, depth of the node
        node.depth = depth
        node.parent = parent

        # apply the move to the node
        node.board.updateBoardState(move[0],move[1])

        # update the priority of the node based on the heuristic
        node.priority = node.countBlackPieces()
        return node

    # set helper methods for hashing array to a set
    @staticmethod
    def listToString(list):
        return str(list)
