from gameBoard import Board
import heapq
from node import Node
from copy import deepcopy
import constant
from queue import PriorityQueue

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
        startNode = deepcopy(node)
        for depth in range(10):
            result = self.recursiveDLS(startNode,problem)


    def BFS(self,root):
        # copy the root to the starting node
        startNode = deepcopy(root)
        if startNode.isGoalState():
            return node

        # populate the queue with the successors of the starting node:
        for moves in root.board.availableMoves[constant.WHITE_PIECE]:
            if root.board.isLegalMove(moves[0],moves[1]):
                # create a new node
                newNode = self.createNode(startNode.board,moves,startNode.depth+1,startNode,startNode.counter+1)

                if newNode.isGoalState():
                    return newNode

                # add new node to the queue
                self.queue.append(newNode)
                # newNode.board.printBoard()
                # print()

        # add the board configuration of that node to the visited set list
        # if startNode.board.boardState not in self.visitedSet:
        #    self.visitedSet.append(newNode.board.boardState)

        # we convert the boardState to a string such that it becomds hashable
        # then we add this to the list
        # therefore when we test for memebership, need to remember to test the string version
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
                # child.board.printBoard()
                # print()

                # if a child node was not created, return no solution
                if child is None:
                    return None

                # if the child node is not in the visited set or in the frontier
                if self.listToString(child.board.boardState) not in self.visitedSet or child not in self.queue:

                    # test if the child node is the goal state
                    if child.isGoalState():
                        # print ("arb")
                        return child

                    # if it is not the goal state then append the child to the frontier queue
                    self.queue.append(child)

    def DFS(self,node):
        pass

    def recursiveDLS(self,node,limit):
        pass

    def BFS_WITH_HEAPPQ(self,root):
        # copy the root to the starting node
        startNode = deepcopy(root)
        if startNode.isGoalState():
            print("wtf2")
            return startNode

        # populate the queue with the successors of the starting node:
        for moves in root.board.availableMoves[constant.WHITE_PIECE]:
            if root.board.isLegalMove(moves[0],moves[1]):
                # create a new node
                newNode = self.createNode(startNode.board,moves,startNode.depth+1,startNode,startNode.counter+1)

                if newNode.isGoalState():
                    print("wtf")
                    return newNode

                # add new node to the queue
                # newNodeTuple = (newNode.countNum(),newNode)
                # print(newNodeTuple)
                heapq.heappush(self.heapq,newNode)
                # newNode.board.printBoard()
                # print()

        # add the board configuration of that node to the visited set list
        # if startNode.board.boardState not in self.visitedSet:
        #    self.visitedSet.append(newNode.board.boardState)

        # we convert the boardState to a string such that it becomds hashable
        # then we add this to the list
        # therefore when we test for memebership, need to remember to test the string version
        # of the boardState
        self.visitedSet.add(self.listToString(startNode))
        print("asdfasdfasf")
        # dequeue an element from the node
        while len(self.heapq) > 0:
            node = heapq.heappop(self.heapq)
            # print(node)
            # add the node to the explored state
            if self.listToString(node.board.boardState) not in self.visitedSet:
                self.visitedSet.add(self.listToString(node.board.boardState))

            # test each of that nodes available actions
            for moves in node.board.availableMoves[constant.WHITE_PIECE]:
                # create a child node for this move
                child = self.createNode(node.board, moves, node.depth+1, node, node.counter+1)
                child.board.printBoard()
                print()

                # if a child node was not created, return no solution
                if child is None:
                    print("wtf3")
                    return None

                # if the child node is not in the visited set or in the frontier
                if self.listToString(child.board.boardState) not in self.visitedSet or child not in self.heapq:

                    # test if the child node is the goal state
                    if child.isGoalState():
                        # print("arb")
                        return child

                    # if it is not the goal state then append the child to the frontier queue
                    heapq.heappush(self.heapq,child)
                    print(child.priority)

    def createNode(self,board,move,depth,parent,counter):

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
        node.priority = node.totalManhattanDist()
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

    # set helper methods
    def listToString(self,list):
        return str(list)

    def __lt__(self, other):
        return self.priority < other.priority