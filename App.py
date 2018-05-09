from tkinter import *
from BoardOOP.Board import Board
from Constants import constant

def main():

    root = Tk()
    app = Window(root)
    root.geometry("1024x768")
    root.mainloop()

class Window(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master)
        self.master = master

        self.init_window()

        self.p1_strategy = None
        self.p2_strategy = None

        # the board representation of this game
        self.board = Board()

    def init_window(self):
        self.master.title("Watch Your Back")

        self.pack(fill=BOTH, expand=1)

        exit_button = Button(self, text="EXIT",command=self.exit_program)
        exit_button.place(x=5, y=5)

        canvas = Canvas(self)

        self.draw_grid(canvas)
        canvas.pack(fill=BOTH, expand=1)
        # create the menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the algorithm chooser
        player_1 = Menu(menu)
        player_1.add_command(label="Random", command=self.choose_random_player(1))
        player_1.add_command(label="Negamax", command=self.choose_negamax(1))
        player_1.add_command(label="Negascout", command=self.choose_negascout(1))

        menu.add_cascade(label="Player 1", menu=player_1)

    def exit_program(self):
        exit()

    def choose_random_player(self,player):
        pass

    def choose_negamax(self,player):
        pass

    def choose_negascout(self,nega_scout):
        pass

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

        corner_id = []
        corners = [(0,0),(0,7),(7,0),(7,7)]

        a = self.draw_boardpiece(canvas, 2, 2, constant.BLACK_PIECE)
        a = self.draw_boardpiece(canvas, 4, 2, constant.WHITE_PIECE)
        a = self.draw_boardpiece(canvas, 3, 2, constant.INVALID_SPACE)
        a = self.draw_boardpiece(canvas, 7, 2, constant.WHITE_PIECE)
        # delete the corners
        piece_dict = self.draw_board(canvas)
        canvas.pack(fill=BOTH, expand=1)

    @staticmethod
    def draw_boardpiece(canvas, row, col, piece_type):
        if piece_type == constant.INVALID_SPACE:
            colour = "#FF0000"
            size = 80
            offset = 50
            inset = 5
            x_1 = row * (size) + (offset + inset)
            y_1 = col * (size) + (offset + inset)

            x_2 = (row + 1) * (size) + (offset - inset)
            y_2 = (col + 1) * (size) + (offset - inset)
            # return the canvas object ID
            return canvas.create_rectangle(x_1, y_1, x_2, y_2, outline="#000", fill=colour, width=5)
        elif piece_type == constant.BLACK_PIECE:
            colour = "#000"
            size = 80
            offset = 50
            inset = 5
            x_1 = row * (size) + (offset + inset)
            y_1 = col * (size) + (offset + inset)

            x_2 = (row + 1) * (size) + (offset - inset)
            y_2 = (col + 1) * (size) + (offset - inset)

            # return the canvas object ID
            return canvas.create_oval(x_1, y_1, x_2, y_2, outline="#000", fill=colour, width=5)

        elif piece_type == constant.WHITE_PIECE:
            colour = "#FFFFFF"
            size = 80
            offset = 50
            inset = 5
            x_1 = row * (size) + (offset + inset)
            y_1 = col * (size) + (offset + inset)

            x_2 = (row + 1) * (size) + (offset - inset)
            y_2 = (col + 1) * (size) + (offset - inset)

            # return the canvas object ID
            return canvas.create_oval(x_1, y_1, x_2, y_2, outline="#000", fill=colour, width=5)
        elif piece_type == constant.CORNER_PIECE:
            size = 80
            offset = 50
            inset = 5
            x_1 = row * (size) + (offset + inset)
            y_1 = col * (size) + (offset + inset)

            x_2 = (row + 1) * (size) + (offset - inset)
            y_2 = (col + 1) * (size) + (offset - inset)

            # return the canvas object ID
            return canvas.create_rectangle(x_1, y_1, x_2, y_2,
                                           outline="#CBC2C0", fill="#CBC2C0", width=2)
        else:
            colour = "#FFFFFF"
            size = 80
            offset = 50
            inset = 5
            x_1 = row * (size) + (offset + inset)
            y_1 = col * (size) + (offset + inset)

            x_2 = (row + 1) * (size) + (offset - inset)
            y_2 = (col + 1) * (size) + (offset - inset)
            # return the canvas object ID
            return canvas.create_rectangle(x_1, y_1, x_2, y_2, outline=colour, fill=colour, width=5)

    def draw_board(self, canvas):
        board = Board()
        piece_arr = {}
        # canvas.delete("all")
        for row in range(8):
            for col in range(8):
                piece = board.get_board_piece(row, col)
                piece_arr.update({(col,row): self.draw_boardpiece(canvas,row,col,piece)})

        return piece_arr


if __name__ == "__main__":
    main()
