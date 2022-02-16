from http.client import NETWORK_AUTHENTICATION_REQUIRED
from BoardModel import Board

class Game():

    default_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self, fen=default_fen):
        self.board = Board()
        self.state = ("", "", "", "", "") # Turn, Castling, En Passant Tracker, 50 move counter, Full move counter
        self.move_history = []
        self.fen_history = []
        self.set_fen(fen)

    def __str__(self):
        pass

    def set_fen(self, fen):
        fen = fen.split()
        self.board.set_board(fen[0])
        self.state[0] = fen[0]
        self.state[1] = fen[1]
        self.state[2] = fen[2]
        self.state[3] = fen[3]
        self.state[4] = fen[4]
        

    def reset(self, fen=default_fen):
        self.set_fen(fen)
        self.move_history = []
        self.fen_history = []

    def notation_to_index(self, notation):
        notation = list(notation)
        return notation[1] * 8 + ord(notation[0]) - 96

    def index_to_notation(self, index):
        pass

    def make_move(self, start, end): # move is in the form "e2", "e4"
        start = self.notation_to_index(start)
        end = self.notation_to_index(end)

        
        pass

    def get_moves(self, player):
        pass

    def update_status(self):
        pass

