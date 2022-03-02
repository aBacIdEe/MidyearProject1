from math import atan2

from BoardModel import Board

class Game():

    EVERY_MOVE = {} # all moves possible in any position from any piece

    '''
    Clockwise from the Top, all directions for each ray
    And then all the knight rotations, it doesn't matter since DIRECTIONS 
    will restrict the rays anyways
    '''
    RAYS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1),
            (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
    RAY_ANGLES = [atan2(ray[0], ray[1]) for ray in RAYS]

    '''
    After generating a full ray in every direction for each piece, 
    restrict it to the following conditions.
    '''
    DIRECTIONS = {"p": lambda y, dx, dy: y < 8 and dy == -1 and abs(dx) <= 1,
                  "P": lambda y, dx, dy: y > 1 and dy == 1 and abs(dx) <= 1,
                  "n": lambda y, dx, dy: (abs(dx) + abs(dy) == 3) and 
                                          abs(dx) >= 1 and abs(dy) >= 1,
                  'N': lambda y, dx, dy: (abs(dx) + abs(dy) == 3) and 
                                          abs(dx) >= 1 and abs(dy) >= 1,
                  "b": lambda y, dx, dy: abs(dx) == abs(dy),
                  'B': lambda y, dx, dy: abs(dx) == abs(dy),
                  "r": lambda y, dx, dy: dx == 0 or dy == 0,
                  'R': lambda y, dx, dy: dx == 0 or dy == 0,
                  "q": lambda y, dx, dy: dx == 0 or dy == 0 or abs(dx) == abs(dy),
                  'Q': lambda y, dx, dy: dx == 0 or dy == 0 or abs(dx) == abs(dy),
                  "k": lambda y, dx, dy: abs(dx) <= 1 and abs(dy) <= 1,
                  'K': lambda y, dx, dy: abs(dx) <= 1 and abs(dy) <= 1}

    for piece, rule in DIRECTIONS.items():

        EVERY_MOVE[piece] = []

        for i in range(64):
            EVERY_MOVE[piece].append([[] for _ in range(8)])

            # for each respective ray, taking the absolute difference
            # of their start and end positions orders them from closest
            # to farthest away on the board
            for target in sorted(range(64), key=lambda x, i=i: abs(x - i)):

                y = 8 - i // 8
                dy = (8 - target // 8) - y
                dx = (target % 8) - (i % 8)

                # determine if it's a valid move
                if i == target or not rule(y, dx, dy):
                    continue
                
                # determine which ray it belongs to
                angle = atan2(dy, dx)
                if angle in RAY_ANGLES:
                    rayIndex = RAY_ANGLES.index(angle) % 8
                    EVERY_MOVE[piece][i][rayIndex].append(target)

            # Re-append non-empty lists
            EVERY_MOVE[piece][i] = [ray for ray in EVERY_MOVE[piece][i] if ray]

    # Adding castling spots manually
    # 'k': black king, 4: 4th index on board, 0: 0th ray
    EVERY_MOVE['k'][4][0].append(6)
    EVERY_MOVE['k'][4][1].append(2)
    EVERY_MOVE['K'][60][0].append(62)
    EVERY_MOVE['K'][60][4].append(58)

    edge = 0 # if the piece is on the edge, the ray count is offset by one
    for i in range(8):
        EVERY_MOVE['P'][55 - i][edge].append(39 - i)
        EVERY_MOVE['p'][8 + i][edge].append(24 + i)
        edge = 1

    default_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    # 'check' is for creating a testboard where a move is valid even if
    # it puts their king in check, since it will be a move that takes
    # the opponent's king
    def __init__(self, fen=default_fen, check=True):
        self.board = Board()
        # Turn, Castling, En Passant Tracker, 50 move counter, Full move counter
        self.state = ["", "", "", 0, 1] 
        self.move_history = []
        self.fen_history = []
        self.check = check
        self.set_fen(fen)

    def __str__(self):
        return ' '.join([str(self.board)] + list(map(str, self.state)))

    def set_fen(self, fen):
        self.fen_history.append(fen)
        fen = fen.split()
        self.state[0] = fen[1] # Turn 'w' or 'b'
        self.state[1] = fen[2] # Castling KQkq
        self.state[2] = fen[3] # En Passant e6
        self.state[3] = int(fen[4]) # 50 move counter
        self.state[4] = int(fen[5]) # Full move counter
        self.board.set_board(fen[0])

    def reset(self, fen=default_fen):
        self.set_fen(fen)
        self.move_history = []
        self.fen_history = []

    def notation_to_index(self, notation):
        return (8 - int(notation[1])) * 8 + ord(notation[0]) - 97

    def index_to_notation(self, index):
        return chr(97 + index % 8) + str(8 - index // 8)

    def make_move(self, move): # Updates Board states as well as making the move
        # Indicies
        start = self.notation_to_index(move[0:2])
        end = self.notation_to_index(move[2:4])
        # Names
        piece = self.board.board[start]
        target = self.board.board[end]

        temp =  self.get_moves(self.state[0], i=[start])
        if self.check and move not in temp:
            #print("Invalid Move")
            return False

        newState = ['', '-', '-', 0, 1]

        if self.state[0] == "w":
            newState[0] = "b"
        else:
            newState[0] = "w"
        
        castleRights = {0: 'q', 7: 'k', 4: 'qk', 56: 'Q', 63: 'K', 60: 'KQ'}
        toRemove = ""
        for key in castleRights:
            if key == start or key == end:
                toRemove += castleRights[key]
        newCastleRights = []
        for right in self.state[1]:
            if right not in toRemove:
                newCastleRights.append(right)
        newState[1] = ''.join(newCastleRights)
        if newState[1] == '':
            newState[1] = '-'

        if piece.lower() == 'p' and abs(start - end) == 16:
            newState[2] = self.index_to_notation((start + end) // 2)

        newState[3] += 1
        if piece.lower() == 'p': # add capture detection later
            newState[3] = 0

        if self.state[4] != 1:
            newState[4] = self.state[4]
        if self.state[0] == 'b': # upcoming turn is white so black ups the turn
            newState[4] += 1

        if len(move) == 5:
            piece = move[4]
            if self.state[0] == 'w': 
                piece = piece.upper()

        self.move_history.append(move)
        self.board.move_piece(start, end, piece)

        castleMove = {62: 'K', 58: 'Q', 6: 'k', 2: 'q'}
        castleType = castleMove.get(end)
        if piece.lower() == 'k' and castleType and castleType in self.state[1]:
            rookMove = {'K': (63, 61), 'Q': (56, 59), 'k': (7, 5), 'q': (0, 3)}
            rookType = rookMove[castleType]
            rookSide = self.board.board[rookType[0]] # either "R" or 'r
            self.board.move_piece(rookType[0], rookType[1], rookSide)

        if piece.lower() == 'p' and self.state[2] != '-' \
                                and self.notation_to_index(self.state[2]) == end:
            if self.notation_to_index(self.state[2]) < 24:
                self.board.move_piece(end + 8, end + 8, ' ')
            else: self.board.move_piece(end - 8, end - 8, ' ')

        self.set_fen(' '.join(str(item) for item in [self.board] + newState))

    def get_moves(self, player, i=range(64)):
        if not self.check:
            return self.player_moves(player, i=i)

        result = []

        testBoard = Game(fen=str(self), check=False)
        for move in self.player_moves(player, i=i):
            
            kingColor = 'K' if player == 'w' else 'k'
            opponent = 'w' if player == 'b' else 'b'
            kingTile = self.index_to_notation(self.board.board.index(kingColor))
            dx = abs(self.board.board.index(kingColor) - self.notation_to_index(move[2:4]))

            # check for castling
            if move[0:2] == kingTile and dx == 2:
                attackedTiles = [move[2:4] for move in testBoard.get_moves(opponent)]
                gapMove = {'e1g1': 'e1f1', 'e1c1': 'e1d1', 'e8g8': 'e8f8', 'e8c8': 'e8d8'}.get(move)

                if kingTile in attackedTiles or gapMove and gapMove not in result:
                    continue

            testBoard.make_move(move)
            attackedTiles = []
            for tempMove in testBoard.get_moves(opponent):
                attackedTiles.append(self.notation_to_index(tempMove[2:4]))
            if testBoard.board.board.index(kingColor) not in attackedTiles:
                result.append(move)

            testBoard.reset(fen=str(self))

        return result

    def player_moves(self, player, i=range(64)):
        result = []
        for tile in i:
            if self.board.get_player(tile) == player:
                piece = self.board.board[tile]
                rays = self.EVERY_MOVE.get(piece)
                

                for ray in rays[tile]:
                    moves = self.eval_ray(tile, piece, ray, player)
                    result.extend(moves)

        return result

    def eval_ray(self, start, piece, ray, player):
        result = []
        
        for tile in ray:
            move = [self.index_to_notation(start) + self.index_to_notation(tile)]
            dx = abs(tile - start) % 8
            # if this is False it means there's no piece there
            tileOwner = self.board.get_player(tile)

            if tileOwner == player:
                break

            if piece.lower() == 'k' and dx == 2:
                # False if empty
                gap1 = self.board.get_player((start + tile) // 2) # the gap for castling
                gap2 = self.board.get_player(tile - 1) # second gap only applicable for queenside castling
                castleRights = {62: 'K', 58: 'Q', 6: 'k', 2: 'q'}
                rights = castleRights.get(tile)
                if tileOwner or gap1 or rights not in self.state[1] or \
                   (rights.lower() == 'q' and gap2):
                   break

            if piece.lower() == 'p':
                if dx == 0 and tileOwner:
                    break
                
                elif dx != 0 and not tileOwner:
                    if self.state[2] == "-" or tile != self.notation_to_index(self.state[2]):
                        break

                if tile < 8 or tile > 55:
                    for char in "bnrq":
                        move.append(move[0] + char)
                    del move[0]
        
            result.extend(move)

            if tileOwner:
                break 
        
        return result

    def check_status(self): # to check if it's black win, white win, or draw
        moves = self.get_moves(self.state[0])
        enemyMoves = [move[2:4] for move in self.get_moves({'w': 'b', 'b': 'w'}.get(self.state[0]))]
        if self.state[0] == 'w':
            inCheck = self.index_to_notation(self.board.board.index('K')) in enemyMoves
        else:
            inCheck = self.index_to_notation(self.board.board.index('k')) in enemyMoves
        if len(moves) == 0:
            if inCheck:
                if self.state[0] == 'w':
                    print("Black wins")
                    return 'b'
                else:
                    print("White wins")
                    return 'w'
            else:
                print("Stalemate")
                return 's'
        return ''

def main():
    game1 = Game()
    print(game1)
    print()
    print(game1.board.all_moves())
    print()
    print(game1.extra_moves())
    game1.make_move("e2e3")
    print(game1)

# main()