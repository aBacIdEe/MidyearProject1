from tkinter import *

import BoardModel as bm

GRIDLIST = ['a8 b8 c8 d8 e8 f8 g8 h8'.split(),
            'a7 b7 c7 d7 e7 f7 g7 h7'.split(),
            'a6 b6 c6 d6 e6 f6 g6 h6'.split(),
            'a5 b5 c5 d5 e5 f5 g5 h5'.split(),
            'a4 b4 c4 d4 e4 f4 g4 h4'.split(), 
            'a3 b3 c3 d3 e3 f3 g3 h3'.split(),
            'a2 b2 c2 d2 e2 f2 g2 h2'.split(),
            'a1 b1 c1 d1 e1 f1 g1 h1'.split()]

BUTTONS = []

# Setting up the board        
chess = bm.Board()
chess.load_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def getPos(self, r, c):
        '''Gets the grid position of the position using row and column'''
        pos = (GRIDLIST[r-1][c-1])
        pressed = self.isButtonPressed()
        if not pressed:
            # this is the first button
            self.moves.append(pos)
        else:
            # this is the second button being pressed
            # getting the last move
            chess.move_piece(self.moves[-1], pos)

    def isButtonPressed(self):
        if self.buttonPressed:
            # the button that was just pressed is the second button
            # perform tasks
            self.buttonPressed = False
            return True
        else:
            self.buttonPressed = True
            return False

    def create_widgets(self):
        self.buttonPressed = False
        self.moves = []
        x = 0
        self.rowLabels = list('abcdefgh')
        for row in range(1,9):
            for column in range(1,9):
                t = str(chess.board[x])
                if t == '0':
                    t = ''
                if row%2==0:
                    if column%2==0:
                        # self.printPos(row,column)
                        Button(self, width=6, height=3, text=t, bg='white', command=(lambda r,c: lambda:self.getPos(r,c))(row,column)).grid(row=row,column=column)
                    else:
                        # self.printPos(row,column)
                        # (lambda r,c: lambda:self.printPos(r,c))(row,column)
                        Button(self, width=6, height=3, text=t, bg='tan', command=(lambda r,c: lambda:self.getPos(r,c))(row,column)).grid(row=row,column=column)
                else:
                    if column%2==1:
                        Button(self, width=6, height=3, text=t, bg='white', command=(lambda r,c: lambda:self.getPos(r,c))(row,column)).grid(row=row,column=column)
                    else:
                        # self.printPos(row,column)
                        Button(self, width=6, height=3, text=t, bg='tan', command=(lambda r,c: lambda:self.getPos(r,c))(row,column)).grid(row=row,column=column)
                x += 1
            Label(self, text=row).grid(row=9-row,column=0)
        for i in range(len(self.rowLabels)):
            Label(self, text=self.rowLabels[i]).grid(row=9,column=i+1)

root = Tk()
root.title('Board GUI')
app = Application(root)
root.mainloop()