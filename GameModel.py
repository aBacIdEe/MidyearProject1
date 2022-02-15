from BoardModel import Board

class Game():

    default_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self, fen=default_fen):
        self.board = Board()
        self.state = ("", "", "", "", "")
        self.move_history = []
        self.fen_history = []
        self.set_fen(fen)

    def set_fen(self):
        pass

    def notation_to_index(self, notation):
        pass

    def index_to_notation(self, index):
        pass

    def make_move(self, move): # Should Update Everything in the turn
        pass

    def get_moves(self, player):
        pass

    def update_status(self):
        pass

