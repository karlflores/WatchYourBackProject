from tkinter import *
# from Board.Board import Board

def main():

    root = Tk()
    app = Window(root)
    root.geometry("1024x768")
    root.mainloop()


class Window(Frame):
    def __init__(self,master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

        self.p1_strategy = None
        self.p2_strategy = None

        # the board representation of this game
        # self.board = Board()

    def init_window(self):
        self.master.title("Watch Your Back")

        self.pack(fill=BOTH, expand=1)

        exit_button = Button(self, text="EXIT",command=self.exit_program)
        exit_button.place(x=5, y=5)

        # create the menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the algorithm chooser
        player_1 = Menu(menu)
        player_1.add_command(label="Random", command = self.choose_random_player(1))
        player_1.add_command(label="Negamax", command = self.choose_negamax(1))
        player_1.add_command(label="Negascout", command = self.choose_negascout(1))

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
if __name__ == "__main__":
    main()
