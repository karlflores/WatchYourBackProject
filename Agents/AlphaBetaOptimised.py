'''
* Implements the mini-max algorithm based on the minimax_mode structure
* and the player file
'''
from math import inf
from Board.Board import constant
from Board.Board import Board
from Evaluation.Policies import Evaluation
from copy import deepcopy
from time import time, sleep
from functools import lru_cache
import heapq

class MinimaxABOptimised(object):

    def __init__(self, board, colour):
        # we want to create a node

        self.transposition_table = set()

        # only use this board to complete the search
        # save memory
        self.board = deepcopy(board)

        # for alpha beta search -- instead of passing it into the function calls we can use this
        self.alpha = -inf
        self.beta = inf

        # defines the colours of min and max
        self.player = colour
        self.opponent = Board.get_opp_piece_type(self.player)

        # default depth
        self.depth = inf

        # default move ordering with iterative deepening
        self.actions_evaluated = []
        self.actions_leftover = []

    '''
    * Alpha Beta - Minimax Driver Function 
    '''

    def iterative_deepening_alpha_beta(self):
        '''
        I dont think this is working correctly -- i believe when things are getting cached because it doesnt take in consideration the depth of the call of that minimax evaluation
        we need to take into consideration the depth for it to call correctly

        need to change this
        '''
        MAX_ITER = 10

        # default policy
        available_actions = self.board.update_actions(self.board,self.player)
        # self.actions_leftover = self.board.update_actions(self.board, self.player)

        if len(available_actions) == 0:
            return None
        else:
            # lets just set the default to the first move
            move = available_actions[0]


        # time allocated per move in ms
        time_alloc = 1500

        # get time
        start_time = MinimaxABOptimised.curr_millisecond_time()

        # iterative deepening begins here
        for depth in range(1, MAX_ITER):
            print(depth)
            # invalidate / clear the cache when increasing the search depth cutoff
            self.min_value.cache_clear()

            # peform the search
            move = self.alpha_beta_minimax(depth, available_actions)

            # after one iteration of ab search we can order the moves based on the actions that
            # the previous depth evaluated the actions at
            available_actions = []
            while len(self.actions_evaluated) > 0:
                (val, action) = heapq._heappop_max(self.actions_evaluated)
                available_actions.append(action)
            # transform the heap into a max heap
            heapq._heapify_max(self.actions_evaluated)

            # update the available_actions list
            available_actions = available_actions + self.actions_leftover

            sleep(0.05)

            if MinimaxABOptimised.curr_millisecond_time() - start_time > time_alloc:
                break

        return move

    def set_player_colour(self,colour):
        self.player = colour;
        self.opponent = Board.get_opp_piece_type(colour)

    @staticmethod
    def curr_millisecond_time():
        return int(time() * 1000)

    def alpha_beta_minimax(self, depth, available_actions):
        self.actions_evaluated = []
        if self.board.phase == constant.MOVING_PHASE and self.board.move_counter == 0:
            self.min_value.cache_clear()
            # self.max_value.cache_clear()
        # print the available mvoes of the alpha beta call
        # print(root.available_moves)
        # generate the child nodes of the root node and run minimax  on these
        # nodes -- choose the node that has the best value

        best_move = None
        alpha = -inf
        evaluate = -inf
        beta = inf

        # update the minimax depth counter
        self.depth = depth


        i = 0
        # get the available moves of the board (based on the current board representation)
        # we can generate the actions as we wish -- this can easily change -- TODO : OPTIMISATION/ PRUNING OF ACTION __ CAN BE GREEDY __ favoured moves and unfavoured moves
        self.actions_leftover = self.board.update_actions(self.board, self.player)
        # self.actions_leftover = self.board.update_actions(self.board,self.player)

        for action in available_actions:
            # print("{} Action AB call".format(i))
            # update the minimax board representation with the action
            self.board.update_board(action, self.player)

            board_string = self.board.board_state.decode("utf-8")

            # decrease the depth counter
            self.depth -= 1

            ab_evaluate = self.min_value(board_string, self.opponent, self.board.phase, depth - 1)
            # print(ab_evaluate)
            # print(self.min_value.cache_info())

            heapq.heappush(self.actions_evaluated, (ab_evaluate, action))
            self.actions_leftover.remove(action)

            if ab_evaluate > evaluate:
                best_move = action
                evaluate = ab_evaluate

            self.undo_move()
            self.depth += 1

            if evaluate >= beta:
                # print(evaluate)
                # print("AB Best Value: ",end='')
                # rint(evaluate, best_move)
                return best_move

            alpha = max(alpha, evaluate)

        # print(best_move)
        # print(evaluate)
        # print("AB Best Value: ",end='')
        # print(evaluate, best_move)
        return best_move

    # memoize the function call -- opitimisation
    # @lru_cache(maxsize=50000)
    def max_value(self,board_string, colour, phase, depth):

        evaluate = -inf

        if self.cutoff_test(depth):
            return self.evaluate_state(self.board)

        # visit each available move
        available_actions = self.board.update_actions(self.board, colour)

        for action in available_actions:

            # update the board representation with the move
            self.board.update_board(action, colour)
            self.depth -= 1
            # create an immutable object for board_string such that we can call lru_cache on the max function call
            board_string = self.board.board_state.decode("utf-8")

            # get the minimax value for this state

            evaluate = max(evaluate, self.min_value(board_string, self.opponent, self.board.phase, depth-1))
            # print(self.board.action_applied)

            # undo the move so that we can apply another action
            self.undo_move()
            self.depth += 1

            if evaluate >= self.beta:
                return evaluate

            self.alpha = max(evaluate, self.alpha)

        return evaluate

    # memoize the min value results -- optimisation of its function call
    @lru_cache(maxsize=10000)
    def min_value(self, board_string, colour, phase, depth):
        # print("CALLED MIN")
        # beginning evaluation value
        evaluate = inf

        if self.cutoff_test(depth):
            # val = self.evaluate_node(node)
            # print("MIN NODE VAL: ",end='')
            # print(val)
            # return val
            # print(self.evaluate_node(node))
            return self.evaluate_state(self.board)
        # print("MIN MOVES: ",end='')
        # print(node.available_moves)

        # generate the actions to search on
        available_actions = self.board.update_actions(self.board, colour)

        for action in available_actions:

            # update the board representation -- this action is the min nodes's action
            self.board.update_board(action, colour)
            # when we apply a move we do down a level so we have to decrease depth
            self.depth -= 1

            board_string = self.board.board_state.decode("utf-8")

            # find the value of the max node
            evaluate = min(evaluate, self.max_value(board_string, self.player, self.board.phase, depth - 1))

            # undo the board move so that we can apply another move
            # -- we also go up a level therefore we need to increment depth
            self.undo_move()
            self.depth += 1

            '''
            if beta <= alpha:
                # when we break from the loop make sure to undo the move
                break
            '''

            if evaluate <= self.alpha:

                # print("MIN Best Value: ",end='')
                # print(evaluate)
                return evaluate

            self.beta = min(self.beta, evaluate)

        return evaluate
    def cutoff_test(self, depth):
        if depth == 0:
            return True

        if self.is_terminal():
            return True

        return False

    '''
    * NEED TO THINK ABOUT IF THIS FUNCTION JUST EVALUATES THE NODES AT THE ROOT STATE DUE TO THE UNDO MOVES 
            -- NEED TO TEST THIS OUT SOMEHOW, because other than that the algorithm is working as intended 
            -- Need to work out some optimisations of the algorithm though 

    '''

    def evaluate_state(self, board):
        return Evaluation.basic_policy(board, self.player)

    # update the available moves of the search algorithm after it has been instantiated
    #
    # def update_available_moves(self, node, available_moves):
    #    node.available_moves = available_moves

    def update_board(self, board):
        self.board = deepcopy(board)


    def is_terminal(self):
        return self.board.is_terminal()

    def check_symmetry(self, board_state):
        transformation = MinimaxABUndo.apply_horizontal_reflection(board_state)
        board = deepcopy(board_state)
        if transformation.decode("utf-8") in self.visited:
            return True
        else:
            self.visited.add(board.decode("utf-8"))
            return False

    @staticmethod
    def apply_horizontal_reflection(board_state):
        temp = ''
        for index in range(constant.BOARD_SIZE ** 2):
            temp += constant.FREE_SPACE

        temp = bytearray(temp, 'utf-8')

        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                Board.set_array_char(temp, 7 - row, 7 - col,
                                     Board.get_array_element(board_state, row, col))
        # print(temp)
        # print(board_state)
        return temp

    def undo_move(self):
        self.board.undo_move()
        # then we need to recalculate the available moves based on the board representation
        # self.generate_actions()

