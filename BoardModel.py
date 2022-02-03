

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
        if str == "p": return Pawn(color, self.board)
        elif str == "r": return Rook(color, self.board)
        elif str == "n": return Knight(color, self.board)
        elif str == "b": return Bishop(color, self.board)
        elif str == "q": return Queen(color, self.board)
        elif str == "k": return King(color, self.board)

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
                piece = self.abbrv_to_piece(char, "White", i)
                self.board[i] = piece
                i += 1
            else:
                piece = self.abbrv_to_piece(char, "Black", i)
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
        if piece == 0:
            self.move_confirmation(False)
        elif piece.moves(Srank, Sfile, Erank, Efile):
            temp = self.board[endIndex]
            self.board[endIndex] = self.board[startIndex]
            self.board[startIndex] = 0
            if piece.king_in_check(): # After seeing if a move is valid, make that move and check if your king is till in check
                self.board[startIndex] = self.board[endIndex] # if it is, then it undos the move and says invalid
                self.board[endIndex] = temp
                self.move_confirmation(False)
            else: # otherwise it goes through
                self.move_confirmation(True)
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

    def __init__(self, color, board, pos):
        self.color = color
        self.directions = ((-8, "N"), (1, "E"), (8, "S"), (-1, "W"), (-7, "NE"), (9, "SE"), (7, "SW"), (-9, "NW"))
        self.cardinalDirections = ((-8, "N"), (1, "E"), (8, "S"), (-1, "W"))
        self.diagonalDirections = ((-7, "NE"), (9, "SE"), (7, "SW"), (-9, "NW"))
        self.knightDirections = ((-15, "NE"), (-6, "NE"), (10, "SE"), (17, "SE"), (6, "SW"), (15, "SW"), (-10, "NW"), (-17, "NW")) # knight moves
        # slide function not in here to repeatedly use one "king move" until hit piece
        # for pawn moves it's a procedure
        self.board = board
        # init will be overwritten for king, pawn, and rook for promotion, castle eligbility, and in check
        self.position = pos

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

    def is_piece(self, target):
        if self.board[target] != 0:
            return True
        return False

    def is_same_color(self, color, target):
        target = self.board[target]
        if target.color == color:
            return True
        return False 

    def location_to_index(self, sr, sf, er, ef): # from rank and file to index
        pass

    def king_in_check(self):
        if self.color == "White":
            for location in self.board:
                if location != 0 and str(location) == "K" and location.in_check():
                    return True
        else:
            for location in self.board:
                if location != 0 and str(location) == "k" and location.in_check():
                    return True
        return False



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
            if 0 <= possibility < 64 and self.orientation(sr, sf, possibility // 8, possibility % 8) == dir[1]:
                valid.append(possibility)
            
        if goal in valid:
            return True
        return False
    
    def in_check(self):
        er = self.position // 8
        ef = self.position % 8
        enemies = []
        if self.color == "White":
            for location in self.board:
                if location != 0 and location.color == "Black":
                    enemies.append(location)
            for enemy in enemies:
                sr = enemy.position // 8
                sf = enemy.position % 8
                if enemy.moves(sr, sf, er, ef):
                    return True
        else:
            for location in self.board:
                if location != 0 and location.color == "White":
                    enemies.append(location)
            for enemy in enemies:
                sr = enemy.position // 8
                sf = enemy.position % 8
                if enemy.moves(sr, sf, er, ef):
                    return True
        return False

class Queen(Piece):

    def __str__(self):
        if self.color == "White":
            return "Q"
        return "q"

    def moves(self, sr, sf, er, ef):
        position = (8 - sr) * 8 + sf
        goal = (8 - er) * 8 + ef
        valid = []

        for dir in self.directions:
            possibility = position + dir[0]
            while 0 <= possibility < 64 and self.orientation(sr, sf, possibility // 8, possibility % 8) == dir[1]:
                if self.is_piece(possibility) and self.is_same_color(self.color, possibility):
                    break # if the endpoint is of same color, break

                valid.append(possibility) # adds possibility if empty 
                possibility += dir[0] # increments possibility

                if self.is_piece(possibility) and not self.is_same_color(self.color, possibility):
                    valid.append(possibility) # if endpoint is of opposite color
                    break # taking is as far as you can go, and break

        if goal in valid:
            return True
        return False

class Bishop(Piece):

    def __str__(self):
        if self.color == "White":
            return "B"
        return "b"

    def moves(self, sr, sf, er, ef):
        position = (8 - sr) * 8 + sf
        goal = (8 - er) * 8 + ef
        valid = []

        for dir in self.diagonalDirections:
            possibility = position + dir[0]
            while 0 <= possibility < 64 and self.orientation(sr, sf, possibility // 8, possibility % 8) == dir[1]:
                if self.is_piece(possibility) and self.is_same_color(self.color, possibility):
                    break # if the endpoint is of same color, break

                valid.append(possibility) # adds possibility if empty 
                possibility += dir[0] # increments possibility

                if self.is_piece(possibility) and not self.is_same_color(self.color, possibility):
                    valid.append(possibility) # if endpoint is of opposite color
                    break # taking is as far as you can go, and break

        if goal in valid:
            return True
        return False

class Knight(Piece):

    def __str__(self):
        if self.color == "White":
            return "N"
        return "n"

    def moves(self, sr, sf, er, ef):
        position = (8 - sr) * 8 + sf
        goal = (8 - er) * 8 + ef
        valid = []

         # N E S W NE SE SW NW
        for dir in self.knightDirections:
            possibility = position + dir[0]
            if 0 <= possibility < 64 and self.orientation(sr, sf, possibility // 8, possibility % 8) == dir[1]:
                if self.is_piece(possibility) and self.is_same_color(self.color, possibility):
                    continue # if the endpoint is of same color, break
                else:
                    valid.append(possibility)
            
        if goal in valid:
            return True
        return False

class Rook(Piece):

    def __str__(self):
        if self.color == "White":
            return "R"
        return "r"

    def moves(self, sr, sf, er, ef):
        position = (8 - sr) * 8 + sf
        goal = (8 - er) * 8 + ef
        valid = []

        for dir in self.cardinalDirections:
            possibility = position + dir[0]
            while 0 <= possibility < 64 and self.orientation(sr, sf, possibility // 8, possibility % 8) == dir[1]:
                if self.is_piece(possibility) and self.is_same_color(self.color, possibility):
                    break # if the endpoint is of same color, break

                valid.append(possibility) # adds possibility if empty 
                possibility += dir[0] # increments possibility

                if self.is_piece(possibility) and not self.is_same_color(self.color, possibility):
                    valid.append(possibility) # if endpoint is of opposite color
                    break # taking is as far as you can go, and break

        if goal in valid:
            return True
        return False

class Pawn(Piece):

    def __init__(self, color, board):
        self.color = color
        self.passant = False
        if self.color == "White": # move up on board 
            self.directions = [(-8, "N", True), (-16, "N", True), (-7, "NE", False), (-9, "NW", False), (-16, "N", True)] # note: make third state to decide validitiy
        else: # move down on board
            self.directions = [(8, "S", True), (16, "S", True), (9, "SE", False), (7, "SW", False), (16, "S", True)]

        self.board = board

    def __str__(self):
        if self.color == "White":
            return "P"
        return "p"

    def moves(self, sr, sf, er, ef):
        position = (8 - sr) * 8 + sf
        goal = (8 - er) * 8 + ef
        valid = []

        if self.color == "White": # ADDED CHECK IF PIECE UPAHEAD FOR DOUBLE JUMP
            if self.is_piece(position - 8):
                self.directions[0] = (-8, "N", False)
                self.directions[4] = (-16, "N", False)
            if self.is_piece(position - 7):
                self.directions[2] = (-7, "NE", True)
            if self.is_piece(position -9):
                self.directions[3] = (-9, "NW", True)
        elif self.color == "Black":
            if self.is_piece(position + 8):
                self.directions[0] = (8, "S", False)
                self.directions[4] = (16, "S", False)
            if self.is_piece(position + 9):
                self.directions[2] = (9, "SE", True)
            if self.is_piece(position + 7):
                self.directions[3] = (7, "SW", True)


        for dir in self.directions:
            possibility = position + dir[0]
            if 0 <= possibility < 64 and self.orientation(sr, sf, possibility // 8, possibility % 8) == dir[1] and dir[2]:
                if self.is_piece(possibility) and self.is_same_color(self.color, possibility):
                    continue # if the endpoint is of same color, break
                else:
                    valid.append(possibility) # adds possibility if empty 
        
        self.reset_directions()

        if goal in valid:
            return True
        return False
                

    def reset_directions(self):
        if self.color == "White":
            self.directions = [(-8, "N", True), (-16, "N", False), (-7, "NE", False), (-9, "NW", False), (-16, "N", False)]
        else:
            self.directions = [(8, "S", True), (16, "S", False), (9, "SE", False), (7, "SW", False), (16, "S", False)]


def main():
    chess = Board()
    chess.load_board("rnbqkbnr/pppppppp/8/8/8/8/PPP1PPPP/RNBQKBNR")
    print(str(chess))
    chess.move_piece("d1", "d7")
    print(str(chess))
    chess.move_piece("d7", "e6")
    print(str(chess))
    chess.move_piece("e6", "e8")
    print(str(chess))
    chess.move_piece("e6", "e7")
    print(str(chess))

main()