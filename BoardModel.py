

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

    def abbrv_to_piece(self, str, color, location):
        str = str.lower()
        if str == "p": return Pawn(color, self.board, location)
        elif str == "r": return Rook(color, self.board, location)
        elif str == "n": return Knight(color, self.board, location)
        elif str == "b": return Bishop(color, self.board, location)
        elif str == "q": return Queen(color, self.board, location)
        elif str == "k": return King(color, self.board, location)

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
        start = list(start) + [""]
        end = list(end) + [""]
        Srank = int(start[1])
        Sfile = self.rank_to_int(start[0]) # a = 1, h = 8
        Erank = int(end[1])
        Efile = self.rank_to_int(end[0])
        pawnPromote = end[2]

        startIndex = Sfile + 8 * (8 - Srank)
        endIndex = Efile + 8 * (8 - Erank)

        piece = self.board[startIndex]
        if piece != 0:
            if piece.color != self.turn:
                self.move_confirmation(False)
            elif piece.moves(Srank, Sfile, Erank, Efile):
                temp = self.board[endIndex]
                self.board[endIndex] = self.board[startIndex]
                self.board[startIndex] = 0
                tempPos = piece.position
                piece.position = self.board.index(piece)
                if piece.king_in_check(): # After seeing if a move is valid, make that move and check if your king is still in check
                    self.board[startIndex] = self.board[endIndex] # if it is, then it undos the move and says invalid
                    self.board[endIndex] = temp
                    piece.position = tempPos
                    self.move_confirmation(False)
                else: # otherwise it goes through
                    if str(piece).lower() == "k": # if king is being moved
                        if startIndex - endIndex == -2: # short castle
                            self.board[startIndex + 1] = self.board[startIndex + 3]
                            self.board[startIndex + 3] = 0
                        elif startIndex - endIndex == 2: # long castle
                            self.board[startIndex - 1] = self.board[startIndex - 4]
                            self.board[startIndex - 4] = 0
                    if str(piece).lower() == "p":
                        if piece.passanted:
                            if piece.color == "White":
                                self.board[endIndex + 8] = 0
                                piece.passanted = False
                            else:
                                self.board[endIndex - 8] = 0
                                piece.passanted = False
                        if 0 <= piece.position < 8:
                            if pawnPromote == "Q": self.board[endIndex] = Queen(piece.color, self.board, endIndex)
                            elif pawnPromote == "B": self.board[endIndex] = Bishop(piece.color, self.board, endIndex)
                            elif pawnPromote == "N": self.board[endIndex] = Knight(piece.color, self.board, endIndex)
                            elif pawnPromote == "R": self.board[endIndex] = Rook(piece.color, self.board, endIndex)
                            else: self.move_confirmation(False)
                        elif 56 <= piece.position < 64:
                            if pawnPromote == "Q": self.board[endIndex] = Queen(piece.color, self.board, endIndex)
                            elif pawnPromote == "B": self.board[endIndex] = Bishop(piece.color, self.board, endIndex)
                            elif pawnPromote == "N": self.board[endIndex] = Knight(piece.color, self.board, endIndex)
                            elif pawnPromote == "R": self.board[endIndex] = Rook(piece.color, self.board, endIndex)
                            else: self.move_confirmation(False)
                                
                    piece.position = self.board.index(piece)
                    self.move_confirmation(True)
            else:
                self.move_confirmation(False)
        else:
            self.move_confirmation(False)

    def move_confirmation(self, valid):
        if valid:
            print("move made")
            if self.turn == "White":
                self.turn = "Black"
            else:
                self.turn = "White"
            return True
        elif not valid:
            print("invalid move")
            return False

        if self.end():
            print("Checkmate")

    def end(self):
        return False
        for location in self.board:
            if location != 0 and str(location) == "K" and self.in_check(location.position, "White"):
                return True

    def in_check(self, position, color):
        er = 8 - position // 8
        ef = position % 8
        enemies = []
        if color == "White":
            for location in self.board:
                if location != 0 and location.color == "Black":
                    enemies.append(location)
            for enemy in enemies:
                sr = 8 - enemy.position // 8
                sf = enemy.position % 8
                if enemy.moves(sr, sf, er, ef):
                    return True
        elif color == "Black":
            for location in self.board:
                if location != 0 and location.color == "White":
                    enemies.append(location)
            for enemy in enemies:
                sr = 8 - enemy.position // 8
                sf = enemy.position % 8
                if enemy.moves(sr, sf, er, ef):
                    return True
        return False

    def evaluation(self):
        pass

class Piece(Board):

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
        if sr < er and sf < ef: return "NE" # i think it's fixed...it's not fixed...maybe it is fixed
        elif sr < er and sf > ef: return "NW" # 6 ranks
        elif sr > er and sf < ef: return "SE" # 5
        elif sr > er and sf > ef: return "SW" # 4
        elif sr < er and sf == ef: return "N" # 3
        elif sr > er and sf == ef: return "S" # 2
        elif sr == er and sf < ef: return "E" # 1
        elif sr == er and sf > ef: return "W" # 0 1 2 3 4 5 6 7 8 file

    def is_piece(self, target):
        if 0 <= target < 64 and self.board[target] != 0:
            return True
        return False

    def is_double_pawn(self, target):
        if 0 <= target < 64 and str(self.board[target]).lower() == "p" and self.board[target].moveCount == 1:
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
                if location != 0 and str(location) == "K" and self.in_check(location.position, "White"):
                    return True
        else:
            for location in self.board:
                if location != 0 and str(location) == "k" and self.in_check(location.position, "Black"):
                    return True
        return False



class King(Piece):
        
    def __init__(self, color, board, pos):
        self.color = color
        self.directions = [(-8, "N"), (1, "E"), (8, "S"), (-1, "W"), (-7, "NE"), (9, "SE"), (7, "SW"), (-9, "NW")]
        self.board = board
        # init will be overwritten for king, pawn, and rook for promotion, castle eligbility, and in check
        self.position = pos
        self.notMoved = True

    def __str__(self):
        if self.color == "White":
            return "K"
        return "k"

    def moves(self, sr, sf, er, ef):
        position = (8 - sr) * 8 + sf
        goal = (8 - er) * 8 + ef
        valid = []

        if self.notMoved and str(self.board[self.position + 3]).lower() == "r" and self.board[self.position + 3].color == self.color and self.board[self.position + 3].castleable: # East side has an unmoved rook
            doable = True
            # check if those squares are empty
            if self.board[self.position + 1] == 0 and self.board[self.position + 2] == 0:
                # check if those squares are in check
                # It's now hardcoded, but significantly cleaner
                if self.in_check(self.position + 1, self.board[self.position].color): doable = False
                if self.in_check(self.position + 2, self.board[self.position].color): doable = False
                if doable:
                    self.directions.append((2, "E"))
        if self.notMoved and str(self.board[self.position - 4]).lower() == "r" and self.board[self.position - 4].color == self.color and self.board[self.position - 4].castleable: # West side has an unmoved rook    
            doable = True
            # check if those squares are empty
            if self.board[self.position - 1] == 0 and self.board[self.position - 2] == 0 and self.board[self.position - 3] == 0:
                # check if those squares are in check
                if self.in_check(self.position - 1, self.board[self.position].color): doable = False        
                if self.in_check(self.position - 2, self.board[self.position].color): doable = False
                if self.in_check(self.position - 3, self.board[self.position].color): doable = False
                if doable:
                    self.directions.append((-2, "W"))

         # N E S W NE SE SW NW
        for dir in self.directions:
            possibility = position + dir[0]
            if 0 <= possibility < 64 and self.orientation(sr, sf, 8 - possibility // 8, possibility % 8) == dir[1]:
                if self.is_piece(possibility) and self.is_same_color(self.color, possibility):
                    continue
                else:
                    valid.append(possibility)
        
        if goal in valid:
            self.reset_directions() # ADD IF STATEMENT TO MOVE ROOKS
            return True
        return False
    
    def reset_directions(self):
        self.directions = [(-8, "N"), (1, "E"), (8, "S"), (-1, "W"), (-7, "NE"), (9, "SE"), (7, "SW"), (-9, "NW")]
        self.notMoved = False
    

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
            while 0 <= possibility < 64 and self.orientation(sr, sf, 8 - possibility // 8, possibility % 8) == dir[1]:
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
            while 0 <= possibility < 64 and self.orientation(sr, sf, 8 - possibility // 8, possibility % 8) == dir[1]:
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
            if 0 <= possibility < 64 and self.orientation(sr, sf, 8 - possibility // 8, possibility % 8) == dir[1]:
                if self.is_piece(possibility) and self.is_same_color(self.color, possibility):
                    continue # if the endpoint is of same color, break
                else:
                    valid.append(possibility)
            
        if goal in valid:
            return True
        return False

class Rook(Piece):

    def __init__(self, color, board, pos):
        self.color = color
        self.cardinalDirections = ((-8, "N"), (1, "E"), (8, "S"), (-1, "W"))
        self.board = board
        # init will be overwritten for king, pawn, and rook for promotion, castle eligbility, and in check
        self.position = pos
        self.castleable = True

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
            while 0 <= possibility < 64 and self.orientation(sr, sf, 8 - possibility // 8, possibility % 8) == dir[1]:
                if self.is_piece(possibility) and self.is_same_color(self.color, possibility):
                    break # if the endpoint is of same color, break

                valid.append(possibility) # adds possibility if empty 
                possibility += dir[0] # increments possibility

                if self.is_piece(possibility) and not self.is_same_color(self.color, possibility):
                    valid.append(possibility) # if endpoint is of opposite color
                    break # taking is as far as you can go, and break

        if goal in valid:
            self.castleable = False
            return True
        return False

class Pawn(Piece):

    def __init__(self, color, board, pos):
        self.color = color
        self.passant = False
        if self.color == "White": # move up on board 
            self.directions = [(-8, "N", True), (-7, "NE", False), (-9, "NW", False), (-16, "N", True)] # note: make third state to decide validitiy
        else: # move down on board
            self.directions = [(8, "S", True), (9, "SE", False), (7, "SW", False), (16, "S", True)]

        self.board = board
        self.position = pos
        self.moveCount = 0

        self.passanted = False

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
                self.directions[3] = (-16, "N", False)

            if self.is_piece(position - 7):
                self.directions[1] = (-7, "NE", True)
            if self.is_double_pawn(position + 1):
                self.directions[1] = (-7, "NE", True, True)
            
            if self.is_piece(position -9):
                self.directions[2] = (-9, "NW", True)
            if self.is_double_pawn(position - 1):
                self.directions[2] = (-9, "NW", True, True)
        
        elif self.color == "Black":
            if self.is_piece(position + 8):
                self.directions[0] = (8, "S", False)
                self.directions[3] = (16, "S", False)
            
            if self.is_piece(position + 9):
                self.directions[1] = (9, "SE", True)
            if self.is_double_pawn(position + 1):
                self.directions[1] = (9, "SE", True, True)
    
            if self.is_piece(position + 7):
                self.directions[2] = (7, "SW", True)
            if self.is_double_pawn(position - 1):
                self.directions[2] = (7, "SW", True, True)


        for dir in self.directions:
            possibility = position + dir[0]
            if 0 <= possibility < 64 and self.orientation(sr, sf, 8 - possibility // 8, possibility % 8) == dir[1] and dir[2]:
                if self.is_piece(possibility) and self.is_same_color(self.color, possibility):
                    continue # if the endpoint is of same color, break
                else:
                    if len(dir) == 4:
                        valid.append((possibility, True))
                    else:
                        valid.append((possibility, False)) # adds possibility if empty 

        for possible in valid:
            if goal in possible:
                if possible[1]:
                    self.passanted = True
                self.reset_directions()
                self.moveCount += 1
                return True
        return False
                

    def reset_directions(self):
        if self.color == "White":
            self.directions = [(-8, "N", True), (-7, "NE", False), (-9, "NW", False), (-16, "N", False)]
        else:
            self.directions = [(8, "S", True), (9, "SE", False), (7, "SW", False), (16, "S", False)]

 
def main():
    chess = Board()
    chess.load_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    print(str(chess))
    chess.move_piece("e2", "e4")
    print(str(chess))
    chess.move_piece("a7", "a5")
    print(str(chess))
    chess.move_piece("e4", "e5")
    print(str(chess))
    chess.move_piece("f7", "f5")
    print(str(chess))
    chess.move_piece("e5", "f6")
    print(str(chess))
    chess.move_piece("b7", "b6")
    print(str(chess))

main()