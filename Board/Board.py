'''
* Implements the board class for the game
*

'''

from Board import constant
from copy import deepcopy
import math


class Board(object):

    def __init__(self):
        # define the board parameters and constants
        self.board_state = self.init_board_rep()

        # self.piece_pos = {constant.BLACK_PIECE: {-1:}, constant.WHITE_PIECE: []}
        # store the current position of pieces on the board
        self.piece_pos = {constant.WHITE_PIECE: [],
                          constant.BLACK_PIECE: []}

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

    def init_board_rep(self):
        # store the board representation as a byte_array length 64 (64bytes)
        temp = ''
        for index in range(constant.BOARD_SIZE * constant.BOARD_SIZE):
            temp += constant.FREE_SPACE
        # create a temp string of length 64
        temp = bytearray(temp,'utf-8')

        # set the corner locations on the board representation
        corner_pos = [(0,0),(0,7),(7,0),(7,7)]
        for col,row in corner_pos:
            self.set_array_char(temp, row, col, constant.CORNER_PIECE)

        return temp

    def is_valid_placement(self,piece_place,piece_type):
        # set the valid zones for placement
        if piece_type == constant.WHITE_PIECE:
            start_zone = 0
            end_zone = constant.BOARD_SIZE - 2
        else:
            start_zone = 2
            end_zone = constant.BOARD_SIZE - 1

        # get the row and col
        pos_col, pos_row = piece_place

        # check the boundary of the board -- if a piece is placed outside
        # of it then return false
        if pos_col < 0 or pos_col > constant.BOARD_SIZE - 1:
            return False
        if pos_row < start_zone or pos_row > end_zone:
            # we can check if the place is placed in the starting zones for each player
            return False

        # now we can check if the placement of the piece is a free space -- if it
        # is then we know it is possible
        if self.get_board_piece(pos_row, pos_col) == constant.FREE_SPACE:
            return True
        else:
            return False

    # returns the type of the cell at a given position
    def return_cell_type(self, my_piece_pos):
        # based on the corner positions we know the current
        # dimensions of the board
        col_min = self.corner_pos[0][1]
        col_max = self.corner_pos[2][1]
        row_min = self.corner_pos[0][0]
        row_max = self.corner_pos[1][0]

        # if the position is outside of the playable bounds
        col, row = my_piece_pos
        if col < col_min or col > col_max:
            return constant.INVALID_SPACE
        if row < row_min or row > row_max:
            return constant.INVALID_SPACE

        # piece is in the playable bounds of the game
        # we can return this piece
        return self.get_board_piece(row,col)

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

    @ staticmethod
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



    # check if a move is legal
    def is_legal_move(self,my_piece_pos,move_type):
        # print("MOVE: " + str(my_piece_pos))
        # apply the move to the piece
        new_pos = self.convert_move_type_to_coord(my_piece_pos, move_type)
        # print("NEW POS: " + str(new_pos))
        my_piece_type = self.return_cell_type(my_piece_pos)

        # check if the piece is actually a piece on the board
        if my_piece_type != constant.BLACK_PIECE and my_piece_type != constant.WHITE_PIECE:
            # then the piece cannot be placed here
            return False

        # at this stage we know the position is a piece on the board

        # get the piece type:
        new_my_piece_type = self.return_cell_type(new_pos)
        # check if the piece is within the current dimensions of the board
        if new_my_piece_type == constant.INVALID_SPACE or \
                new_my_piece_type == constant.SPACE_NOT_EXIST:
            return False

        # if there is not another piece occupying that space and if it is inside the board
        # then it is a valid move
        # now we can check the move itself
        # if it is an adjacent move
        if 0 <= move_type < 4:
            if new_my_piece_type == constant.FREE_SPACE:
                return True
            else:
                # there is a piece that is occupying this space
                return False
        # check the two space move
        elif 4 <= move_type < 8:
            # get the intermediate position piece_type
            inter_pos = self.convert_move_type_to_coord(my_piece_pos,move_type-4)
            inter_pos_piece_type = self.return_cell_type(inter_pos)
            # print("INTERMEDIATE SPACE " + inter_pos_piece_type)

            # if there is a piece adjacent to that piece then we can make the jump
            if inter_pos_piece_type in (constant.BLACK_PIECE, constant.WHITE_PIECE):
                if new_my_piece_type == constant.FREE_SPACE:
                    # if the space is free then we can move here
                    return True
                else:
                    # if the space is not free then we cannot move here
                    return False
            else:
                # if the intermediate piece is a free space then we cannot perform this move
                return False

    # get the opposite piece type
    @staticmethod
    def get_opp_piece_type(piece_type):
        if piece_type == constant.WHITE_PIECE:
            return constant.BLACK_PIECE
        else:
            return constant.WHITE_PIECE

    # board representation setters and getter methods
    def get_board_piece(self, row, col):
        return self.get_array_element(self.board_state,row,col)

    # change the piece type in the board representation
    def set_board(self, row, col, piece_type):
        piece_types = (constant.CORNER_PIECE, constant.WHITE_PIECE, constant.BLACK_PIECE,
                       constant.FREE_SPACE, constant.INVALID_SPACE)
        # check if the piece_type is valid
        if piece_type not in piece_types:
            return

        # if valid we can set the board position
        self.set_array_char(self.board_state,row,col,piece_type)

    # print board method
    def print_board(self):

        for row in range(constant.BOARD_SIZE):
            for col in range (constant.BOARD_SIZE):
                # get the char to print
                char_index = row * constant.BOARD_SIZE + col

                char = chr(self.board_state[char_index])
                print('{} '.format(char),end='')

            print()

    # elimination checkers

    def perform_elimination(self, my_piece_pos, my_piece_type):
        # get the opponent piece type
        opp_piece_type = self.get_opp_piece_type(my_piece_type)

        eliminated_pieces = []

        while self.check_one_piece_elimination(my_piece_pos,my_piece_type) is not None:
            piece = self.check_one_piece_elimination(my_piece_pos,my_piece_type)

            # want to eliminate about the opposition's piece
            if piece in self.piece_pos[opp_piece_type]:
                # update the opponents piece_pos_list
                self.piece_pos[opp_piece_type].remove(piece)

                # update the string board representation
                remove_col,remove_row = piece
                self.set_board(remove_row, remove_col, constant.FREE_SPACE)
                eliminated_pieces.append(piece)

        # check for self elimination if there is not opponent piece to be eliminated
        piece = self.check_self_elimination(my_piece_pos,my_piece_type)
        if piece is not None:
            # removes item from the board and list
            self.piece_pos[my_piece_type].remove(piece)

            remove_col, remove_row = piece
            self.set_board(remove_row, remove_col, constant.FREE_SPACE)
            eliminated_pieces.append(piece)

        return eliminated_pieces

    # elimination helper function
    def check_one_piece_elimination(self,my_piece_pos,my_piece_type):
        pos_col, pos_row = my_piece_pos
        my_piece_pos_list = deepcopy(self.piece_pos[my_piece_type])
        opp_piece_type = self.get_opp_piece_type(my_piece_type)
        # append the corner pieces to the list as these act as your own piece
        for corner in self.corner_pos:
            my_piece_pos_list.append(corner)

        # test all the 4 cases for this type of elimination
        # don't need to test for negative indices and positions outside the boundary of the board because there should
        # be no pieces that are placed in these positions and therefore do not exist in these lists

        # check left
        if (pos_col-1,pos_row) in self.piece_pos[opp_piece_type] and\
                (pos_col-2,pos_row) in my_piece_pos_list:
            return pos_col-1,pos_row
        # check right
        if (pos_col+1,pos_row) in self.piece_pos[opp_piece_type] and\
                (pos_col+2,pos_row) in my_piece_pos_list:
            return pos_col+1,pos_row
        # check up
        if (pos_col,pos_row-1) in self.piece_pos[opp_piece_type] and\
                (pos_col,pos_row-2) in my_piece_pos_list:
            return pos_col,pos_row-1
        # check down
        if (pos_col,pos_row+1) in self.piece_pos[opp_piece_type] and\
                (pos_col,pos_row+2) in my_piece_pos_list:
            return pos_col, pos_row+1

        # if it does not exist therefore there is no piece to be eliminated
        return None
    
    def check_self_elimination(self,my_piece_pos,my_piece_type):
        # update piecePos from tuple to pos_row and pos_col
        pos_col,pos_row = my_piece_pos
        
        # if the current piece pos is not the expected piece type then return None
        # if self.return_cell_type(my_piece_pos) != my_piece_type:
        #    return None

        opp_piece_type = self.get_opp_piece_type(my_piece_type)

        opp_piece_pos_list = deepcopy(self.piece_pos[opp_piece_type])
        # add the location of the corners to the location list of the opponent piece
        for corner in self.corner_pos:
            opp_piece_pos_list.append(corner)
        
        # now just need to check horizontal and vertical positions to see if they are in the piecePos list
        # horizontal check
        if ((pos_col+1,pos_row) in opp_piece_pos_list) and \
                ((pos_col-1,pos_row) in opp_piece_pos_list):
            return pos_col,pos_row
        # vertical piece position check for self elimination
        elif ((pos_col,pos_row+1) in opp_piece_pos_list) and \
                ((pos_col,pos_row-1) in opp_piece_pos_list):
            return pos_col,pos_row
        else:
            return None

    # call this when we want to make a move -- change the dict and change the board

    # when we want to apply a move to the board -- update the board and the dict associated
    def make_move(self, old_pos, move_type, my_piece_type):
        eliminated_pieces = []
        # check if the move is legal first
        if self.is_legal_move(old_pos, move_type) is False:
            return

        # we know we can make the move now
        new_pos = self.convert_move_type_to_coord(old_pos, move_type)
        new_col, new_row = new_pos
        old_col, old_row = old_pos

        # first we update the board representation
        self.set_board(old_row, old_col, constant.FREE_SPACE)
        self.set_board(new_row,new_col,my_piece_type)

        # then we can update the dictionaries
        self.piece_pos[my_piece_type].remove(old_pos)
        # create a new entry in the dictionary containing the piece on the board
        self.piece_pos[my_piece_type].append(new_pos)

        # now we can test for elimination at the new position on the board
        pieces = self.perform_elimination(new_pos,my_piece_type)
        if pieces is not None:
            for piece in pieces:
                eliminated_pieces.append(piece)
        # increase the number of moves made on the board
        # self.move_counter += 1
        # success
        return eliminated_pieces

    def make_placement(self,pos, my_piece_type):
        eliminated_pieces = []
        col,row = pos

        # check if that placement is legal
        if self.is_valid_placement(pos, my_piece_type) is False:
            return

        # else we know that this piece can be placed on the board

        # first we update the board representation
        self.set_board(row,col,my_piece_type)

        # then we update the position list of that player on the board
        self.piece_pos[my_piece_type].append(pos)

        # increment the move counter
        # self.move_counter += 1

        # perform the elimination around the piece that has been placed
        pieces = self.perform_elimination(pos, my_piece_type)
        if pieces is not None:
            for piece in pieces:
                eliminated_pieces.append(piece)
        # success if we reach here
        return eliminated_pieces

    # went we want to update the board we call this function
    # move has to be in the form ((row,col),move_type)
    def update_board(self,move,my_piece_type):
        eliminated_pieces = []
        # print(move)

        # make the action
        if self.phase == constant.PLACEMENT_PHASE:
            # make the placement -- this should take care of the update to the piece position list
            # as well as the move counter
            pieces = self.make_placement(move, my_piece_type)
            if pieces is not None:
                for piece in pieces:
                    eliminated_pieces.append(piece)

        elif self.phase == constant.MOVING_PHASE:
            # move is in the form (pos, move_type)
            pos = move[0]
            move_type = move[1]
            # print(pos)
            # make the move
            pieces = self.make_move(pos,move_type, my_piece_type)
            # return the eliminated pieces list
            if pieces is not None:
                for piece in pieces:
                    eliminated_pieces.append(piece)

        # after an action is applied we can increment the move counter of the board
        self.move_counter += 1

        # test if we need to switch from placement to moving
        if self.move_counter == 24 and self.phase == constant.PLACEMENT_PHASE:
            # change the phase from placement to moving
            self.phase = constant.MOVING_PHASE
            self.move_counter = 0
            # all 24 pieces have been placed on the board

        if self.phase == constant.MOVING_PHASE:
            # do we need to shrink the board
            if self.move_counter in (128, 192):
                self.shrink_board()

            # check if the move passed in was a forfeit move
            if move is None:
                self.move_counter += 1

            # the current player has made its move the we need to
            # set the next player to move to be the player to move on next update
            self.set_player_to_move(self.get_opp_piece_type(self.player_to_move))

            # check if the board is a terminal state / a win/ loose/ draw
            self.is_terminal()

        return eliminated_pieces

    # shrink the board
    def shrink_board(self):
        # use the referee code for the shrinking of the board
        offset = self.num_shrink
        for i in range(offset, constant.BOARD_SIZE - offset):
            # list storing the row and column we need to shrink
            shrink = [(i,offset), (offset,i), (i,7-offset), (7-offset,i)]
            for (col,row) in shrink:
                # update the board representation
                # set the row to invalid spaces
                self.set_board(row, col, constant.INVALID_SPACE)

                # remove any piece that is eliminated from the position lists
                if (col, row) in self.piece_pos[constant.BLACK_PIECE]:
                    self.piece_pos[constant.BLACK_PIECE].remove((col, row))
                elif (col,row) in self.piece_pos[constant.WHITE_PIECE]:
                    self.piece_pos[constant.WHITE_PIECE].remove((col, row))

                # set the column to invalid spaces
                self.set_board(col, row, constant.INVALID_SPACE)

        self.num_shrink += 1
        offset += 1
        # set the new corner
        self.corner_pos[0] = (offset,offset)
        self.corner_pos[1] = (7-offset,offset)
        self.corner_pos[2] = (offset,7-offset)
        self.corner_pos[3] = (7-offset,7-offset)

        # if a corner is on top of a piece , eliminate that piece
        for corner in self.corner_pos:
            for player in (constant.BLACK_PIECE, constant.WHITE_PIECE):
                if corner in self.piece_pos[player]:
                    self.piece_pos[player].remove(corner)

        # update the board representations
        for corner_col,corner_row in self.corner_pos:
            self.set_board(corner_row, corner_col, constant.CORNER_PIECE)

        # check for one space eliminations about the corner pieces
        for i in (0,2,3,1):
            corner = self.corner_pos[i]
            self.corner_elimination(corner)

    # helper function for elimination of pieces at a corner -- for board shrinks

    def corner_elimination(self,corner):
        # print("CALLED CORNER ELIMINATION")
        # print("*"*50)
        # self.print_board()
        # print("*"*50)
        # types of players
        player_types = (constant.WHITE_PIECE, constant.BLACK_PIECE)

        # the corner piece can act as the player piece -- therefore we can eliminate
        # the white pieces around the corner first, then the black pieces
        for player in player_types:
            # there can be more than one elimination or there can be None
            while self.check_one_piece_elimination(corner, player) is not None:
                opp_player = self.get_opp_piece_type(player)
                eliminated_piece = self.check_one_piece_elimination(corner,player)

                # remove from the oppenent players piece pos list
                # print("ELIMINATED: " + str(eliminated_piece))
                self.piece_pos[opp_player].remove(eliminated_piece)
                col, row = eliminated_piece
                # update the board representation
                self.set_board(row, col, constant.FREE_SPACE)

    # check if there is a winner terminal states can only occur in the final phase
    def is_terminal(self):

        # use the referee code for this
        white_num = len(self.piece_pos[constant.WHITE_PIECE])
        black_num = len(self.piece_pos[constant.BLACK_PIECE])

        if self.phase == constant.MOVING_PHASE:
            if black_num >= 2 and white_num >= 2:
                return False
            elif black_num >= 2 and white_num < 2:
                self.winner = constant.BLACK_PIECE
                # self.phase = constant.TERMINAL
                self.terminal = True
                return True
            elif black_num < 2 and white_num >=2:
                self.winner = constant.WHITE_PIECE
                # self.phase = constant.TERMINAL
                self.terminal = True
                return True
            elif black_num < 2 and white_num < 2:
                self.winner = None
                # self.phase = constant.TERMINAL
                self.terminal = True
                return True
        else:
            return False

    def set_player_to_move(self,player):
        self.player_to_move = player

    # string_array helper methods
    @staticmethod
    def get_array_element(byte_array,row,col):
        # we assume that the string array is n x n in dimension

        # get the dimension
        dimension = int(math.sqrt(len(byte_array)))
        # check if row and col are valid
        if row > dimension - 1 or col > dimension - 1:
            return None

        elif row < 0 or col < 0:
            return None
        # get the index to access in the string
        index = row*dimension + col;

        # return the char at position index
        return chr(byte_array[index])

    @staticmethod
    def set_array_char(byte_array, row, col, new_char):
        dimension = int(math.sqrt(len(byte_array)))

        if row > dimension - 1 or col > dimension - 1:
            return
        elif row < 0 or col < 0:
            return

        # set the new char in the string
        # need to turn char into utf-8 encoding first
        byte_array[row * dimension + col] = ord(new_char)
