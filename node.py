class Node(object):
    def __init__(self,board,counter,move):
        self.board = board
        self.depth = 0
        self.parent = None
        self.counter = counter

        # this stores the move applied to a certain node to bring it to the state that it is in
        # move should be in the form (tup1,tup2) where tup1 is the original location and tup2 is the
        # location where the piece has moved to
        self.moveApplied = move
    def updateCounter(self):
        self.counter+=1
        return
    def updateDepth(self):
        self.depth+=1
        return
