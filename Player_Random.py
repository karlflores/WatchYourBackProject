from Constants import constant
from WatchYourBack.Board import Board
from Error_Handling.Errors import *
from random import randint

class Player:

    def __init__(self, colour):
        if colour == 'white':
            self.colour = constant.WHITE_PIECE
        elif colour == 'black':
            self.colour = constant.BLACK_PIECE

        # each players internal board representation
        self.board = Board()

        self.opponent = self.board.get_opp_piece_type(self.colour)

    def update(self, action):

        # update the board based on the action of the opponent
        # get move type
        if self.board.phase == constant.PLACEMENT_PHASE:
            self.board.update_board(action, self.opponent)

        elif self.board.phase == constant.MOVING_PHASE:
            if isinstance(action[0],tuple) is False:
                raise InvalidAction

            direction = self.board.convert_coord_to_direction(action[0], action[1])
            self.board.update_board((action[0], direction), self.opponent)
        # print("UPDATE BOARD _______________________________")
        # print(self.board)
        # print("UPDATE BOARD _______________________________")

    def action(self, turns):
        available_actions = self.board.update_actions(self.colour)
        next_action = available_actions[randint(0,len(available_actions)-1)]

        if self.board.phase == constant.PLACEMENT_PHASE:
            # making moves during the placement phase
            self.board.update_board(next_action, self.colour)
            # print(next_action)
            return next_action
        else:
            new_pos = self.board.convert_direction_to_coord(next_action[0],next_action[1])
            # making moves during the placement phase
            # print(next_action)
            self.board.update_board(next_action, self.colour)
            #print(next_action)
            return next_action[0], new_pos
