from Board import constant
from math import sqrt
from BoardOOP.Piece import Piece
from Error_Handling.Errors import *
from copy import copy


class Board(object):

    # a class to represent the board state of the game
    def __init__(self):

        # key -- the position of the pieces
        # value -- the piece object
        # when we place a piece on the board we update pieces_remaining and we look at any neighbours in a 2 block radius
        # we need to update these pieces neighbour positions to being False -- a
        self.white_pieces = {}
        self.white_eliminate_pieces = []

        self.black_pieces = {}
        self.black_eliminate_pieces = []

        self.free_sqaures = {}

        self.places_remaining = {constant.WHITE_PIECE: 12, constant.BLACK_PIECE: 12}

        # initialise the board representation
        # LT RT LB RB
        self.corner_pos = [(0, 0), (7, 0), (0, 7), (7, 7)]

        # how many moves have been applied to the board so far
        self.move_counter = 0
        self.phase = constant.PLACEMENT_PHASE
        self.num_shrink = 0

        # initially no one wins
        self.winner = None
        self.terminal = False

        # who is moving first
        self.player_to_move = None

        # current size of the board
        self.min_dim = 0
        self.max_dim = constant.BOARD_SIZE-1

        # initialise the board with the corner pieces
        # this dictionary keeps track of the board and the pieces that are currently on the board
        # define the board parameters and constants
        self.board_state = self.init_board_rep()

    def init_board_rep(self):
        # store the board representation as a byte_array length 64 (64bytes)
        temp = ''
        for index in range(constant.BOARD_SIZE * constant.BOARD_SIZE):
            temp += constant.FREE_SPACE
        # create a temp string of length 64
        temp = bytearray(temp,'utf-8')

        # set the corner locations on the board representation

        for col,row in self.corner_pos:
            self.set_array_char(temp, row, col, constant.CORNER_PIECE)

        return temp

# string_array helper methods
    @staticmethod
    def get_array_element(byte_array,row,col):
        # we assume that the string array is n x n in dimension

        # get the dimension
        dimension = constant.BOARD_SIZE
        # check if row and col are valid
        if row > dimension - 1 or col > dimension - 1:
            return None

        elif row < 0 or col < 0:
            return None
        # get the index to access in the string
        index = row*dimension + col

        # return the char at position index
        return chr(byte_array[index])

    @staticmethod
    def set_array_char(byte_array, row, col, new_char):
        dimension = constant.BOARD_SIZE

        if row > dimension - 1 or col > dimension - 1:
            return
        elif row < 0 or col < 0:
            return

        # set the new char in the string
        # need to turn char into utf-8 encoding first
        byte_array[row * dimension + col] = ord(new_char)

    # return the current size of the board
    def get_min_dim(self):
        return self.min_dim

    def get_max_dim(self):
        return self.max_dim

    # board representation setters and getter methods
    def get_board_piece(self, row, col):
        return self.get_array_element(self.board_state, row, col)

    # change the piece type in the board representation
    def set_board(self, row, col, piece_type):
        piece_types = (constant.CORNER_PIECE, constant.WHITE_PIECE, constant.BLACK_PIECE,
                       constant.FREE_SPACE, constant.INVALID_SPACE)
        # check if the piece_type is valid
        if piece_type not in piece_types:
            return

        # if valid we can set the board position
        self.set_array_char(self.board_state, row, col, piece_type)

    # print board method
    def print_board(self):

        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                # get the char to print
                char_index = row * constant.BOARD_SIZE + col

                char = chr(self.board_state[char_index])
                print('{} '.format(char), end='')

            print()

    # when we add a piece back to the board -- this will automatically take care of updating the neighbour
    # therefore move generation should still happen in constant time -- we don't need to test if squares are free
    # or not as this should handle it
    def add_piece(self,pos,colour):
        try:
            new_piece = Piece(pos,colour,self)
            col, row = pos
            new_piece_entry = {pos: new_piece}

            if colour == constant.WHITE_PIECE:
                self.white_pieces.update(new_piece_entry)
                # update the board representation string
                self.set_board(row,col,constant.WHITE_PIECE)
            else:
                self.black_pieces.update(new_piece_entry)
                self.set_board(row,col,constant.BLACK_PIECE)

            # once we add ths piece to the board, we need to update its neighbours
            for direction in range(constant.MAX_MOVETYPE):
                # check if there are any pieces that are occupying nearby squares
                new_pos = self.convert_move_type_to_coord(pos,direction)

                # get the direction for the new_position from the old position
                opp_direction = self.get_opposite_direction(direction)

                if new_pos in self.black_pieces:
                    # update this pieces neighbour list
                    piece = self.black_pieces[new_pos]
                    # this space is now occupied therefore set the neighbour to false -- can no longer move here
                    piece.set_neighbour(opp_direction, False)
                elif new_pos in self.white_pieces:
                    piece = self.white_pieces[new_pos]
                    piece.set_neighbour(opp_direction, False)

        except IllegalPlacement:
            print("Illegal Piece Placement... at ({}, {})".format(pos[1],pos[0]))

    # elimination checkers -- TODO: need to change this to work with this board representation
    def perform_elimination(self, my_piece_pos, colour):
        eliminated_pieces = []

        # get the opponent piece type
        opponent = self.get_opp_piece_type(colour)

        if colour == constant.WHITE_PIECE:
            my_pieces = self.white_pieces
            my_elim_pieces = self.white_eliminate_pieces
            opponent_pieces = self.black_pieces
            opp_elim_pieces = self.black_eliminate_pieces
        elif colour == constant.BLACK_PIECE:
            my_pieces = copy(self.black_pieces)
            my_elim_pieces = self.black_eliminate_pieces
            opponent_pieces = copy(self.white_pieces)
            opp_elim_pieces = self.white_eliminate_pieces

        while self.check_one_piece_elimination(my_piece_pos, colour) is not None:
            # check if this piece has eliminated an opponent
            elim_pos = self.check_one_piece_elimination(my_piece_pos, colour)

            # want to eliminate about the opposition's piece
            if elim_pos in opponent_pieces:
                # get the eliminated piece
                elim_piece = opponent_pieces.pop(elim_pos)

                # eliminate that piece from the board
                elim_piece.eliminate()

                # add to the opponent eliminated pieces
                opp_elim_pieces.append(elim_piece)

                # update the string board representation
                remove_col, remove_row = elim_pos
                self.set_board(remove_row, remove_col, constant.FREE_SPACE)

                # update the eliminated piece list
                eliminated_pieces.append(elim_piece)

                # for the eliminated piece we must also update any neighboutrs
                for direction in range(constant.MAX_MOVETYPE):
                    neighbour_pos = self.convert_move_type_to_coord(elim_pos,direction)
                    opp_dir = self.get_opposite_direction(direction)

                    # if a neighbouring square is occupied by this piece, we must update its free-neighbour list
                    if neighbour_pos in my_pieces:
                        neighbour = my_pieces[neighbour_pos]
                        neighbour.set_neighbour(opp_dir, True)
                        print(neighbour)

                    # if a neighbour is occupied by the opponent piece, we need to update its free-neighbour list
                    elif neighbour_pos in opponent_pieces:
                        neighbour = opponent_pieces[neighbour_pos]
                        neighbour.set_neighbour(opp_dir, True)
                        print(neighbour)

        # check for self elimination if there is not opponent piece to be eliminated
        elim_pos = self.check_self_elimination(my_piece_pos, colour)
        if elim_pos is not None:
            # removes item from the board and list
            elim_piece = my_pieces.pop(elim_pos)
            elim_piece.eliminate()

            # add to this players eliminated piece list
            my_elim_pieces.append(elim_piece)

            remove_col, remove_row = elim_pos
            self.set_board(remove_row, remove_col, constant.FREE_SPACE)

            # update the eliminated piece dictionary
            eliminated_pieces.append(elim_piece)

            # for the eliminated piece we must also update any neighbour
            for direction in range(constant.MAX_MOVETYPE):
                neighbour_pos = self.convert_move_type_to_coord(elim_pos, direction)
                opp_dir = self.get_opposite_direction(direction)

                # if a neighbouring square is occupied by this piece, we must update its free-neighbour list
                if neighbour_pos in my_pieces:
                    neighbour = my_pieces[neighbour_pos]
                    neighbour.set_neighbour(opp_dir, True)
                    print(neighbour)

                # if a neighbour is occupied by the opponent piece, we need to update its free-neighbour list
                elif neighbour_pos in opponent_pieces:
                    neighbour = opponent_pieces[neighbour_pos]
                    neighbour.set_neighbour(opp_dir, True)
                    print(neighbour)

        print(eliminated_pieces)
        print(my_elim_pieces)
        print(opp_elim_pieces)
        print(self)
        return eliminated_pieces

    # elimination helper function
    def check_one_piece_elimination(self, my_piece_pos, colour):
        pos_col, pos_row = my_piece_pos

        if colour == constant.WHITE_PIECE:
            my_pieces = copy(self.white_pieces)
            opponent_pieces = copy(self.black_pieces)
        elif colour == constant.BLACK_PIECE:
            my_pieces = copy(self.black_pieces)
            opponent_pieces = copy(self.white_pieces)

        # append the corner pieces to the list as these act as your own piece
        for corner in self.corner_pos:
            my_pieces.update({corner: None})

        # test all the 4 cases for this type of elimination
        # don't need to test for negative indices and positions outside the boundary of the board because there should
        # be no pieces that are placed in these positions and therefore do not exist in these lists

        # check left
        if (pos_col - 1, pos_row) in opponent_pieces and (pos_col - 2, pos_row) in my_pieces:
            if opponent_pieces[(pos_col - 1, pos_row)].is_alive():
                return pos_col - 1, pos_row
        # check right
        if (pos_col + 1, pos_row) in opponent_pieces and (pos_col + 2, pos_row) in my_pieces:
            if opponent_pieces[(pos_col + 1, pos_row)].is_alive():
                return pos_col + 1, pos_row
        # check up
        if (pos_col, pos_row - 1) in opponent_pieces and (pos_col, pos_row - 2) in my_pieces:
            if opponent_pieces[(pos_col, pos_row - 1)].is_alive():
                return pos_col, pos_row - 1
        # check down
        if (pos_col, pos_row + 1) in opponent_pieces and (pos_col, pos_row + 2) in my_pieces:
            if opponent_pieces[(pos_col, pos_row + 1)].is_alive():
                return pos_col, pos_row + 1

        # if it does not exist therefore there is no piece to be eliminated
        return None

    def check_self_elimination(self, my_piece_pos, colour):
        # update piecePos from tuple to pos_row and pos_col
        pos_col, pos_row = my_piece_pos

        if colour == constant.WHITE_PIECE:
            opponent_pieces = copy(self.black_pieces)
            my_pieces = self.white_pieces
        elif colour == constant.BLACK_PIECE:
            opponent_pieces = copy(self.white_pieces)
            my_pieces = self.black_pieces

        # append the corner pieces to the list as these act as your own piece
        for corner in self.corner_pos:
            opponent_pieces.update({corner: None})

        # now just need to check horizontal and vertical positions to see if they are in the piecePos list
        # horizontal check
        if ((pos_col + 1, pos_row) in opponent_pieces) and ((pos_col - 1, pos_row) in opponent_pieces):
            if my_pieces[(pos_col, pos_row)].is_alive():
                return pos_col, pos_row
        # vertical piece position check for self elimination
        elif ((pos_col, pos_row + 1) in opponent_pieces) and ((pos_col, pos_row - 1) in opponent_pieces):
            if my_pieces[(pos_col, pos_row)].is_alive():
                return pos_col, pos_row
        else:
            return None

    # helper method for the moving phase of the game
    @staticmethod
    def convert_move_type_to_coord(my_piece_pos, move_type):
        # piece pos is in the form of a tuple (col,row)
        # moves types
        # 0 - right 1 space
        # 1 - down 1 space
        # 2 - left 1 space
        # 3 - up 1 spaces
        # 4 - right 2 spaces
        # 5 - down 2 spaces
        # 6 - left 2 spaces
        # 7 - up 2 spaces

        # convert the tuple to row, col variable
        pos_col, pos_row = my_piece_pos

        # do the conversion -- this function does not handle
        if move_type == constant.RIGHT_1:
            return pos_col + 1, pos_row
        elif move_type == constant.DOWN_1:
            return pos_col, pos_row + 1
        elif move_type == constant.LEFT_1:
            return pos_col - 1, pos_row
        elif move_type == constant.UP_1:
            return pos_col, pos_row - 1
        elif move_type == constant.RIGHT_2:
            return pos_col + 2, pos_row
        elif move_type == constant.DOWN_2:
            return pos_col, pos_row + 2
        elif move_type == constant.LEFT_2:
            return pos_col - 2, pos_row
        elif move_type == constant.UP_2:
            return pos_col, pos_row - 2

    @staticmethod
    def convert_coord_to_move_type(coord_1, coord_2):
        # coord is the stationary piece, coord_2 is the piece we want to move to
        # the move type returned is the move type to get from coord_1 to coord_2
        coord_1_col, coord_1_row = coord_1
        # print(coord_1_col, coord_1_row)
        coord_2_col, coord_2_row = coord_2

        # check left and right first
        # check left
        if coord_1_col + 1 == coord_2_col and coord_1_row == coord_2_row:
            return constant.RIGHT_1
        elif coord_1_col == coord_2_col and coord_1_row + 1 == coord_2_row:
            return constant.DOWN_1
        elif coord_1_col - 1 == coord_2_col and coord_1_row == coord_2_row:
            return constant.LEFT_1
        elif coord_1_col == coord_2_col and coord_1_row - 1 == coord_2_row:
            return constant.UP_1
        elif coord_1_col + 2 == coord_2_col and coord_1_row == coord_2_row:
            return constant.RIGHT_2
        elif coord_1_col == coord_2_col and coord_1_row + 2 == coord_2_row:
            return constant.DOWN_2
        elif coord_1_col - 2 == coord_2_col and coord_1_row == coord_2_row:
            return constant.LEFT_2
        elif coord_1_col == coord_2_col and coord_1_row - 2 == coord_2_row:
            return constant.UP_2

    @staticmethod
    def get_opposite_direction(direction):
        if direction == constant.UP_1:
            return constant.DOWN_1
        elif direction == constant.LEFT_1:
            return constant.RIGHT_1
        elif direction == constant.DOWN_1:
            return constant.UP_1
        elif direction == constant.RIGHT_1:
            return constant.LEFT_1
        elif direction == constant.UP_2:
            return constant.DOWN_2
        elif direction == constant.LEFT_2:
            return constant.RIGHT_2
        elif direction == constant.DOWN_2:
            return constant.UP_2
        elif direction == constant.RIGHT_2:
            return constant.LEFT_2

    # shrink the board
    def shrink_board(self):
        eliminated_pieces = []

        # use the referee code for the shrinking of the board
        offset = self.num_shrink
        for i in range(offset, constant.BOARD_SIZE - offset):
            # list storing the row and column we need to shrink
            shrink = [(i, offset), (offset, i), (i, 7 - offset), (7 - offset, i)]
            for (col, row) in shrink:
                # update the board representation
                # set the row to invalid spaces
                self.set_board(row, col, constant.INVALID_SPACE)

                # remove any piece that is eliminated from the position lists
                if (col, row) in self.black_pieces:
                    piece = self.black_pieces.pop((col, row))
                    self.black_eliminate_pieces.append(piece)
                    eliminated_pieces.append(piece)
                elif (col, row) in self.white_pieces:
                    piece = self.white_pieces.pop((col, row))
                    self.white_eliminate_pieces.append(piece)
                    eliminated_pieces.append(piece)

                # set the column to invalid spaces
                self.set_board(col, row, constant.INVALID_SPACE)

        self.num_shrink += 1
        offset += 1
        # set the new corner
        self.corner_pos[0] = (offset, offset)
        self.corner_pos[1] = (7 - offset, offset)
        self.corner_pos[2] = (offset, 7 - offset)
        self.corner_pos[3] = (7 - offset, 7 - offset)

        # if a corner is on top of a piece , eliminate that piece
        for corner in self.corner_pos:

            if corner in self.white_pieces:
                piece = self.white_pieces.pop(corner)
                self.white_eliminate_pieces.append(piece)
                eliminated_pieces.append(piece)
            elif corner in self.black_pieces:
                piece = self.black_pieces.pop(corner)
                self.black_eliminate_pieces.append(piece)
                eliminated_pieces.append(piece)

        # update the board representations
        for corner_col, corner_row in self.corner_pos:
            self.set_board(corner_row, corner_col, constant.CORNER_PIECE)

        # check for one space eliminations about the corner pieces
        for i in (0, 2, 3, 1):
            corner = self.corner_pos[i]
            pieces = self.corner_elimination(corner)

            # add the eliminated pieces from corner elimination to the list of eliminated pieces
            eliminated_pieces += pieces

    # helper function for elimination of pieces at a corner -- for board shrinks
    def corner_elimination(self, corner):
        eliminated_pieces = []
        # print("CALLED CORNER ELIMINATION")
        # print("*"*50)
        # self.print_board()
        # print("*"*50)
        # types of players
        player_types = (constant.WHITE_PIECE, constant.BLACK_PIECE)

        # the corner piece can act as the player piece -- therefore we can eliminate
        # the white pieces around the corner first, then the black pieces
        for player in player_types:

            if player == constant.WHITE_PIECE:
                opponent_pieces = self.black_pieces
                opp_elim_pieces = self.black_eliminate_pieces
            elif player == constant.BLACK_PIECE:

                opponent_pieces = self.white_pieces
                opp_elim_pieces = self.white_eliminate_pieces

            opp_player = self.get_opp_piece_type(player)
            # there can be more than one elimination or there can be None
            while self.check_one_piece_elimination(corner, player) is not None:
                eliminated_pos = self.check_one_piece_elimination(corner, player)

                # remove from the oppenent players piece pos list
                # print("ELIMINATED: " + str(eliminated_piece))
                elim_piece = opponent_pieces.pop(eliminated_pos)
                opp_elim_pieces.append(elim_piece)

                eliminated_pieces[opp_player].append(elim_piece)
                col, row = eliminated_pos
                # update the board representation
                self.set_board(row, col, constant.FREE_SPACE)

        return eliminated_pieces

    # get the opposite piece type
    @staticmethod
    def get_opp_piece_type(piece_type):
        if piece_type == constant.WHITE_PIECE:
            return constant.BLACK_PIECE
        else:
            return constant.WHITE_PIECE

    def __str__(self):
        board = ""
        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                # get the char to print
                char_index = row * constant.BOARD_SIZE + col

                char = chr(self.board_state[char_index])
                board+=char + " "
            board+="\n"

        return "THIS BOARD: \n" + board + "\n"
