'''
* Class to implement the different features of a game -- this is going
* to be used for the evaluation function of a board state
* Therefore we need to investigate different features of the board game
* whether this be through simulation via MCTS or by playing the games a number of time s
'''
from Board.Board import Board

class Features(object):
    @staticmethod
    def dist_to_piece(board, move):
        pass

    @staticmethod
    #what to do if colour has middle 4 pieces in final stage
    def final_captures(board):
        pass

    #binary - does colour have middle 4 // better to check middle 4 squares if they're taken
    @staticmethod
    def middle_pieces(board,colour):
        out = [0,0,0,0]
        for piece in board.piece_pos[colour]:
            if piece == (3,3):
                out[0] = 1
            if piece == (3,4):
                out[1] = 1
            if piece == (4,3):
                out[2] = 1
            if piece == (4,4):
                out[3] = 1

        for i in out:
            if (i == 0):
                return False
        return True

    # how many moves from capturing an opponent piece -- from a particular action what is the minimum number of moves to capture a single/two pieces of the opponent
    # assumption relaxed such that current piece just needs to be next to opponent piece
    # we assume that the opponent is not moving and no pieces in the way
    # only use this evaluation function in the moving phase
    @staticmethod
    def min_dist_to_capture_piece(board, colour):
        min_distance = 14 #14 is maximum

        return min_distance

    #number of pieces
    @staticmethod
    def number_of_pieces(board, colour):
        return len(board.piece_pos[colour])

    #net number of pieces, if > 0, our player has more pieces than the opponent, if < 0 the opponent has more pieces.
    @staticmethod
    def net_number_of_pieces(board, colour):
        return Features.number_of_pieces(colour) - Features.number_of_pieces(board.get_opp_piece_type(colour))

    #compare number of moves to get all pieces on edge out of edge to move counter
    @staticmethod
    def edge_moves_to_shrink(board, colour): #Doesn't account for blocked moves yet
        count = 0
        size1 = 8
        start1 = 0
        end1 = 7
        size2 = 6
        start2 = 1
        end2 = 6

        if (count < 128):
            moves_until_shrink = 128 - board.move_counter
            for piece in board.piece_pos[colour]:
                    for i in range(size1):
                        if piece in ((start1,i), (i,start1), (end1, i), (i, end1)):
                        count += 1
        elif (count < 196):
            moves_until_shrink = 196 - board.move_counter
            for piece in board.piece_pos[colour]:
                for i in range(size2):
                    if (piece in ((start2,i), (i,start2), (end2, i), (i, end2))):
                        count += 1

        #shows how many 'spare' moves we have before we'd need to evacuate pieces from edge before they are taken
        return count - moves_until_shrink


    @staticmethod
    def diff_pieces(board, colour):
        # this is the difference of the number of pieces relative to a specified colour on the board
        return len(board.piece_pos[colour]) - len(board.piece_pos[board.get_opp_piece_type(colour)])

    @staticmethod
    # board is the current board state
    # colour is the current nodes player colour
    def self_elim(board,colour):
        # check if the move has eliminated its own piece therefore in the previous
        elim = Board.eliminated_pieces_last_move(board, board.phase,board.move_counter, colour)
        for piece in elim:
            if len(elim[colour]) > 0:
                return True
            else:
                return False

    @staticmethod
    def piece_elim_pattern(self,piece):
        pass
