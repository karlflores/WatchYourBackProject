from random import randint


class Random(object):
    def __init__(self, len_available_moves):
        self.num_moves = len_available_moves

    def choose_move(self):
        return randint(0,self.num_moves-1)

    def update_num(self, num):
        self.num_moves = num