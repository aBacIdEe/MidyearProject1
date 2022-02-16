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

    def notation_to_index(self, notation): # 
        notation = list(notation)
        return notation[1] * 8 + ord(notation[0]) - 96

    def index_to_notation(self, index):
        pass

    def validate_moves(self): # filters all moves for check and such
        self.eval_rays() # evaluate the rays
        ALL_MOVES = self.board.all_moves()
        VALID_MOVES = {}

        for index in ALL_MOVES: # Iterates through all indicies of all pieces
            testBoard = Board(fen=str(self.board)) # Create a test board
            validPieceMoves = []
            
            if self.board[index].isupper():
                color = "White"
                playerMoves = testBoard.get_player_moves("White")
                kingIndex = self.board.index("K")
            else:
                color = "Black"
                playerMoves = testBoard.get_player_moves("Black")
                kingIndex = self.board.index("k")

            for rays in ALL_MOVES[index]: # Iterate through all rays from that piece
                for move in rays:
                    testBoard.move_piece(int(index), move, self.board[int(index)]) # make that move on the test board
                    
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


                    

                # compile a list of all enemy moves and see if our our side is in check


    def eval_rays(self): # filters ALL_MOVES for rays
        '''
        Our Original Moves, only the nonempty indicies are in here
        '''
        ALL_MOVES = self.board.all_moves()


        '''
        Iterates through all indicies of the board, and skips that index if it's empty
        '''
        for i in range(64):
            if self.board[i] == " ":
                continue
            else:
                '''
                Creates a revised Moves list which recompiles the list based on the pieces on the board
                '''
                pieceMoves = ALL_MOVES[str(i)]
                revisedMoves = []
                if self.board[i].isupper(): # Checks if the piece that we're checking is white or black
                    color = "White"
                else:
                    color = "Black"
                
                '''
                Creates a revised Ray list which recompiles each individual ray
                '''
                for ray in pieceMoves:
                    revisedRay = []

                    for tile in ray:
                        if self.board[tile] == " ":
                            revisedRay.append(tile)
                        elif self.board[tile].isupper() and color == "White" or self.board[tile].islower() and color == "Black":
                            break
                        else:
                            revisedRay.append(tile)
                            break

                    '''
                    Aggregates all the revised Rays to the revised Moves list
                    '''
                    revisedMoves.append(revisedRay) # updates the
            
            '''
            Aggregates all the revised Moves to the ALL_MOVES dictionary
            '''
            ALL_MOVES[str(i)] = revisedMoves

    def update_status(self):
        pass

