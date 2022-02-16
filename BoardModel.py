class Board():

    DIRECTIONS = {"P": lambda index, dx, dy: (8 - index // 8) > 1 and -1 <= dx <= 1 and dy == 1,
                  "p": lambda index, dx, dy: (8 - index // 8) < 8 and -1 <= dx <= 1 and dy == -1,
                  "n": lambda index, dx, dy: (abs(dx) + abs(dy) == 3) and abs(dx) >= 1 and abs(dy) >= 1,
                  "b": lambda index, dx, dy: abs(dx) == abs(dy),
                  "r": lambda index, dx, dy: dx == 0 or dy == 0,
                  "q": lambda index, dx, dy: dx == 0 or dy == 0 or abs(dx) == abs(dy),
                  "k": lambda index, dx, dy: dx <= 1 and dy <= 1}

    default_fen = " " * 64

    def __init__(self, fen=default_fen):
        self.board = []
        self.set_fen(fen)

    def __str__(self): # returns FEN str of Board
        result = []

        for i in range(64): # Iterates with index i through all 64 slots
            piece = self.board[i]
            if i != 0 and i % 8 == 0:
                result.append("/")

            if piece != " ": # if it's not a space, append the piece
                result.append(piece)
            elif piece == " ": # if it is a space, append a digit of 1, and if there's already an integer there, add one to it
                if result[-1].is_integer():
                    result[-1] += 1
                else:
                    result.append(1)

        return "".join(result)

    def set_fen(self, fen):
        self.position = []

        for char in fen:
            if char == "/":
                continue
            elif char.isdigit():
                for _ in range(int(char)):
                    self.position.append(" ")
            else:
                self.position.append(char)

    def move_piece(self, start, end, piece):
        self.board[end] = piece
        self.board[start] = " "

    def index_to_notation(self, index): # chr(97) = "a"
        file = chr(97 + index % 8)
        rank = str(8 - index // 8)
        return file + rank

    def all_moves(self):
        MOVES = {}
        for i in range(64):
            MOVES[self.index_to_notation(i)] = self.moves(i)

    def moves(self, index):
        PIECE_MOVES = []
        piece = self.board[index]
        
        startingRank = 8 - index // 8
        startingFile = index % 8

        for i in range(64):
            endingRank = 8 - i // 8
            endingFile = i % 8
            deltaRank = endingRank - startingRank
            deltaFile = endingFile - startingFile

            if self.DIRECTIONS[piece](index, deltaRank, deltaFile):
                PIECE_MOVES.append(i)

        # sort moves by distance from starting point to account for "line moves" that extend from the center

        

            
