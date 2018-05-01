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

        # best move path
        self.best_move_path = []

        # data structures for machine learning
        self.eval_depth = 0
        self.minimax_val = 0
        self.policy_vector = []

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
        available_actions = self.board.update_actions(self.board, self.player)
        # available_actions = self.move_ordering(available_actions,self.player)

        # self.actions_leftover = self.board.update_actions(self.board, self.player)

        if len(available_actions) == 0:
            return None
        else:
            # lets just set the default to the first move
            move = available_actions[0]

        # time allocated per move in ms
        time_alloc = constant.TIME_CUTOFF_AB

        # get time
        start_time = MinimaxABOptimised.curr_millisecond_time()
        best_depth = 1
        # iterative deepening begins here
        for depth in range(1, MAX_ITER):
            print(depth)
            # invalidate / clear the cache when increasing the search depth cutoff
            self.min_value.cache_clear()
            #self.max_value.cache_clear()
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

            best_depth += 1
            sleep(0.05)
            if MinimaxABOptimised.curr_millisecond_time() - start_time > time_alloc:
                break

        self.eval_depth = best_depth
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

        best_move = None
        alpha = -inf
        evaluate = -inf
        beta = inf

        # get the available moves of the board (based on the current board representation)
        # we can generate the actions as we wish -- this can easily change -- TODO : OPTIMISATION/ PRUNING OF ACTION __ CAN BE GREEDY __ favoured moves and unfavoured moves
        self.actions_leftover = self.board.update_actions(self.board, self.player)
        # self.actions_leftover = self.move_ordering(self.actions_leftover,self.player)
        # self.actions_leftover = self.move_ordering(self.actions_leftover,self.player)
        # self.actions_leftover = self.board.update_actions(self.board,self.player)

        for action in available_actions:
            # clear the best move path
            self.best_move_path = []

            # update the minimax board representation with the action
            self.board.update_board(action, self.player)

            # get the board representation for caching
            board_string = self.board.board_state.decode("utf-8")

            ab_evaluate = self.min_value(board_string, self.opponent, self.board.phase, depth - 1)

            heapq.heappush(self.actions_evaluated, (ab_evaluate, action))
            self.actions_leftover.remove(action)

            if ab_evaluate > evaluate:
                best_move = action
                evaluate = ab_evaluate

            self.undo_move()

            if evaluate >= beta:
                self.minimax_val = evaluate
                return best_move

            alpha = max(alpha, evaluate)

        self.minimax_val = evaluate
        return best_move

    # memoize the function call -- opitimisation
    #@lru_cache(maxsize=10000)
    def max_value(self,board_string, colour, phase, depth):

        evaluate = -inf

        best_move = None

        if self.cutoff_test(depth):
            return self.evaluate_state(self.board)

        # visit each available move
        available_actions = self.board.update_actions(self.board, colour)
        # available_actions = self.move_ordering(available_actions, colour)

        for action in available_actions:

            # update the board representation with the move
            self.board.update_board(action, colour)

            # create an immutable object for board_string such that we can call lru_cache on the max function call
            board_string = self.board.board_state.decode("utf-8")

            # get the minimax value for this state
            eval_before = evaluate
            evaluate = max(evaluate, self.min_value(board_string, self.opponent, self.board.phase, depth-1))
            # check if we have changed the minimax value -- therefore we need to change the best move
            if eval_before != evaluate:
                best_move = action

            # undo the move so that we can apply another action
            self.undo_move()

            if evaluate >= self.beta:
                # append the best move that we have found to the list
                self.best_move_path.append((action, colour))
                return evaluate

            self.alpha = max(evaluate, self.alpha)

        self.best_move_path.append((best_move, colour))
        return evaluate

    # memoize the min value results -- optimisation of its function call
    @lru_cache(maxsize=100000)
    def min_value(self, board_string, colour, phase, depth):

        # beginning evaluation value
        evaluate = inf
        best_move = None

        if self.cutoff_test(depth):
            return self.evaluate_state(self.board)

        # generate the actions to search on
        available_actions = self.board.update_actions(self.board, colour)
        # available_actions = self.move_ordering(available_actions,colour)

        for action in available_actions:

            # update the board representation -- this action is the min nodes's action
            self.board.update_board(action, colour)

            board_string = self.board.board_state.decode("utf-8")

            # find the value of the max node
            eval_before = evaluate
            evaluate = min(evaluate, self.max_value(board_string, self.player, self.board.phase, depth - 1))
            if eval_before != evaluate:
                best_move = action

            # undo the board move so that we can apply another move
            # -- we also go up a level therefore we need to increment depth
            self.undo_move()

            '''
            if beta <= alpha:
                # when we break from the loop make sure to undo the move
                break
            '''

            if evaluate <= self.alpha:
                self.best_move_path.append((action,colour))
                return evaluate

            self.beta = min(self.beta, evaluate)

        self.best_move_path.append((best_move, colour))
        return evaluate

    def cutoff_test(self, depth):
        if depth == 0:
            return True

        if self.is_terminal():
            return True

        return False

    def move_ordering(self, actions, colour):
        # get the available moves for this board phase
        weighted_actions = []
        final = []

        for action in actions:
            self.board.update_board(action,colour)

            val = Evaluation.basic_policy(self.board, colour)
            self.undo_move()
            weighted_actions.append((val,action))
            #
        heapq._heapify_max(weighted_actions)

        while len(weighted_actions) > 0:
            action = heapq._heappop_max(weighted_actions)
            final.append(action[1])

        #print(final)
        #print()
        #print()
        return final
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


    '''
    Begin the Nega-Scout Implementation 
    '''
    '''
    def nega_scout(self,board_state,colour,phase,depth):
        # default case - cut off test
        if self.cutoff_test(depth):
            self.evaluate_state(self.board)
        
        b = self.beta 
        best_score = -inf 
        
        # generate moves 
        available_actions = self.board.update_actions(self.board,colour)
        
        for i in range(len(available_actions)): 
            # get the action 
            action = available_actions[i]
            
            self.board.update_board(action, colour)
            
            val = -self.nega_scout(self.board.board_state,Board.get_opp_piece_type(colour),self.board.phase, depth-1)
            if (val > self.alpha) and (val < self.beta) and (i > 0) :
                self.alpha = - val
                self.beta = - self.beta 
                val = -self.nega_scout(self.board.board_state, Board.get_opp_piece_type(colour), self.board.phase, depth - 1)
                
        
    '''

    # naive implementation of Nega Scout
    def nega_scout_value(self,alpha,beta,depth,colour):

        colour_arr = {self.player: 1, self.opponent: -1}

        if self.cutoff_test(depth):
            return self.evaluate_state(self.board)

        # generate moves
        available_actions = self.board.update_actions(self.board, colour)

        for i in range(len(available_actions)):
            opponent = Board.get_opp_piece_type(colour)
            action = available_actions[i]
            # apply the move to the board
            self.board.update_board(action, opponent)

            # evaluate the first move -- assume in iterative deepening that this move is
            # the best move so far
            score = -self.nega_scout_value(-beta, -alpha, depth-1, opponent)

            # nega-scout condition on all other moves but the best move
            # scout the rest of the moves
            if i > 0:
                score = -self.nega_scout_value(-alpha-1,-alpha,depth-1,opponent)
                if alpha < score < beta:
                    score = -self.nega_scout_value(-beta, -score, depth-1, opponent)

            # get alpha value
            # undo the move so that we can apply another move
            self.undo_move()
            alpha = max(alpha, score)

            # undo the move so that we can apply another move -- AB cutoff
            if alpha >= beta:
                return alpha

        return alpha

    def nega_scout(self, depth, available_actions):
        self.actions_evaluated = []
        '''
        if self.board.phase == constant.MOVING_PHASE and self.board.move_counter == 0:
            self.min_value.cache_clear()
            # self.max_value.cache_clear()
        '''

        best_move = None
        best_score = -inf
        alpha = -inf
        beta = inf

        # get the available moves of the board (based on the current board representation)
        # we can generate the actions as we wish -- this can easily change -- TODO : OPTIMISATION/ PRUNING OF ACTION __ CAN BE GREEDY __ favoured moves and unfavoured moves
        self.actions_leftover = self.board.update_actions(self.board, self.player)
        # self.actions_leftover = self.board.update_actions(self.board,self.player)

        for i in range(len(available_actions)):
            action = available_actions[i]
            # update the minimax board representation with the action
            self.board.update_board(action, self.player)

            # get the board representation for caching
            # board_string = self.board.board_state.decode("utf-8")

            score = -self.nega_scout_value(-beta,-alpha, depth-1, self.opponent)

            if i > 0:
                score = -self.nega_scout_value(-alpha-1, -alpha, depth-1, self.opponent)

                if alpha < score < beta:
                    score = -self.nega_scout_value(-beta, -score, depth-1, self.opponent)

            self.undo_move()

            alpha = max(alpha, score)

            if best_score > score:
                best_move = action
            else:
                best_score = score

            if alpha >= beta:
                best_score = alpha
                break

        print(best_move)
        heapq.heappush(self.actions_evaluated, (alpha, best_move))
        self.actions_leftover.remove(best_move)

        self.minimax_val = best_score
        return best_move

    def iterative_deepening_nega_scout(self):

        '''
        I dont think this is working correctly -- i believe when things are getting cached because it doesnt take in consideration the depth of the call of that minimax evaluation
        we need to take into consideration the depth for it to call correctly

        need to change this
        '''
        MAX_ITER = 4

        # default policy
        available_actions = self.board.update_actions(self.board,self.player)
        # self.actions_leftover = self.board.update_actions(self.board, self.player)

        if len(available_actions) == 0:
            return None
        else:
            # lets just set the default to the first move
            move = available_actions[0]

        # time allocated per move in ms
        time_alloc = constant.TIME_CUTOFF_AB

        # get time
        start_time = MinimaxABOptimised.curr_millisecond_time()
        best_depth = 1
        # iterative deepening begins here
        for depth in range(1, MAX_ITER):
            print(depth)
            # invalidate / clear the cache when increasing the search depth cutoff
            # self.min_value.cache_clear()
            #self.max_value.cache_clear()
            # peform the search
            move = self.nega_scout(depth, available_actions)

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

            best_depth += 1

            if MinimaxABOptimised.curr_millisecond_time() - start_time > time_alloc:
                break

        self.eval_depth = best_depth
        return move

    def negamax_val(self,depth,alpha,beta,player):

        opponent = Board.get_opp_piece_type(player)
        colour_arr = {self.player: 1, self.opponent: -1}

        if self.cutoff_test(depth):
            # if we are at the max depth child we return the evaluation of this state
            return self.evaluate_state(self.board)*colour_arr[player], None

        best_value = -inf
        best_action = None
        # generate all moves
        actions = self.board.update_actions(self.board, player)

        for action in actions:
            self.board.update_board(action,player)

            tup = self.negamax_val(depth-1,-beta,-alpha,opponent)
            value = -tup[0]

            prev_val = value
            best_value = max(best_value, value)
            # has the best_value action changed -- if it has we have found a new best_action
            if prev_val != best_value:
                best_action = action

            alpha = max(alpha, value)
            self.undo_move()
            if alpha >= beta:
                # self.best_move_path.append(best_action)
                # best_move = action
                break

        # we should have the best value so far
        self.best_move_path.append((best_action, player))
        return best_value, best_action

    def negamax(self, depth):
        '''
        self.best_move_path = []
        alpha = -inf
        beta = inf
        best_value = alpha
        best_action = None
        colour_arr = {self.player:1,self.opponent:-1}

        # calculate the negamax scores of each of the children states
        actions = self.board.update_actions(self.board,self.player)

        for action in actions:
            self.board.update_board(action, self.player)
            value = -self.negamax_val(depth-1,-beta,-alpha,self.opponent)
            if best_value < value:
                best_value = value
                best_action = action

            self.undo_move()

            if alpha < value:
                alpha = value

            if alpha >= beta:
                break
        '''
        alpha = -inf
        beta = inf
        best_move = self.negamax_val(depth, alpha, beta, self.player)
        best_action = best_move[1]
        # print(self.best_move_path)
        return best_action





