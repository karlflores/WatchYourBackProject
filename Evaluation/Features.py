'''
* Class to implement the different features of a game -- this is going
* to be used for the evaluation function of a board state
'''

from math import fabs, inf, sqrt
from Constants import constant

class Features(object):

    @staticmethod
    def diff_pieces(board, colour):

        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces
            opposition_pieces = board.black_pieces
        else:
            my_pieces = board.black_pieces
            opposition_pieces = board.white_pieces

        # this is the difference of the number of pieces relative to a specified colour on the board
        return len(my_pieces) - len(opposition_pieces)

    @staticmethod
    def total_dist_to_center(board, colour):
        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces
        else:
            my_pieces = board.black_pieces

        dist_cent = 0
        for pieces in my_pieces:
            dist_cent += Features.cart_distance(pieces, (3.5,3.5))

        return 1/(1+dist_cent)

    # number of actions the player can make -- if we have less actions to make
    # this may not be good, but this is not as important as every other feature therefore this should
    # be weighted the least
    @staticmethod
    def num_actions(actions):
        return len(actions)

    @staticmethod
    # cartesian distance
    def cart_distance(pos_1, pos_2):
        return sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)

    @staticmethod
    def manhattan_dist(piece1,piece2):
        return fabs(piece1[0]-piece2[0]) + fabs(piece1[1]-piece2[1])

    @staticmethod
    def min_manhattan_dist(board, action, colour):
        if colour == constant.WHITE_PIECE:
            opposition_pieces = board.black_pieces
        else:
            opposition_pieces = board.white_pieces

        # provided a piece to move check if this piece is close to any of the opponent pieces on the board
        # if we are in the moving phase, we don't want to move any piece that is far from the opponent unless
        # we need to
        # only really should move the pieces that are close to the opponent, thus we can reduce the branching factor
        # this way
        # extract the piece to move from the
        if board.phase == constant.MOVING_PHASE:
            piece = action[0]
        else:
            piece = action

        # if there are no opponents on the board, then we can return 0
        if len(opposition_pieces) == 0:
            return 0

        min_dist = inf

        # loop through each pieces
        for opp_piece in opposition_pieces:
            dist = Features.manhattan_dist(piece, opp_piece)
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
            # the action must be converted from direction to coord of the new square it will occupy
            new_pos = board.convert_direction_to_coord(action[0],action[1])
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
            if board.check_self_elimination(action, colour, action_eval=True) is not None:
                return True
            else:
                return False

        if board.phase == constant.MOVING_PHASE:
            # the action must be converted from direction to coord of the new square it will occupy
            new_pos = board.convert_direction_to_coord(action[0], action[1])
            if board.check_self_elimination(new_pos, colour, action_eval=True) is not None:
                return True
            else:
                return False

    @staticmethod
    def surrounded(board,piece,colour):
        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces
            opposition_pieces = board.black_pieces
        else:
            my_pieces = board.black_pieces
            opposition_pieces = board.white_pieces
        # check if a piece is surrounded by the opposite colour
        opponent = board.get_opp_piece_type(colour)
        if len(opposition_pieces) < 3:
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
        if (col-1, row-1) in opposition_pieces and (col-1, row+1) in opposition_pieces\
                and (col+1, row+1) in opposition_pieces and (col+1, row-1) in opposition_pieces:
            return True

        return False

    @staticmethod
    # the number of my pieces that are surrounded by opponents -- this is bad
    def check_board_surrounded_my_piece(board,colour):
        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces
        else:
            my_pieces = board.black_pieces

        # check if there are any opponent pieces that surround you piece
        num_surround = 0
        for piece in my_pieces:
            if Features.surrounded(board,piece,colour):
                num_surround += 1
        return num_surround

    @staticmethod
    def check_board_surround_opponent(board,colour):
        if colour == constant.WHITE_PIECE:
            opposition_pieces = board.black_pieces
        else:
            opposition_pieces = board.white_pieces

        num_surround = 0
        opponent = board.get_opp_piece_type(colour)
        for piece in opposition_pieces:
            if Features.surrounded(board,piece,opponent):
                # check if any opponent pieces are surrounded by our pieces
                num_surround += 1

        return num_surround

    # can we make an action that surrounds another piece , if we can then this is good to do
    @staticmethod
    def can_action_surround(board, action, colour):
        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces
            opposition_pieces = board.black_pieces
        else:
            my_pieces = board.black_pieces
            opposition_pieces = board.white_pieces

        # if there is less than 3 pieces of your colour on the board, then return false
        if len(my_pieces) < 3:
            return False
            # check if a piece is surrounded by the opposite colour

        if board.phase == constant.PLACEMENT_PHASE:
            pos = action

        elif board.phase == constant.MOVING_PHASE:
            pos = board.convert_direction_to_coord(action[0],action[1])


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
        if (col + 1, row + 1) in opposition_pieces and (col + 2, row) in my_pieces \
                and (col, row + 2) in my_pieces and (col + 2, row + 2) in my_pieces:
            return True
        # bottom left
        if (col + 1, row - 1) in opposition_pieces and (col + 2, row) in my_pieces \
                and (col, row - 2) in my_pieces and (col, row - 2) in my_pieces:
            return True
        # bottom right
        if (col - 1, row - 1) in opposition_pieces and (col, row - 2) in my_pieces \
                and (col - 2, row) in my_pieces and (col - 2, row - 2) in my_pieces:
            return True
        # top right
        if (col - 1, row + 1) in opposition_pieces and (col, row + 2) in my_pieces \
                and (col - 2, row) in my_pieces and (col - 2, row + 2) in my_pieces:
            return True

        # if none of these are true, then the whole thing is not true
        return False

    @staticmethod
    def cluster_exists(board,colour):
        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces
            opposition_pieces = board.black_pieces
        else:
            my_pieces = board.black_pieces
            opposition_pieces = board.white_pieces
        # if we can form a cluster on the board
            # define a cluster to be a 2 x 2 area on the board that you occupy
            # just need to check top left -- if that is in a cluster then we are good
        num_cluster = 0
        for piece in my_pieces:
            col, row = piece

            if (col+1,row) in my_pieces and (col,row+1) in my_pieces\
                    and (col+1,row+1) in my_pieces:
                num_cluster += 1

        return num_cluster

    @staticmethod
    def can_form_cluster(board,action,colour):
        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces
            opposition_pieces = board.black_pieces 
        else: 
            my_pieces = board.black_pieces
            opposition_pieces = board.white_pieces 
        
        if len(my_pieces) < 3:
            return False
            # check if a piece is surrounded by the opposite colour

        if board.phase == constant.PLACEMENT_PHASE:
            pos = action

        elif board.phase == constant.MOVING_PHASE:
            pos = board.convert_direction_to_coord(action[0], action[1])

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
        if (col + 1, row) in my_pieces \
                and (col - 1, row) in my_pieces and (col + 1, row + 1) in my_pieces:
            return True
        # bottom left
        if (col - 1, row) in my_pieces \
                and (col - 1, row + 1) in my_pieces and (col, row + 1) in my_pieces:
            return True
        # bottom right
        if (col, row - 1) in my_pieces \
                and (col + 1, row) in my_pieces and (col + 1, row - 1) in my_pieces:
            return True
        # top right
        if (col - 1, row) in my_pieces \
                and (col - 1, row - 1) in my_pieces and (col, row - 1) in my_pieces:
            return True

        # if none of these are true, then the whole thing is not true
        return False

    @staticmethod
    def occupy_middle(board,action,colour):

        if board.phase == constant.PLACEMENT_PHASE:
            pos = action

        elif board.phase == constant.MOVING_PHASE:
            pos = board.convert_direction_to_coord(action[0], action[1])

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
        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces
            opposition_pieces = board.black_pieces
        else:
            my_pieces = board.black_pieces
            opposition_pieces = board.white_pieces

        middle = [(3,3),(3,4),(4,3),(4,4)]
        net_val = 0

        for piece in middle:
            if piece in my_pieces:
                net_val += 10
            elif piece in opposition_pieces:
                net_val -= 20

        return net_val

    @staticmethod
    # count the number of pieces are at the edge of the board
    def edge_vulnerable_pieces(board,colour):
        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces

        else:
            my_pieces = board.black_pieces

        edges = {}
        num = 0
        # count the number of edge pieces
        for i in range(board.min_dim,board.max_dim+1):

            left_edge = (board.min_dim,i)
            right_edge = (board.max_dim,i)
            top_edge = (i,board.min_dim)
            bottom_edge = (i,board.max_dim)

            if left_edge in my_pieces:
               num += 1
            if right_edge in my_pieces:
                num += 1
            if top_edge in my_pieces:
                num += 1
            if bottom_edge in my_pieces:
                num += 1

        # next shrink
        next_corners = [(board.min_dim+1,board.min_dim+1),
         (board.min_dim+1, board.max_dim-1),
         (board.max_dim+1, board.max_dim-1),
         (board.max_dim-1, board.max_dim-1)]

        # count the number of pieces that are at the new corner positions
        for corner in next_corners:
            if corner in my_pieces:
                num += 1

        return num

    # returns the difference in the number of pieces of opponent pieces at an edge vs our pieces at an edge
    @staticmethod
    def diff_edge_vulnerable(board,colour):
        opponent = board.get_opp_piece_type(colour)
        if board.phase == constant.MOVING_PHASE:
            if 112 < board.move_counter < 128:
                # double the weight of any enemy players because we don't want to return zero if we have our pieces
                # at the edges
                return 2*Features.edge_vulnerable_pieces(board,opponent) - Features.edge_vulnerable_pieces(board,colour)

            if 176 < board.move_counter < 192:
                return 2*Features.edge_vulnerable_pieces(board,opponent) - Features.edge_vulnerable_pieces(board,colour)

            # if we are not near the shrink we do no care about this
            return 0

        # if we not in placing phase we do not care about this
        return 0

    # count the number of pieces next to the corners
    @staticmethod
    def place_next_to_corner(board,colour):
        num = 0
        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces

        else:
            my_pieces = board.black_pieces

        # left corner
        top_L, top_R, bot_L, bot_R = board.corner_pos

        if colour == constant.WHITE_PIECE:
            piece_1 = board.convert_direction_to_coord(top_L, 0)
            piece_2 = board.convert_direction_to_coord(top_L, 1)
            piece_3 = board.convert_direction_to_coord(top_R, 2)
            piece_4 = board.convert_direction_to_coord(top_R, 1)

            if piece_1 in my_pieces:
                num += 1
            if piece_2 in my_pieces:
                num += 1
            if piece_3 in my_pieces:
                num += 1
            if piece_4 in my_pieces:
                num += 1

        else:
            piece_1 = board.convert_direction_to_coord(bot_L, 3)
            piece_2 = board.convert_direction_to_coord(bot_L, 1)
            piece_3 = board.convert_direction_to_coord(bot_R, 3)
            piece_4 = board.convert_direction_to_coord(bot_R, 2)

            if piece_1 in my_pieces:
                num += 1
            if piece_2 in my_pieces:
                num += 1
            if piece_3 in my_pieces:
                num += 1
            if piece_4 in my_pieces:
                num += 1

        return num

    # if we have the centre position or not
    @staticmethod
    def center_hold(board,colour):

        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces

        else:
            my_pieces = board.black_pieces

        # check if we currently occupy the middle positions
        if (4,4) in my_pieces and (3,4) in my_pieces and (4,3) in my_pieces and (3,3) in my_pieces:
            # top pieces
            return 1
        else:
            return 0

    # get the minimum distance of each piece to an ememy piece, add these distances together
    # therefore this is a measure of how close our piece is to an enemy piece. In the later stages we
    # want to move towards enemy pieces to capture them therefore this should take that into consideration
    @staticmethod
    def total_min_man_dist(board,colour):
        total = 0
        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces
            opposition_pieces = board.black_pieces

        else:
            my_pieces = board.black_pieces
            opposition_pieces = board.white_pieces

        # only take this into consideration in the moving phase of the game
        if board.phase == constant.MOVING_PHASE and board.move_counter > 30:
            total = 0
            for pos in my_pieces:
                if len(opposition_pieces) == 0:
                    return 0

                min_dist = inf
                # loop through each pieces
                for opp_piece in opposition_pieces:
                    dist = Features.manhattan_dist(pos, opp_piece)
                    # get the min distance
                    min_dist = min(min_dist, dist)

                total += min_dist

        return total

    '''
    ELIM PATTERN IS AS FOLLOWS 
       (1)   |   (2)  |   (3)    |   (4)
        B    |    B   |          |         |{  These patterns are good to establish as they ensure that we are able to 
        WW   |   WW   |    BW    |    BW   |{  capture a piece. Therefore if we can form these patterns it will be a
         B   |   B    |     WB   |   WB    |{  benefit to us to do so 
    '''
    @staticmethod
    def check_elim_pattern(board, colour):
        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces
            opposition_pieces = board.black_pieces
        else:
            my_pieces = board.black_pieces
            opposition_pieces = board.white_pieces

        num_pattern = 0

        for piece in my_pieces:
            col,row = piece

            # check pattern 1


    @staticmethod
    def form_elim_patther(board, colour):
        if colour == constant.WHITE_PIECE:
            my_pieces = board.white_pieces
            opposition_pieces = board.black_pieces
        else:
            my_pieces = board.black_pieces
            opposition_pieces = board.white_pieces

'''
LOOK AT TIMING SCHEMES
'''