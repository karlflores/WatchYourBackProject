'''
* Class to implement the different features of a game -- this is going
* to be used for the evaluation function of a board state
* Therefore we need to investigate different features of the board game
* whether this be through simulation via MCTS or by playing the games a number of time s
'''
# from Board.Board import Board
from math import fabs, inf, sqrt
from Constants import constant


# from copy import copy

class Features(object):
    @staticmethod
    def dist_to_piece(board, move):
        pass

    @staticmethod
    #what to do if colour has middle 4 pieces in final stage
    def final_captures(board):
        pass

    #binary - does colour have middle 4
    @staticmethod
    def middle_pieces(board):
        pass

    #implement massacre as a count for how many moves would be taken to eliminate all but 1 piece of opponent if no moves were made by them
    @staticmethod
    def massacre_1left(board):
        pass

    #how many moves from capturing an opponent piece -- from a particular action what is the minimum number of moves to capture a single/two pieces of the opponent
    # we assume that the opponent is not moving
    # only use this evaluation function in the moving phase
    @staticmethod
    def min_dist_to_capture_piece(board):
        pass

    #number of pieces
    @staticmethod
    def number_of_pieces(board):
        pass

    #compare number of moves to get all pieces on edge out of edge to move counter
    @staticmethod
    def edge_moves_to_shrink(board):
        pass

    @staticmethod
    def diff_pieces(board, colour):
        # this is the difference of the number of pieces relative to a specified colour on the board
        return len(board.piece_pos[colour]) - len(board.piece_pos[board.get_opp_piece_type(colour)])

    @staticmethod
    def piece_elim_pattern(self,piece):
        pass

    @staticmethod
    def total_dist_to_center(board, colour):
        dist_cent = 0
        for pieces in board.piece_pos[colour]:
            dist_cent += Features.cart_distance(pieces, (3.5,3.5) )

        # number of pieces of the opponent eliminated
        # available_actions = board.update_actions(board,colour)

        # num_moves = len(available_actions)

        # RANDOM MOVES FOR TESTING IF MINIMAX IS WORKING CORRECTLY
        # return randint(0,5)
        return 1/(1+dist_cent)

    @staticmethod
    def num_actions(actions):
        return len(actions)

    @staticmethod
    def cart_distance(pos_1, pos_2):
        return sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)

    @staticmethod
    def manhattan_dist(piece1,piece2):
        return int(fabs(piece1[0]-piece2[0])) + int(fabs(piece1[1]-piece2[1]))

    @staticmethod
    def min_manhattan_dist(board, action, colour):
        # provided a piece to move check if this piece is close to any of the opponent pieces on the board
        # if we are in the moving phase, we don't want to move any piece that is far from the opponent unless
        # we need to
        # only really should move the pieces that are close to the opponent, thus we can reduce the branching factor
        # this way
        opponent = board.get_opp_piece_type(colour)
        # extract the piece to move from the
        if board.phase == constant.MOVING_PHASE:
            piece = action[0]
        else:
            piece = action

        # if there are no opponents on the board, then we can return 0
        if len(board.piece_pos[opponent]) == 0:
            return 0

        min_dist = inf

        # loop through each pieces
        for opp_piece in board.piece_pos[opponent]:
            dist = Features.manhattan_dist(piece,opp_piece)
            min_dist = min(min_dist,dist)

        return min_dist

    @staticmethod
    def dist_to_center(piece):
        return int(fabs(piece[0]-4))+int(fabs(piece[1]-4))

    @staticmethod
    def can_action_capture(board,action,colour):
        # when we apply an action to the board, can we capture a piece, or put our selves in a position
        # that will capture a piece of the opponent
        if board.phase == constant.PLACEMENT_PHASE:
            # the action is a placement on the board -- therefore we just need to check if it can
            # eliminate an opponent piece
            if board.check_one_piece_elimination(action,colour) is not None:
                return True
            else:
                return False

        if board.phase == constant.MOVING_PHASE:
            # the action must be converted from move_Type to coord of the new square it will occupy
            new_pos = board.convert_move_type_to_coord(action[0],action[1])
            if board.check_one_piece_elimination(new_pos,colour) is not None:
                return True
            else:
                return False

    @staticmethod
    def check_self_elimination(board,action,colour):
        # check if we place/move a piece to a specific location, will this piece result in a self elimination
        # if it does then we do not want to do this action
            # is is an unfavourable move, and we should not explore it

        if board.phase == constant.PLACEMENT_PHASE:
            # the action is a placement on the board -- therefore we just need to check if it can
            # eliminate an opponent piece
            if board.check_self_elimination(action, colour) is not None:
                return True
            else:
                return False

        if board.phase == constant.MOVING_PHASE:
            # the action must be converted from move_Type to coord of the new square it will occupy
            new_pos = board.convert_move_type_to_coord(action[0], action[1])
            if board.check_self_elimination(new_pos, colour) is not None:
                return True
            else:
                return False

    @staticmethod
    def surrounded(board,piece,colour):

        # check if a piece is surrounded by the opposite colour
        opponent = board.get_opp_piece_type(colour)
        if len(board.piece_pos[opponent]) < 3:
            return False

        '''
        # if an enemy is in the middle of 4 pieces then this is a good thing 
        # i.e B     B   (y-1,x-1)  (y+1,x-1)
                 W            (y , x)
              B     B   (y=1,x+1)  (y+1,x+1)
              
        then the enemy cannot move anywhere because it will be self eliminated therefore we are in a better 
        position than the enemy 
        '''
        col,row = piece
        if (col-1, row-1) in board.piece_pos[opponent] and (col-1, row+1) in board.piece_pos[opponent]\
                and (col+1, row+1) in board.piece_pos[opponent] and (col+1, row-1) in board.piece_pos[opponent]:
            return True

        return False

    @staticmethod
    def check_board_surrounded_my_piece(board,colour):
        # check if there are any opponent pieces that surround you piece
        num_surround = 0
        for piece in board.piece_pos[colour]:
            if Features.surrounded(board,piece,colour):
                num_surround += 1
        return num_surround

    @staticmethod
    def check_board_surround_opponent(board,colour):
        num_surround = 0
        opponent = board.get_opp_piece_type(colour)
        for piece in board.piece_pos[opponent]:
            if Features.surrounded(board,piece,opponent):
                # check if any opponent pieces are surrounded by our pieces
                num_surround += 1

        return num_surround

    @staticmethod
    def can_action_surround(board, action, colour):
        # if there is less than 3 pieces of your colour on the board, then return false
        if len(board.piece_pos[colour]) < 3:
            return False
            # check if a piece is surrounded by the opposite colour
        opponent = board.get_opp_piece_type(colour)
        if board.phase == constant.PLACEMENT_PHASE:
            pos = action

        elif board.phase == constant.MOVING_PHASE:
            pos = board.convert_move_type_to_coord(action[0],action[1])


        '''
        # if an enemy is in the middle of 4 pieces then this is a good thing 
        # i.e B     B   (y-1,x-1)  (y+1,x-1)
                 W            (y , x)
              B     B   (y-1,x+1)  (y+1,x+1)

        then the enemy cannot move anywhere because it will be self eliminated therefore we are in a better 
        position than the enemy 
        
        
        now just need to check if a piece can occupy the corner locations 
        '''
        col, row = pos
        # top left
        if (col + 1, row + 1) in board.piece_pos[opponent] and (col + 2, row) in board.piece_pos[colour] \
                and (col, row + 2) in board.piece_pos[colour] and (col + 2, row + 2) in board.piece_pos[colour]:
            return True
        # bottom left
        if (col + 1, row - 1) in board.piece_pos[opponent] and (col + 2, row) in board.piece_pos[colour] \
                and (col, row - 2) in board.piece_pos[colour] and (col, row - 2) in board.piece_pos[colour]:
            return True
        # bottom right
        if (col - 1, row - 1) in board.piece_pos[opponent] and (col, row - 2) in board.piece_pos[colour] \
                and (col - 2, row) in board.piece_pos[colour] and (col - 2, row - 2) in board.piece_pos[colour]:
            return True
        # top right
        if (col - 1, row + 1) in board.piece_pos[opponent] and (col, row + 2) in board.piece_pos[colour] \
                and (col - 2, row) in board.piece_pos[colour] and (col - 2, row + 2) in board.piece_pos[colour]:
            return True

        # if none of these are true, then the whole thing is not true
        return False

    @staticmethod
    def cluster_exists(board,colour):
        # if we can form a cluster on the board
            # define a cluster to be a 2 x 2 area on the board that you occupy
            # just need to check top left -- if that is in a cluster then we are good
        num_cluster = 0
        for piece in board.piece_pos[colour]:
            col, row = piece

            if (col+1,row) in board.piece_pos[colour] and (col,row+1) in board.piece_pos[colour]\
                    and (col+1,row+1) in board.piece_pos[colour]:
                num_cluster += 1

        return num_cluster

    @staticmethod
    def can_form_cluster(board,action,colour):
        if len(board.piece_pos[colour]) < 3:
            return False
            # check if a piece is surrounded by the opposite colour

        if board.phase == constant.PLACEMENT_PHASE:
            pos = action

        elif board.phase == constant.MOVING_PHASE:
            pos = board.convert_move_type_to_coord(action[0], action[1])

        '''
        # if an enemy is in the middle of 4 pieces then this is a good thing 
        # X B  B X  B B   B B
          B B  B B  X B   B X

        then the enemy cannot move anywhere because it will be self eliminated therefore we are in a better 
        position than the enemy 


        now just need to check if a piece can occupy the corner locations 
        '''
        col, row = pos
        # top left
        if (col + 1, row) in board.piece_pos[colour] \
                and (col - 1, row) in board.piece_pos[colour] and (col + 1, row + 1) in board.piece_pos[colour]:
            return True
        # bottom left
        if (col - 1, row) in board.piece_pos[colour] \
                and (col - 1, row + 1) in board.piece_pos[colour] and (col, row + 1) in board.piece_pos[colour]:
            return True
        # bottom right
        if (col, row - 1) in board.piece_pos[colour] \
                and (col + 1, row) in board.piece_pos[colour] and (col + 1, row - 1) in board.piece_pos[colour]:
            return True
        # top right
        if (col - 1, row) in board.piece_pos[colour] \
                and (col - 1, row - 1) in board.piece_pos[colour] and (col, row - 1) in board.piece_pos[colour]:
            return True

        # if none of these are true, then the whole thing is not true
        return False

    @staticmethod
    def occupy_middle(board,action,colour):
        if board.phase == constant.PLACEMENT_PHASE:
            pos = action

        elif board.phase == constant.MOVING_PHASE:
            pos = board.convert_move_type_to_coord(action[0], action[1])

        if pos == (3,3) or pos == (4,4) or pos == (3,4) or pos == (4,3):
            return True

        # if none of these are true, then the whole thing is not true
        return False

    @staticmethod
    def in_middle(board,action):
        if board.phase == constant.PLACEMENT_PHASE:
            pos = action

        elif board.phase == constant.MOVING_PHASE:
            pos = action[0]

        if pos == (3,3) or pos == (4,4) or pos == (3,4) or pos == (4,3):
            return True

        # if none of these are true, then the whole thing is not true
        return False

    @staticmethod
    def check_middle(board,colour):
        opponent = board.get_opp_piece_type(colour)
        middle = [(3,3),(3,4),(4,3),(4,4)]
        net_val = 0

        for piece in middle:
            if piece in board.piece_pos[colour]:
                net_val += 10
            elif piece in board.piece_pos[opponent]:
                net_val -= 20

        return net_val

