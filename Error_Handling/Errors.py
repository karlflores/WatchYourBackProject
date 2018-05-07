class Error(Exception):
    pass


class TimeOut(Error):
    pass


class OutOfMemory(Error):
    pass


class NoFavourableMoves(Error):
    pass


class ReturnUnfavourableMove(Error):
    pass


class PieceOutofBound(Error):
    pass


class IllegalPlacement(Error):
    pass
