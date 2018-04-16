from Board.Board import Board

class Evaluation(object):
    @staticmethod
    def basic_policy(board):
        # assume that the board is in a byte string representation
        board.get