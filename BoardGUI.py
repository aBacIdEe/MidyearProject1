from tkinter import *
from PIL import Image, ImageTk
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

'''imgSmall = tkinter.PhotoImage(file='images/'+imageName)
    w = tkinter.Label(self, image=imgSmall)
    w.photo = imgSmall
    w.grid(row=r2,column=1)'''

IMAGESOFPIECES = {
    'r': 'images/blackrookpiece.png',
    'R': 'images/whiterookpiece.png',
    'n': 'images/blackknightpiece.png',
    'N': 'images/whiteknightpiece.png',
    'b': 'images/blackbishoppiece.png',
    'B': 'images/whitebishoppiece.png',
    'q': 'images/blackqueenpiece.png',
    'Q': 'images/whitequeenpiece.png',
    'k': 'images/blackkingpiece.png',
    'K': 'images/whitekingpiece.png',
    'p': 'images/blackpawnpiece.png',
    'P': 'images/whitepawnpiece.png',
    '': 'images/blankspace.png'
}

# Setting up the board        
chess = bm.Board()
chess.load_board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.buttonList = []
        self.create_widgets()

    def getPos(self, r, c, t):
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
            for i in range(len(self.buttonList)):
                if str(chess.board[i]) != "0":
                    pieceImg = Image.open(IMAGESOFPIECES[str(chess.board[i])])
                    pieceImg = pieceImg.resize((50,50))
                    convertedImg = ImageTk.PhotoImage(pieceImg)
                    self.buttonList[i].photo = convertedImg
                    self.buttonList[i]['image'] = convertedImg
                else: 
                    pieceImg = Image.open('images/blankspace.png')
                    pieceImg = pieceImg.resize((50,50))
                    convertedImg = ImageTk.PhotoImage(pieceImg)
                    self.buttonList[i].photo = convertedImg
                    self.buttonList[i]["image"] = convertedImg

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
        self.imagesUsed = []
        x = 0
        self.rowLabels = list('abcdefgh')
        w, h = 70, 60
        for row in range(1,9):
            for column in range(1,9):
                t = str(chess.board[x])
                if t == '0':
                    t = ''
                if t != '':
                    '''imgSmall = tkinter.PhotoImage(file='images/'+imageName)
                        w = tkinter.Label(self, image=imgSmall)
                        w.photo = imgSmall
                        w.grid(row=r2,column=1)'''
                    pieceImg = Image.open(IMAGESOFPIECES.get(t))
                    pieceImg = pieceImg.resize((50,50))
                    convertedImg = ImageTk.PhotoImage(pieceImg)
                elif t == '':
                    pieceImg = Image.open("images/blankspace.png")
                    pieceImg = pieceImg.resize((50,50))
                    convertedImg = ImageTk.PhotoImage(pieceImg)
                if row%2==0:
                    if column%2==0:
                        self.buttonList.append(Button(self, width=w, height=h, image=convertedImg, bg='white', command=(lambda r,c,t: lambda:self.getPos(r,c,t))(row,column)))
                        self.buttonList[-1].photo = convertedImg
                        self.buttonList[-1].grid(row=row,column=column)
                    else: 
                        self.buttonList.append(Button(self, width=w, height=h, image=convertedImg, bg='tan', command=(lambda r,c: lambda:self.getPos(r,c))(row,column)))
                        self.buttonList[-1].photo = convertedImg
                        self.buttonList[-1].grid(row=row,column=column)
                else:
                    if column%2==0:
                        self.buttonList.append(Button(self, width=w, height=h, image=convertedImg, bg='tan', command=(lambda r,c,t: lambda:self.getPos(r,c,t))(row,column)))
                        self.buttonList[-1].photo = convertedImg
                        self.buttonList[-1].grid(row=row,column=column)
                    else:    
                        self.buttonList.append(Button(self, width=w, height=h, image=convertedImg, bg='white', command=(lambda r,c,t: lambda:self.getPos(r,c,t))(row,column)))
                        self.buttonList[-1].photo = convertedImg
                        self.buttonList[-1].grid(row=row,column=column)
                x += 1
            Label(self, text=row).grid(row=9-row,column=0)
            Label(self,image=convertedImg).grid(row=10,column=0)
        for i in range(len(self.rowLabels)):
            Label(self, text=self.rowLabels[i]).grid(row=9,column=i+1)

root = Tk()
root.title('Board GUI')
app = Application(root)
root.mainloop()