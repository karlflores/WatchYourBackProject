'''
* Class to implement the different features of a game -- this is going
* to be used for the evaluation function of a board state
* Therefore we need to investigate different features of the board game
* whether this be through simulation via MCTS or by playing the games a number of time s
'''

class Features(object):
    @staticmethod
    def dist_to_piece(board,move):
        pass

    @staticmethod
    #what to do if colour has middle 4 pieces in final stage
    def final_captures(board):
        pass

    #binary - does colour have middle 4
    def middle_pieces(board):
        pass

    #implement massacre as a count for how many moves would be taken to eliminate all but 1 piece of opponent if no moves were made by them
    def massacre_1left(board):
        pass

    #how many moves from capturing an opponent piece
    def min_dist_to_capture(board):
        pass

    #number of pieces
    def number_of_pieces(board):
        pass

    #compare number of moves to get all pieces on edge out of edge to move counter
    def edge_moves_to_shrink(board):
        pass
