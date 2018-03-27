import heapq
from node import Node
from copy import deepcopy
import constant

class Massacre(object):

    def __init__(self,node):
        # create an empty min heap priority queue for A*, dijkstra, greedy search algorithm implementation
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

    # iterative deepening search
    def IDDFS(self,node):
        # copy the node to the start node of the search
        startNode = deepcopy(node)

        # iterate through the depths
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
                newNode = self.createNode(startNode.board,moves,startNode.depth+1,
                startNode,startNode.counter+1)

                if newNode.isGoalState():
                    return newNode

                # add new node to the queue
                self.queue.append(newNode)

        # add the board configuration of that node to the visited set list
        # if startNode.board.boardState not in self.visitedSet:
        #    self.visitedSet.append(newNode.board.boardState)

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
                child = self.createNode(node.board, moves, node.depth+1, node, node.counter+1)

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

    def DFS(self,root):
        startNode = deepcopy(root)
        if startNode.isGoalState():
            return startNode

        # populate the stack with the successors of the starting node:
        for moves in root.board.availableMoves[constant.WHITE_PIECE]:
            if root.board.isLegalMove(moves[0],moves[1]):
                # create a new node
                newNode = self.createNode(startNode.board,moves,startNode.depth+1,
                startNode,startNode.counter+1)

                if newNode.isGoalState():
                    return newNode

                # add new node to the queue
                self.stack.append(newNode)

        # add the board configuration of that node to the visited set list
        # if startNode.board.boardState not in self.visitedSet:
        #    self.visitedSet.append(newNode.board.boardState)

        # we convert the boardState to a string such that it becomes hashable
        # then we add this to the list
        # therefore when we test for membership, need to remember to test the string version
        # of the boardState
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
                child = self.createNode(node.board, moves, node.depth+1, node, node.counter+1)

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


    def recursiveDLS(self,node,depth):
        # BASE CASE
        # if the node is the goal state, we return the node
        if node.isGoalState():
            return node

        # if the depth of the call is 0 this is the cutoff values where we stop searching
        # so we return the cutoff value
        elif depth == 0:
            return constant.CUTOFF

        # else we just do the search
        else:
            cutoffOccured = False

        # else we run DFS for depth -1 levels
            # iterate through the successor nodes of the current node and run DFS on this node
            for move in node.board.availableMoves[constant.WHITE_PIECE]:
                # create a child node
                child = self.createNode(node.board, move, node.depth+1, node, node.counter+1)
                # recursively call recursiveDLS to search the subtree of this child node
                resultDLS = self.recursiveDLS(child, depth-1)

                if resultDLS == constant.CUTOFF:
                    cutoffOccured = True
                # return the result if it is not a failed search
                elif resultDLS is not constant.FAILURE:
                    return resultDLS
        # if we have reached the depth and not have found the solution, return the cut off
        # value
        if cutoffOccured:
            return constant.CUTOFF
        else:
            # else return no solution/failure of the search
            return constant.FAILURE


    def BFS_WITH_HEAPPQ(self,root):
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
                newNode = self.createNode(startNode.board,moves,startNode.depth+1,
                startNode,startNode.counter+1)
                # check if it is the goal state
                if newNode.isGoalState():
                    return newNode

                # check if the node is solvable, if it is add it to the heap
                if newNode.isSolveable():
                    heapq.heappush(self.heapq,newNode)

        # add the board configuration of that node to the visited set list
        # we convert the boardState to a string such that it becomes hashable
        # then we add this to the list
        # therefore when we test for membership, need to remember to test the string version
        # of the boardState
        self.visitedSet.add(self.listToString(startNode))
        # dequeue an element from the node
        while len(self.heapq) > 0:
            node = heapq.heappop(self.heapq)

            # add the node to the explored state
            if self.listToString(node.board.boardState) not in self.visitedSet:
                self.visitedSet.add(self.listToString(node.board.boardState))

            # test each of that nodes available actions
            for moves in node.board.availableMoves[constant.WHITE_PIECE]:
                # create a child node for this move
                child = self.createNode(node.board, moves, node.depth+1, node, node.counter+1)

                # if a child node was not created, return no solution
                if child is None:
                    return None

                # if the child node is not in the visited set or in the frontier
                if self.listToString(child.board.boardState) not in self.visitedSet or child not in self.heapq:

                    # test if the child node is the goal state
                    if child.isGoalState():
                        return child

                    # if it is not the goal state then append the child to the frontier queue
                    # only append the node if it is solveable
                    if child.isSolveable():
                        heapq.heappush(self.heapq,child)

    # creates a new node for search expansion
    @staticmethod
    def createNode(board,move,depth,parent,counter):

        # instantiate a new node
        node = Node(board,move)

        if node is None:
            return None

        # update the parent, depth and counter of the node
        node.depth = depth
        node.parent = parent
        node.counter = counter

        # apply the move to the node
        node.board.updateBoardState(move[0],move[1])

        # update the priority of the node based on the heuristic
        node.priority = node.countBlackPieces()
        return node

    def reconstruct(self,node):
        # create a variable representing the start node
        newNode = node
        # whilst the parent of a node exists we can reconstruct the path of
        # that gets to that specific node
        while newNode.parent is not None:
            self.reconstructPath.append(newNode.moveApplied)

            # set the newNode to be the parent of the previous node
            newNode = newNode.parent
            # add comment
        return self.reconstructPath

    # set helper methods for hashing array to a set
    @staticmethod
    def listToString(list):
        return str(list)
        
