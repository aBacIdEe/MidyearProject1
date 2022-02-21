class Board():

    default_fen = " " * 64

    def __init__(self, fen=default_fen):
        self.board = []
        self.set_board(fen)

    def __str__(self): # returns FEN str of Board
        result = []

        for i in range(64): # Iterates with index i through all 64 slots
            piece = self.board[i]
            if i != 0 and i % 8 == 0:
                result.append("/")

            if piece != " ": # if it's not a space, append the piece
                result.append(piece)
            elif piece == " ": # if it is a space, append a digit of 1, and if there's already an integer there, add one to it
                if result and result[-1].isdigit():
                    result[-1] = str(int(result[-1]) + 1)
                else:
                    result.append("1")

        return "".join(result)

    def set_board(self, fen):
        self.board = []

        for char in fen:
            if char == "/":
                continue
            elif char.isdigit():
                for _ in range(int(char)):
                    self.board.append(" ")
            else:
                self.board.append(char)

    def move_piece(self, start, end, piece):
        self.board[end] = piece
        self.board[start] = " "

    def get_player(self, index):
        piece = self.board[index]
        if not piece.isspace():
            return 'w' if piece.isupper() else 'b'
        return False
