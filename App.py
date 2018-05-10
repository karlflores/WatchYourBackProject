from tkinter import *
from WatchYourBack.Board import Board
from Constants import constant
from Agents.Random import Random
from Agents.NegascoutTranspositionTable import Negascout as NSTT
from Agents.NegamaxTranspositionTable import Negamax as NMXTT
from Agents.Negamax import Negamax as NMX
from Agents.Manual import Manual
from time import sleep
def main():

    root = Tk()
    app = Window(root)
    root.geometry("1024x768")
    root.mainloop()

class Window(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master)
        self.master = master
        self.p1_strategy = None
        self.p1_name = ""
        self.p1_name_obj = None
        self.p2_strategy = None
        self.p2_name = ""
        self.p2_name_obj = None
        self.canvas = None
        self.information = None

        # the board representation of this game
        self.board = None
        self.obj_dict = None
        self.info_objs = None
        self.init_window()



    def init_window(self):
        self.master.title("Watch Your Back")

        self.pack(fill=BOTH, expand=1)

        exit_button = Button(self, text="EXIT",command=self.exit_program)
        exit_button.place(x=5, y=5)

        self.canvas = Canvas(self)
        self.info_objs = []
        self.init_information()
        canvas = self.canvas

        self.board = Board()
        self.obj_dict = self.draw_board(canvas)
        self.draw_grid(canvas)
        canvas.pack(fill=BOTH, expand=1)
        # create the menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the algorithm chooser
        player_1 = Menu(menu)
        player_1.add_command(label="Random", command=self.p1_random)
        player_1.add_command(label="Manual", command=self.p1_manual)
        player_1.add_command(label="Negamax - No Transpostion Table", command=self.p1_negamax)
        player_1.add_command(label="Negamax - w/ Transpostion Table", command=self.p1_negamax_tt)
        player_1.add_command(label="Negascout", command=self.p1_negascout)

        menu.add_cascade(label="Player 1", menu=player_1)

        player_2 = Menu(menu)
        player_2.add_command(label="Random", command=self.p2_random)
        player_2.add_command(label="Manual", command=self.p2_manual)
        player_2.add_command(label="Negamax - No Transpostion Table", command=self.p2_negamax)
        player_2.add_command(label="Negamax - w/ Transpostion Table", command=self.p2_negamax_tt)
        player_2.add_command(label="Negascout", command=self.p2_negascout)

        menu.add_cascade(label="Player 2", menu=player_2)

        # button
        begin_button = Button(text="BEGIN", command=self.nextmove, height=2, width=10)
        begin_button.place(x=805, y=650)

    def nextmove(self):
        print("STARTED GAME")
        player = constant.WHITE_PIECE

        if self.p1_name in ("Random", "Human"):
            pass
        else:
            self.p1_strategy.update_board(self.board)

        if self.p2_name in ("Random", "Human"):
            pass
        else:
            self.p2_strategy.update_board(self.board)

        action = self.generate_moves(1)
        print("88888888888888")
        print(action)
        print("88888888888888")
        self.board.update_board(action, constant.WHITE_PIECE)
        print(self.board)
        # self.canvas.delete("all")
        self.draw_board(self.canvas)

        if self.p1_name in ("Random", "Human"):
            pass
        else:
            self.p1_strategy.update_board(self.board)

        if self.p2_name in ("Random", "Human"):
            pass
        else:
            self.p2_strategy.update_board(self.board)

        action = self.generate_moves(2)
        self.board.update_board(action,constant.BLACK_PIECE)
        self.draw_board(self.canvas)
        if self.p1_name in ("Random", "Human"):
            pass
        else:
            self.p1_strategy.update_board(self.board)

        if self.p2_name in ("Random", "Human"):
            pass
        else:
            self.p2_strategy.update_board(self.board)
        return
            # return

    def generate_moves(self,player):
        if player == 1:
            if self.p1_name == "Random":
                actions = self.board.update_actions(constant.WHITE_PIECE)
                action = actions[self.p1_strategy.choose_move(actions)]
                return action

            elif self.p1_name == "Negamax":
                action = self.p1_strategy.itr_negamax()
                return action
            elif self.p1_name == "TT":
                action = self.p1_strategy.itr_negamax()
                return action
            elif self.p1_name == "Human":
                pass
                action = self.p1_strategy.itr_negamax()
                return action
            elif self.p1_name == "NS":
                action = self.p1_strategy.itr_negascout()
                return action

        elif player == 2:
            if self.p2_name == "Random":
                actions = self.board.update_actions(constant.BLACK_PIECE)
                action = actions[self.p2_strategy.choose_move(actions)]
                return action
            elif self.p2_name == "Negamax":
                action = self.p2_strategy.itr_negamax()
                return action
            elif self.p2_name == "TT":
                action = self.p2_strategy.itr_negamax()
                return action
            elif self.p2_name == "Human":
                pass
                action = self.p1_strategy.itr_negamax()
                return action
            elif self.p2_name == "NS":
                action = self.p1_strategy.itr_negascout()
                return action



    def exit_program(self):
        exit()

    def p1_negamax(self):
        self.canvas.delete(self.p1_name_obj)
        x_1 = 740
        y_1 = 50
        x_2 = 974
        y_2 = 690
        self.choose_negamax(1)
        self.p1_name_obj = self.canvas.create_text((x_1 + 20), y_1 + 30, anchor=W, font="Helvetica", text="Player 1: Negamax")
        self.p1_name = "Negamax"
    def p2_negamax(self):
        self.canvas.delete(self.p2_name_obj)
        x_1 = 740
        y_1 = 50
        x_2 = 974
        y_2 = 690
        self.choose_negamax(2)
        self.p2_name_obj = self.canvas.create_text((x_1 + 20), y_1 + 60, anchor=W, font="Helvetica", text="Player 2: Negamax")
        self.p2_name = "Negamax"
    def p1_manual(self):
        self.canvas.delete(self.p1_name_obj)
        x_1 = 740
        y_1 = 50
        x_2 = 974
        y_2 = 690
        self.choose_human(1)
        self.p1_name_obj = self.canvas.create_text((x_1 + 20), y_1 + 30, anchor=W, font="Helvetica", text="Player 1: Human")
        self.p1_name = "Human"

    def p2_manual(self):
        self.choose_human(2)
        self.canvas.delete(self.p2_name_obj)
        x_1 = 740
        y_1 = 50
        x_2 = 974
        y_2 = 690
        self.p2_name_obj = self.canvas.create_text((x_1 + 20), y_1 + 60, anchor=W, font="Helvetica", text="Player 2: Manual")
        self.p2_name = "Human"

    def p1_negamax_tt(self):
        self.choose_negamax_tt(1)
        self.canvas.delete(self.p1_name_obj)
        x_1 = 740
        y_1 = 50
        x_2 = 974
        y_2 = 690
        self.p1_name_obj = self.canvas.create_text((x_1 + 20), y_1 + 30, anchor=W, font="Helvetica", text="Player 1: Negamax w/ TT")
        self.p1_name = "TT"

    def p2_negamax_tt(self):
        self.choose_negamax_tt(2)
        self.canvas.delete(self.p2_name_obj)
        x_1 = 740
        y_1 = 50
        x_2 = 974
        y_2 = 690
        self.p2_name_obj = self.canvas.create_text((x_1 + 20), y_1 + 60, anchor=W, font="Helvetica",
                                         text="Player 2: Negamax w/ TT")
        self.p2_name = "TT"
    def p1_negascout(self):
        self.choose_negascout(1)
        self.canvas.delete(self.p1_name_obj)
        x_1 = 740
        y_1 = 50
        x_2 = 974
        y_2 = 690
        self.p1_name_obj = self.canvas.create_text((x_1 + 20), y_1 + 30, anchor=W, font="Helvetica",
                                         text="Player 1: Negascout")
        self.p1_name = "NS"
    def p2_negascout(self):
        self.choose_negascout(2)
        self.canvas.delete(self.p2_name_obj)
        x_1 = 740
        y_1 = 50
        x_2 = 974
        y_2 = 690
        self.p2_name_obj = self.canvas.create_text((x_1 + 20), y_1 + 60, anchor=W, font="Helvetica",
                                         text="Player 2: Negascout")
        self.p2_name = "NS"
    def p1_random(self):
        self.choose_random_player(1)
        self.canvas.delete(self.p1_name_obj)
        x_1 = 740
        y_1 = 50
        x_2 = 974
        y_2 = 690
        self.p1_name_obj = self.canvas.create_text((x_1 + 20), y_1 + 30, anchor=W, font="Helvetica",
                                         text="Player 1: Random")
        self.p1_name = "Random"

    def p2_random(self):
        self.canvas.delete(self.p2_name_obj)
        self.choose_random_player(2)
        x_1 = 740
        y_1 = 50
        x_2 = 974
        y_2 = 690
        self.p2_name_obj = self.canvas.create_text((x_1 + 20), y_1 + 60, anchor=W, font="Helvetica",
                                         text="Player 2: Random")
        self.p2_name = "Random"

    def choose_random_player(self,player):
        if player == 1:
            self.p1_strategy = Random()
            print("CHOOSE")
        else:
            self.p2_strategy = Random()

    def choose_negamax(self,player):
        if player == 1:
            self.p1_strategy = NMX(self.board, constant.WHITE_PIECE)
        else:
            self.p2_strategy = NMX(self.board, constant.BLACK_PIECE)

    def choose_negascout(self,player):
        if player == 1:
            self.p1_strategy = NSTT(self.board, constant.WHITE_PIECE)
        else:
            self.p2_strategy = NSTT(self.board, constant.BLACK_PIECE)

    def choose_negamax_tt(self,player):
        if player == 1:
            self.p1_strategy = NMXTT(self.board, constant.WHITE_PIECE)
        else:
            self.p2_strategy = NMXTT(self.board, constant.BLACK_PIECE)

    def choose_human(self,player):
        if player == 1:
            self.p1_strategy = Manual(constant.WHITE_PIECE)
        else:
            self.p2_strategy = Manual(constant.BLACK_PIECE)

    def choose_evaluation(self,filename):
        pass

    def draw_grid(self,canvas):
        spacing = 80
        offset = 50
        line_width = spacing*8

        for i in range(8):
            canvas.create_line(offset + spacing * i, offset, offset + spacing * i, line_width + offset)
            canvas.create_line(offset, offset + spacing * i, line_width + offset, offset + spacing * i)

        canvas.create_line(offset, offset, line_width + offset, offset)
        canvas.create_line(offset, line_width + offset, offset, offset)
        canvas.create_line(offset, line_width + offset, line_width + offset, line_width + offset)
        canvas.create_line(line_width + offset, offset, line_width + offset, line_width + offset)
        canvas.pack(expand=0)

    @staticmethod
    def draw_boardpiece(canvas, row, col, piece_type):
        if piece_type == constant.INVALID_SPACE:
            colour = "#FF0000"
            size = 80
            offset = 50
            inset = 5
            x_1 = col * (size) + (offset + inset)
            y_1 = row * (size) + (offset + inset)

            x_2 = (col + 1) * (size) + (offset - inset)
            y_2 = (row + 1) * (size) + (offset - inset)
            # return the canvas object ID
            return canvas.create_rectangle(x_1, y_1, x_2, y_2, outline="#000", fill=colour, width=5)
        elif piece_type == constant.BLACK_PIECE:
            colour = "#000"
            size = 80
            offset = 50
            inset = 5
            x_1 = col * (size) + (offset + inset)
            y_1 = row * (size) + (offset + inset)

            x_2 = (col + 1) * (size) + (offset - inset)
            y_2 = (row + 1) * (size) + (offset - inset)

            # return the canvas object ID
            return canvas.create_oval(x_1, y_1, x_2, y_2, outline="#000", fill=colour, width=5)

        elif piece_type == constant.WHITE_PIECE:
            colour = "#FFFFFF"
            size = 80
            offset = 50
            inset = 5
            x_1 = col * (size) + (offset + inset)
            y_1 = row * (size) + (offset + inset)

            x_2 = (col + 1) * (size) + (offset - inset)
            y_2 = (row + 1) * (size) + (offset - inset)

            # return the canvas object ID
            return canvas.create_oval(x_1, y_1, x_2, y_2, outline="#000", fill=colour, width=5)
        elif piece_type == constant.CORNER_PIECE:
            size = 80
            offset = 50
            inset = 5
            x_1 = col * (size) + (offset + inset)
            y_1 = row * (size) + (offset + inset)

            x_2 = (col + 1) * (size) + (offset - inset)
            y_2 = (row + 1) * (size) + (offset - inset)

            # return the canvas object ID
            return canvas.create_rectangle(x_1, y_1, x_2, y_2, outline="#CBC2C0", fill="#CBC2C0", width=2)
        else:
            colour = "#FFFFFF"
            size = 80
            offset = 50
            inset = 5
            x_1 = col * (size) + (offset + inset)
            y_1 = row * (size) + (offset + inset)

            x_2 = (col + 1) * (size) + (offset - inset)
            y_2 = (row + 1) * (size) + (offset - inset)
            # return the canvas object ID
            return canvas.create_rectangle(x_1, y_1, x_2, y_2, outline=colour, fill=colour, width=5)

    def draw_board(self, canvas):
        piece_arr = {}
        # canvas.delete("all")
        # self.draw_grid(canvas)
        for row in range(8):
            for col in range(8):
                piece = self.board.get_board_piece(row, col)
                piece_arr.update({(col,row): self.draw_boardpiece(canvas,row,col,piece)})
                
        return piece_arr

    def init_information(self):
        c1 = "#000"
        c2 = "#FFFFF0"
        x_1 = 740
        y_1 = 50
        x_2 = 974
        y_2 = 690

        canvas = self.canvas
        self.info_objs.append(canvas.create_rectangle(x_1, y_1, x_2, y_2, outline=c1, fill=c2, width=2))

if __name__ == "__main__":
    main()
