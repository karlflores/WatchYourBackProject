from math import inf,sqrt,log
from Agents.MCTS_Node import Node
from Constants import constant
from WatchYourBack.Board import Board
from copy import deepcopy
from time import time
from random import randint
# need to store untried moves

'''
MCTS PLAYER DOES NOT WORK IF IT IS THE SECOND PLAYER TO MOVE 

TODO -- this need to be fixed 

THIS CLASS IMPLEMENTED MONTE CARLO TREE SEARCH FOR WATCH YOUR BACK 
IT WAS FOUND THAT DUE TO TIME RESTRICTIONS OF MAKING A MOVE THAT WE WERE NOT ABLE TO GENERATE 
A BIG ENOUGH GAME TREE SUCH THAT THE MOVE WE WERE GOING TO MAKE WAS GOING TO BE SOMEWHAT 'GOOD'

THIS IS BECAUSE THE TIME TO SIMULATE A COMPLETELY RANDOM GAME WAS ~0.08s ON AVERAGE, MEANING THAT IN
A 1sec EVALUATION, WE COULD ONLY CREATE 12 NODES TO A SEARCH TREE 

THE GAME HAS A BRANCHING FACTOR OF ~46 MOVES AT THE START OF THE GAME, HENCE WE COULD NOT GENERATE 
A GAME TREE OF AT LEAST ONE WHOLE SET OF AVAILABLE MOVES, THEREFORE WE DECIDED AGAINST USING THIS
AGENT IN OUR FINAL IMPLEMENTATION 

THAT BEING SAID, THIS AGENT, GIVEN ENOUGH TIME, IS ABLE TO PICK INFORMED MOVES, BUT THE TIME IT TAKES
TO CONVERGE IS MUCH TOO SLOW... (HOURS UPON HOURS...)

note: with the reimplemented board mechanisms -- the simulation time was cut from ~0.08s to ~0.04s, this is still
very inefficient
Running some tests -- in a 2 min evaluation roughly 200 nodes are able to be created, therefore if we assume
a branching factor of ~44 the game tree that is constructed is roughly 2-ply deep. Although this is not entirely the 
case as the tree actually grows asymmetrically. 

'''
# start this implementation with each node storing a copy of the board -- then change the implementation such that
# we only use one board representation for the board state -- we just undo moves
class MonteCarloTreeSearch(object):
    def __init__(self,board,colour):
        # this is the board on which we will do our search -- every time we search our
        # tree we will just use this board do it -- when we simulate we will deepcopy the
        # board and do the simulation on that new board so that we can always revert the
        # board it is original state
        self.board = deepcopy(board)

        self.colour = colour

        # number of actions applied to the state of the board -- to return the board to its
        # original state we just need to undo until the actions are 0
        self.action_num = 0

        self.num_nodes = 0

    def MCTS(self, explore_param=sqrt(2)):
        start_time = time()*1000
        end_time = start_time
        # is the root a child node -- if it is we need to look at its child nodes

        # this is the start of the search
        root = self.create_node(self.board, self.colour, None, None)
        root.update_actions()

        while (end_time - start_time) < constant.TIME_CUTOFF:
            # we traverse until we get to a child node
            node = self.UCB1_policy(root, explore_param)

            # we have expanded the leaf node and of all the actions, we have picked the action with
            # the highest UCB1
            net_win = self.simulate(node)

            # after simulation we will back-propagate the values of the simulation
            self.value_backpropagation(node, net_win)

            end_time = time()*1000
        # after this we will make a move
        return self.make_move(root)

    # this is the default policy -- i.e from a given game state we simulate the game randomly
    def simulate(self, node):
        start_time = time()
        # simulate the state based on the actions of the child
        # this is the board on which we do our simulation
        board = deepcopy(node.board)
        #print(board.move_counter)
        #print(board.phase)
        #print(board.piece_pos)
        available_actions = board.update_actions(board, node.colour)
        #print("available_actions")
        #print(available_actions)
        #print(board.is_terminal())
        colour = node.colour
        num_moves = 0

        while board.is_terminal() is False:
            if len(available_actions) == 0:
                # there are no actions to take and therefore it is a forfeit
                action = None
            else:
                # pick a random move -- actions
                action_ind = randint(0,len(available_actions)-1)
                action = available_actions[action_ind]

            # apply the action to the board
            board.update_board(action,colour)
            #board.print_board()
            # update the colour of the piece
            colour = Board.get_opp_piece_type(colour)
            # update the new available actions list -- this action list represents the
            # actions of next player -- this is the player that will make the next move
            available_actions = board.update_actions(board, colour)
        end_time = time()

        # print((end_time - start_time))
        # now we are at a terminal state, we need to find out who has won
        #print(board.winner)

        if board.winner == node.colour:
            return 1
        elif board.winner == Board.get_opp_piece_type(node.colour):
            return -1
        elif board.winner is None:
            return 0


    @staticmethod
    def value_backpropagation(node,value):
        while node is not None:
            node.visit_num += 1
            node.wins += value
            node = node.parent

    def expand(self,node):
        # print("expanded")
        # call on an expandable node to create one more child node -- we add the child to the leaf
        # then we update the current node we are at to this leaf node

        # choose an action -- choose randomly
        action_index = randint(0, len(node.untried_actions)-1)

        action = node.untried_actions[action_index]
        # remove that action from the untried action list
        node.untried_actions.remove(action)

        # create the new node to be added to the game tree
        child = self.create_node(node.board,Board.get_opp_piece_type(node.colour), action, node)

        # apply the move to that child node
        # the parent applies its move to that board
        child.board.update_board(action, node.colour)
        child.update_actions()

        # add this child to the parents child list
        node.add_child(child)
        self.num_nodes+=1
        return child

    # evaluate the UCB1 value of a particular node -- this is what we use to explore
    # the tree until we get to a child node
    def UCB1(self,node,explore_param):
        # check if the parent exists
        if node.parent is None:
            return None

        # if the node has not been explored before/visited then the ucb value of that node is infinite
        # this means that this will be explored first
        if node.visit_num == 0:
            node.ucb_value = inf
            return

        # evaluate the UCB
        val = node.wins/node.visit_num +explore_param*sqrt(log(node.parent.visit_num)/node.visit_num)
        node.ucb_value = val
        return

    # this is the selection and expansion phase of the algorithm
    # UCB1 selects the most urgent child, and expands it to an unvisited state - then returns this unvisited node
    def UCB1_policy(self,root, explore_param):
        #print("UCB1")
        #print(root)
        node = root
        select_node = None

        while node.is_terminal() is False:
            #print("xxx")
            # test if the node we are on is a child node -- ie it has not been expanded before
            if node.is_fully_expanded() is False:
                #print("check expanded")
                child = self.expand(node)
                # print(child)
                return child
            else:

                # choose the child with the best UCB1 score
                # if it is not a child node then we want to find which of its nodes has the highest UCB and traverse
                # down that node
                best_ucb = -inf
                for child in node.children:
                    # set the UCB1 values of all its children
                    self.UCB1(child, explore_param)

                    if child.ucb_value > best_ucb:
                        best_ucb = child.ucb_value
                        select_node = child

                node = select_node
                # apply the best_child's action to the board
                # child.board.update_board(best_child.move, best_child.colour)
                self.action_num += 1

        # return the selected node
        return select_node

    # update the root of the tree
    def update_root(self,root):
        self.root = root
        # update the actions of the root
        self.root.update_actions()

    # update the internal board representation
    def update_board(self,board):
        self.board = deepcopy(board)

    # method to create the node for the search
    @staticmethod
    def create_node(board,colour,move,parent):
        node = Node(board,colour,move,parent)
        node.move = move
        node.parent = parent
        return node

    # method to choose the move based on the UCB values of its children
    def make_move(self,root):
        best_move = None
        best_ucb = -inf
        best_child = None
        for child in root.children:
            self.UCB1(child, sqrt(2))
            print(child.ucb_value)

            if child.ucb_value > best_ucb:
                best_move = child.move
                best_ucb = child.ucb_value
                best_child = child

        # print("UCB: ",end='')
        # print(best_ucb)
        # print("WINS: ",end='')
        # print(best_child.wins)
        #
        # print("VISITED: ",end='')
        # print(best_child.visit_num)
        # print("PARENT VISITED: ",end='')
        # print(best_child.parent.visit_num)
        return best_move
