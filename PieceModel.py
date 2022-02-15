from BoardModel import Board

class Piece(Board):

    def __init__(self, color, pos):
        self.color = color
        self.position = pos

    def get_file(self):
        return self.position % 8

    def get_rank(self):
        return 8 - self.position // 8
