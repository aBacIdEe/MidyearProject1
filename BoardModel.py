

class Board():

    def __init__(self): # size is built in instead of parameterized
        self.board = [0 for _ in range(64)]
        self.turn = "White"

    def __str__(self):
        result = ""
        for x in range(8):
            result += str(8 - x) + " "
            for y in range(8):
                result += str(self.board[8 * x + y]) + " "
            result += "\n"
        result += "  a b c d e f g h\n"
        return result

    def rank_to_int(self, letter):
        base = ord("a")
        return ord(letter) - base

    def abbrv_to_piece(self, str, color):
        str = str.lower()
        if str == "p":
            return Pawn(color)
        elif str == "r":
            return Rook(color)
        elif str == "n":
            return Knight(color)
        elif str == "b":
            return Bishop(color)
        elif str == "q":
            return Queen(color)
        elif str == "k":
            return King(color)

    def is_int(self, str):
        try:
            int(str)
            return True
        except:
            return False

    def load_board(self, str): # FEN
        str = str.split()
        i = 0
        for char in str[0]:
            if char == "/":
                continue
            elif self.is_int(char):
                i += int(char)
            elif char.isupper():
                piece = self.abbrv_to_piece(char, "White")
                self.board[i] = piece
                i += 1
            else:
                piece = self.abbrv_to_piece(char, "Black")
                self.board[i] = piece
                i += 1

    def move_piece(self, start, end):
        start = list(start)
        end = list(end)
        Srank = int(start[1])
        Sfile = self.rank_to_int(start[0]) # a = 1, h = 8
        Erank = int(end[1])
        Efile = self.rank_to_int(end[0])

        startIndex = Sfile + 8 * (8 - Srank)
        endIndex = Efile + 8 * (8 - Erank)

        piece = self.board[startIndex]
        if piece.moves(Srank, Sfile, Erank, Efile):
            self.move_confirmation(True)
            self.board[endIndex] = self.board[startIndex]
            self.board[startIndex] = 0
        else:
            self.move_confirmation(False)

    def move_confirmation(self, valid):
        if valid:
            print("move made")
        else:
            print("invalid move")

    def evaluation(self):
        pass

class Piece():

    def __init__(self, color):
        self.color = color
        self.directions = ((-8, "N"), (1, "E"), (8, "S"), (-1, "W"), (-7, "NE"), (9, "SE"), (7, "SW"), (-9, "NW"))
        self.Nmoves = ((), (), (), (), (), (), (), ()) # knight moves
        # slide function not in here to repeatedly use one "king move" until hit piece
        # for pawn moves it's a procedure

        # init will be overwritten for king, pawn, and rook for promotion, castle eligbility, and in check

    # eventually need a list for attacked squares and unattacked ones so to check checks against the king

    def orientation(self, sr, sf, er, ef): # prevent board wrapping moves
        if sr < er and sf < ef: return "NE" # i think it's fixed...it's not fixed
        elif sr < er and sf > ef: return "NW" # 6 ranks
        elif sr > er and sf < ef: return "SE" # 5
        elif sr > er and sf > ef: return "SW" # 4
        elif sr < er and sf == ef: return "N" # 3
        elif sr > er and sf == ef: return "S" # 2
        elif sr == er and sf < ef: return "E" # 1
        elif sr == er and sf > ef: return "W" # 0 1 2 3 4 5 6 7 8 file

    def location_to_index(self, sr, sf, er, ef): # from rank and file to index
        pass


class King(Piece):
        
    def __str__(self):
        if self.color == "White":
            return "K"
        return "k"

    def moves(self, sr, sf, er, ef):
        position = (8 - sr) * 8 + sf
        goal = (8 - er) * 8 + ef
        valid = []

         # N E S W NE SE SW NW
        for dir in self.directions:
            possibility = position + dir[0]
            if 0 <= possibility < 64 and self.orientation(sr, sf, er, ef) == dir[1]:
                valid.append(possibility)
            
        if goal in valid:
            return True
        return False

class Queen(Piece):

    def __init__(self, color):
        self.color = color

    def __str__(self):
        if self.color == "White":
            return "Q"
        return "q"

    def moves(self):
        pass

class Bishop(Piece):

    def __init__(self, color):
        self.color = color

    def __str__(self):
        if self.color == "White":
            return "B"
        return "b"

    def moves(self):
        pass

class Knight(Piece):

    def __init__(self, color):
        self.color = color

    def __str__(self):
        if self.color == "White":
            return "N"
        return "n"

    def moves(self):
        pass

class Rook(Piece):

    def __init__(self, color):
        self.color = color

    def __str__(self):
        if self.color == "White":
            return "R"
        return "r"

    def moves(self):
        pass

class Pawn(Piece):

    def __init__(self, color):
        self.color = color
        self.double = True
        self.passant = False

    def __str__(self):
        if self.color == "White":
            return "P"
        return "p"

    def moves(self):
        pass

chess = Board()
chess.load_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
print(str(chess))
chess.move_piece("e1", "e2")
print(str(chess))