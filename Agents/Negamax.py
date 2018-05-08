'''
* Implements the mini-max algorithm based on the minimax_mode structure
* and the player file
'''
from math import inf
from Constants import constant
from Board.Board import Board
from Evaluation.Policies import Evaluation
from Data_Structures.Transposition_Table import TranspositionTable
from copy import deepcopy
from time import time
from Error_Handling.Errors import *

'''
FINAL NEGAMAX IMPLEMENTATION WITH A GREEDY CHOICE ON WHAT MOVES TO EXPLORE -- WE ONLY PICK A CERTAIN
SUBSET OF THE AVAILABLE MOVES BASED ON WHAT WE THINK IS GOOD IN THE CURRENT STATE (NOT LOOKING AHEAD)
WE THEN DO A MINIMAX/NEGAMAX SEARCH ON THESE AVAILABLE MOVES AND CHOOSE THE BEST POSSIBLE MOVE OUR OF
THE SUBSET OF FAVOURABLE MOVES THAT WE HAVE CHOSEN

WE SCORE EACH AVAILABLE ACTION USING AN EVALUATION FUNCTION THAT LOOKS AT CAPTURE ABILITY, SELF-ELIMINATION,
FORMATION, AND POSITIONING ON THE BOARD TO DETERMINE WHETHER AN ACTION IS GOOD OR NOT. THIS IS THEN USE 
TO NAIVELY SORT THE ACTIONS BASED ON ITS EVALUATION.

THIS IMPLEMENTATION ALSO IMPLEMENTS ITERATVE DEEPENING WITH A TIMER SUCH THAT WHEN THE TIME RUNS OUT FOR
EVALUATION THE NEGAMAX CALL RAISES A TIMEOUT EXCEPTION AND ITERATIVE DEEPENING IS ABLE TO RETURN THE BEST
MOVE FOUND SO FAR.

THIS NEGAMAX ALSO IMPLEMENTS ALPHA BETA PRUNING -- WE TRY TO MAKE THE MOST OF AB PRUNING BY IMPLEMENTING 
SOME SORT OF MOVE ORDERING 

'''

class Negamax(object):

    def __init__(self, board, colour):
        # we want to create a node

        self.tt = TranspositionTable()

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

        # data structures for machine learning
        self.eval_depth = 0
        self.minimax_val = 0
        self.policy_vector = []

        # dictionary storing the available moves of the board
        self.available_actions = {constant.WHITE_PIECE: {}, constant.BLACK_PIECE: {}}

        # generate the actions for the start of the game
        # self.generate_actions()

        self.undo_effected = []
        self.time_alloc = 0
        self.time_rem = 0
        self.time_start = 0
        self.time_end = 0

        self.evaluation = Evaluation("./XML","/eval_weights")

    '''
    * Alpha Beta - Minimax Driver Function 
    '''

    def itr_negamax(self):
        # clear the transposition table every time we make a new move -- this is to ensure that it doesn't grow too big
        # if self.board.phase == constant.MOVING_PHASE and self.board.move_counter == 0:
        #if self.board.phase == constant.PLACEMENT_PHASE:
        self.tt.clear()

        MAX_ITER = 10

        # default policy
        available_actions = self.board.update_actions(self.board, self.player)
        print(len(available_actions))
        action_set = set(available_actions)
        # self.actions_leftover = self.board.update_actions(self.board, self.player)

        if len(available_actions) == 0:
            return None
        #else:
            # lets just set the default to the first move
        #    move = available_actions[0]

        # time allocated per move in ms
        '''
        self.time_alloc = 0
        if self.board.phase == constant.PLACEMENT_PHASE:
            self.time_alloc = (30000 - self.time_alloc) / (24 - self.board.move_counter)
        else:
            self.time_alloc = (30000 - self.time_alloc) / (100 - self.board.move_counter)
        '''

        # self.time_alloc = 5000
        # time allocated per move in ms
        self.time_alloc = 0
        total = 120000
        if self.board.phase == constant.PLACEMENT_PHASE:
            #self.time_alloc = (total/2 - self.time_alloc) / (24 - self.board.move_counter)
            #total -= self.time_alloc
            self.time_alloc = 1000
        else:
            #self.time_alloc = (total - self.time_alloc) / (100 - self.board.move_counter)
            #total -= self.time_alloc
            self.time_alloc = 1000
        # get time
        start_time = Negamax.curr_millisecond_time()
        best_depth = 1
        val, move = 0, None
        # iterative deepening begins here
        best_move = None
        for depth in range(1, MAX_ITER):
            print(self.tt.size)
            print(depth)
            try:
                self.time_rem = self.time_alloc
                self.time_start = self.curr_millisecond_time()
                val, move = self.negamax(depth,-inf,inf,self.player)
                self.time_end = self.curr_millisecond_time()

                self.time_rem = self.time_alloc - (self.time_end-self.time_start)
                print(move)
                best_depth += 1

                # if we have a move that is not none lets always pick that move that is legal
                # becuase we are doing a greedy search -- it sometimes returns an illegal move, not too sure why
                # therefore here we check if a move is legal as well
                if move is not None and move in action_set:
                    best_move = move
            except TimeOut:
                print("TIMEOUT")
                break

            if Negamax.curr_millisecond_time() - start_time > self.time_alloc:
                break

        self.eval_depth = best_depth
        return best_move

    def set_player_colour(self, colour):
        self.player = colour;
        self.opponent = Board.get_opp_piece_type(colour)

    @staticmethod
    def curr_millisecond_time():
        return int(time() * 1000)

    # naive Negamax (depth limited)  -- No Transposition Table
    def negamax(self,depth,alpha,beta,colour):
        # Timeout handling
        self.time_end = self.curr_millisecond_time()
        if self.time_end - self.time_start > self.time_rem:
            raise TimeOut

        opponent = Board.get_opp_piece_type(colour)
        dic = {self.player: 1, self.opponent: -1}

        # generate legal actions
        actions_1 = self.board.update_actions(self.board, colour)
        # print(len(actions))
        actions = self.board.sort_actions(actions_1, colour)

        # terminal test -- default case
        if self.cutoff_test(depth):
            val = self.evaluate_state(self.board, self.player, actions)*dic[colour]
            return val, None

        # do the minimax search
        best_val = -inf
        best_action = None

        # generate legal actions
        #actions = self.board.update_actions(self.board, colour)
        # split the actions into favourable an unfavourable
        # if the length of actions is greater than X, then we can just choose to look through the first
        # 5 'favourable' actions that we see right now
        # if the length of actions is less than X, then we can just evaluate all possible actions we have
        # THIS IS A GREEDY APPROACH TO MINIMAX THAT LIMITS OUR BRANCHING FACTOR OF THE GAME
        if len(actions) > 8:
            favourable = actions[:8]
        else:
            favourable = actions
        # got here
        #print("got here")
        # depth reduction
        R = 2
        #print(favourable)
        #self.board.print_board()
        for action in favourable:

            self.board.update_board(action, colour)
            if action in favourable:
                score, temp = self.negamax(depth-1, -beta, -alpha, opponent)
            else:
                score, temp = self.negamax(depth-1-R, -beta, -alpha, opponent)

            score = -score

            if score > best_val:
                best_val = score
                best_action = action

            if score > alpha:
                alpha = score

            self.undo_move()

            if alpha >= beta:
                break

        return best_val, best_action

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

    def evaluate_state(self, board, colour, actions):
        #return Evaluation.basic_policy(board,colour)
        return self.evaluation.evaluate(board,colour,actions)

    # update the available moves of the search algorithm after it has been instantiated
    #
    # def update_available_moves(self, node, available_moves):
    #    node.available_moves = available_moves

    def update_board(self, board):
        self.board = deepcopy(board)

    def is_terminal(self):
        return self.board.is_terminal()

    def undo_move(self):
        return self.board.undo_move()
        # then we need to recalculate the available moves based on the board representation
        # self.generate_actions()
