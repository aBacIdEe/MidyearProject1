from BoardModel import Board

class Game():

    default_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self, fen=default_fen):
        self.board = Board()
        self.state = ["", "", "", "", ""] # Turn, Castling, En Passant Tracker, 50 move counter, Full move counter
        self.move_history = []
        self.fen_history = []
        self.set_fen(fen)

    def __str__(self):
        return ' '.join([str(self.board)] + self.state)

    def set_fen(self, fen):
        fen = fen.split()
        self.board.set_board(fen[0])
        self.state[0] = fen[1] # Turn 'w' or 'b'
        self.state[1] = fen[2] # Castling KQkq
        self.state[2] = fen[3] # En Passant e6
        self.state[3] = fen[4] # 50 move counter
        self.state[4] = fen[5] # Full move counter
        

    def reset(self, fen=default_fen):
        self.set_fen(fen)
        self.move_history = []
        self.fen_history = []

    def notation_to_index(self, notation): # 
        notation = list(notation)
        return (8 - int(notation[1])) * 8 + ord(notation[0]) - 96

    def get_player_moves(self, color):
        ALL_MOVES = self.eval_rays()
        PLAYER_MOVES = {}

        if color == "White":
            for index in ALL_MOVES:
                if self.board.board[int(index)].isupper():
                    PLAYER_MOVES[index] = ALL_MOVES[index]

        else:
            for index in ALL_MOVES:
                if self.board.board[int(index)].islower():
                    PLAYER_MOVES[index] = ALL_MOVES[index]

        return PLAYER_MOVES

    def is_attacked(self, tile, color): # Color refers to the color of the enemy
        if color == "White": ALL_POSSIBLE_ATTACKS = self.get_player_moves("White")
        else: ALL_POSSIBLE_ATTACKS = self.get_player_moves("Black")

        ATTACKED_TILES = []
        for key in ALL_POSSIBLE_ATTACKS:
            for tile in ALL_POSSIBLE_ATTACKS[key]:
                if tile in ATTACKED_TILES:
                    continue
                else:
                    ATTACKED_TILES.append(tile)

        return tile in ATTACKED_TILES
        

    def make_move(self, move): # Updates Board states as well as making the move
        move = list(move)
        start = self.notation_to_index(move[0:2])
        end = self.notation_to_index(move[2:4])
        ALL_MOVES = self.extra_moves()

        if end in ALL_MOVES[str(start)]: # Check get
            self.board.move_piece(start, end, self.board.board[start])

        

    def extra_moves(self): # Adds En Passant and Castling and checks their validity, but the actual movement of pieces is not here
        ALL_MOVES = self.validate_moves()
        if self.state[1] != "-": # Castling
            if "K" in self.state[1] and self.board.board[61] == " " and self.board.board[62] == " " \
                and not(self.is_attacked(60, "Black") and self.is_attacked(61, "Black") and self.is_attacked(62, "Black")): 
                ALL_MOVES["K"].append(62)
            if "k" in self.state[1] and self.board.board[57] == " " and self.board.board[58] == " " and self.board.board[59] \
                and not(self.is_attacked(4, "White") and self.is_attacked(5, "White") and self.is_attacked(6, "White")): 
                ALL_MOVES["Kk"].append(6)
            if "Q" in self.state[1] and self.board.board[5] == " " and self.board.board[6] == " " \
                and not(self.is_attacked(60, "Black") and self.is_attacked(59, "Black") and self.is_attacked(58, "Black")): 
                ALL_MOVES["K"].append(58)
            if "q" in self.state[1] and self.board.board[1] == " " and self.board.board[2] == " " and self.board.board[3] \
                and not(self.is_attacked(4, "White") and self.is_attacked(3, "White") and self.is_attacked(2, "White")): 
                ALL_MOVES["K"].append(2)

        if self.state[2] != "-": # En Passant
            targetIndex = self.notation_to_index(self.state[2])
            if targetIndex < 32: # Taking Black Piece
                if str(targetIndex + 7) in ALL_MOVES: ALL_MOVES[str(targetIndex + 7)].append(targetIndex)
                elif self.board.board[targetIndex + 7] == "P": ALL_MOVES[targetIndex + 7] = [targetIndex]
                if str(targetIndex + 9) in ALL_MOVES: ALL_MOVES[str(targetIndex + 9)].append(targetIndex)
                elif self.board.board[targetIndex + 9] == "P": ALL_MOVES[targetIndex + 9] = [targetIndex]
            else:
                if str(targetIndex - 7) in ALL_MOVES: ALL_MOVES[str(targetIndex - 7)].append(targetIndex)
                elif self.board.board[targetIndex - 7] == "P": ALL_MOVES[targetIndex - 7] = [targetIndex]
                if str(targetIndex - 9) in ALL_MOVES: ALL_MOVES[str(targetIndex - 9)].append(targetIndex)
                elif self.board.board[targetIndex - 9] == "P": ALL_MOVES[targetIndex - 9] = [targetIndex]

        return ALL_MOVES

    def validate_moves(self): # filters all moves for check and such
        ALL_MOVES = self.eval_rays() # evaluate the rays
        #print(ALL_MOVES)
        #print()
        VALID_MOVES = {}

        for index in ALL_MOVES: # Iterates through all indicies of all pieces
            testBoard = Game(fen=str(self)) # Create a test board
            validPieceMoves = []
            # add depth counter for this statement, OR currently trying to use not validated moves but evalulated rays
            if self.board.board[int(index)].isupper():
                color = "White"
                playerMoves = testBoard.get_player_moves("White")
                kingIndex = self.board.board.index("K")
            else:
                color = "Black"
                playerMoves = testBoard.get_player_moves("Black")
                kingIndex = self.board.board.index("k")

            for rays in ALL_MOVES[index]: # Iterate through all rays from that piece
                for move in rays:
                    testBoard.board.move_piece(int(index), move, self.board.board[int(index)]) # make that move on the test board
                    
                    attackedSquares = []
                    if color == "White":
                        for testIndex in playerMoves:
                            attackedSquares += playerMoves[testIndex]
                        if kingIndex in attackedSquares:
                            continue
                        else:
                            validPieceMoves.append(move)
                    else:
                        for testIndex in playerMoves:
                            attackedSquares += playerMoves[testIndex]
                        if kingIndex in attackedSquares:
                            continue
                        else:
                            validPieceMoves.append(move)
            
            VALID_MOVES[index] = validPieceMoves
        
        return VALID_MOVES

    def eval_rays(self): # filters ALL_MOVES for rays
        '''
        Our Original Moves, only the nonempty indicies are in here
        '''
        ALL_MOVES = self.board.all_moves()


        '''
        Iterates through all indicies of the board, and skips that index if it's empty
        '''
        for i in range(64):
            if self.board.board[i] == " ":
                continue
            else:
                '''
                Creates a revised Moves list which recompiles the list based on the pieces on the board
                '''
                pieceMoves = ALL_MOVES[str(i)]
                revisedMoves = []
                if self.board.board[i].isupper(): # Checks if the piece that we're checking is white or black
                    color = "White"
                else:
                    color = "Black"
                
                '''
                Creates a revised Ray list which recompiles each individual ray
                '''
                for ray in pieceMoves:
                    revisedRay = []

                    for tile in ray:
                        if self.board.board[tile] == " ":
                            revisedRay.append(tile)
                        elif self.board.board[tile].isupper() and color == "White" or self.board.board[tile].islower() and color == "Black":
                            break
                        else:
                            revisedRay.append(tile)
                            break

                    '''
                    Aggregates all the revised Rays to the revised Moves list
                    '''
                    if revisedRay:
                        revisedMoves.append(revisedRay)
            
            '''
            Aggregates all the revised Moves to the ALL_MOVES dictionary
            '''
            if revisedMoves: # if not empty, then switch, otherwise remove
                ALL_MOVES[str(i)] = revisedMoves
            else:
                del ALL_MOVES[str(i)]


        return ALL_MOVES

    def update_status(self): # to check if it's black win, white win, or draw
        pass

game1 = Game()
print(game1)
print()
print(game1.board.all_moves())
print()
print(game1.extra_moves())
game1.make_move("e2e3")
print(game1)
