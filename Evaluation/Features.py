'''
* Class to implement the different features of a game -- this is going
* to be used for the evaluation function of a board state
* Therefore we need to investigate different features of the board game
* whether this be through simulation via MCTS or by playing the games a number of time s
'''

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
