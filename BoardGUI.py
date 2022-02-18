from tkinter import *
from Timer import Timer
from PIL import Image, ImageTk
import GameModel as gm

GRIDLIST = ['a8 b8 c8 d8 e8 f8 g8 h8'.split(),
            'a7 b7 c7 d7 e7 f7 g7 h7'.split(),
            'a6 b6 c6 d6 e6 f6 g6 h6'.split(),
            'a5 b5 c5 d5 e5 f5 g5 h5'.split(),
            'a4 b4 c4 d4 e4 f4 g4 h4'.split(), 
            'a3 b3 c3 d3 e3 f3 g3 h3'.split(),
            'a2 b2 c2 d2 e2 f2 g2 h2'.split(),
            'a1 b1 c1 d1 e1 f1 g1 h1'.split()]

BUTTONS = []

'''imgSmall = PhotoImage(file='images/'+imageName)
    w = Label(self, image=imgSmall)
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
chess = gm.Game()
class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.buttonList = []
        self.set_obj = 0
        self.white_time_over = False #time over meaning time has ended
        self.black_time_over = True
        self.turn = True #True means white, False means black
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
            chess.make_move(self.moves[-1] + pos)
            print(str(chess))
            for i in range(len(self.buttonList)):
                if str(chess.board.board[i]) != " ":
                    pieceImg = Image.open(IMAGESOFPIECES[str(chess.board.board[i])])
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
        self.updateTurnLabel()

    def updateTurnLabel(self):
        self.turnLabel['text'] = chess.state[0]

    def isButtonPressed(self):
        if self.buttonPressed:
            # the button that was just pressed is the second button
            # perform tasks
            self.buttonPressed = False
            return True
        else:
            self.buttonPressed = True
            return False

    # Timer functions
    def set_seconds(self):
        self.seconds = int(self.seconds_ent.get())
        self.set_obj += 1
        self.seconds_ent.grid_forget()
        self.seconds_bttn.grid_forget()
        self.set_object()
        
        
    def set_increment(self):
        self.increment = int(self.inc_ent.get())
        self.set_obj += 1
        self.inc_ent.grid_forget()
        self.inc_bttn.grid_forget()
        self.set_object()

    def set_object(self):
        if self.set_obj >= 2:
            self.white = Timer(self.seconds, self.increment)
            self.black = Timer(self.seconds, self.increment)
            self.show_timer()
            self.update()

    def show_timer(self):
        self.white_timer['text'] = self.white.string()
        self.black_timer['text'] = self.black.string()
    
    def add_increment(self):
        if self.turn == True:
            self.white.add_increment()
        else: self.black.add_increment(); self.update_turn()
        self.show_timer()
        self.update_turn()

    def update(self):
        if self.white.time > 0:
            if self.turn == True:
                self.white.time -= 1
            else:
                self.black.time -= 1
            self.show_timer()
            self.after(1000, self.update)
        else:
            if self.turn == True: self.white_time_over = True
            else: self.black_time_over = True
    
    def update_turn(self):
        if self.turn == True: self.turn = False
        else: self.turn = True            

    def create_widgets(self):
        self.buttonPressed = False
        self.moves = []
        self.imagesUsed = []
        x = 0
        self.rowLabels = list('abcdefgh')
        w, h = 70, 60
        for row in range(1,9):
            for column in range(1,9):
                t = str(chess.board.board[x])
                if t != ' ':
                    pieceImg = Image.open(IMAGESOFPIECES.get(t, "images/blankspace.png"))
                    pieceImg = pieceImg.resize((50,50))
                    convertedImg = ImageTk.PhotoImage(pieceImg)
                elif t == ' ':
                    pieceImg = Image.open("images/blankspace.png")
                    pieceImg = pieceImg.resize((50,50))
                    convertedImg = ImageTk.PhotoImage(pieceImg)
                if row%2==0:
                    if column%2==0:
                        self.buttonList.append(Button(self, width=w, height=h, image=convertedImg, bg='white', command=(lambda r,c: lambda:self.getPos(r,c))(row,column)))
                        self.buttonList[-1].photo = convertedImg
                        self.buttonList[-1].grid(row=row,column=column)
                    else: 
                        self.buttonList.append(Button(self, width=w, height=h, image=convertedImg, bg='tan', command=(lambda r,c: lambda:self.getPos(r,c))(row,column)))
                        self.buttonList[-1].photo = convertedImg
                        self.buttonList[-1].grid(row=row,column=column)
                else:
                    if column%2==0:
                        self.buttonList.append(Button(self, width=w, height=h, image=convertedImg, bg='tan', command=(lambda r,c: lambda:self.getPos(r,c))(row,column)))
                        self.buttonList[-1].photo = convertedImg
                        self.buttonList[-1].grid(row=row,column=column)
                    else:    
                        self.buttonList.append(Button(self, width=w, height=h, image=convertedImg, bg='white', command=(lambda r,c: lambda:self.getPos(r,c))(row,column)))
                        self.buttonList[-1].photo = convertedImg
                        self.buttonList[-1].grid(row=row,column=column)
                x += 1
            Label(self, text=row).grid(row=9-row,column=0)
            Label(self,image=convertedImg).grid(row=10,column=0)
        for i in range(len(self.rowLabels)):
            Label(self, text=self.rowLabels[i]).grid(row=9,column=i+1)
        self.turnLabel = Label(self,text='White')
        self.turnLabel.grid(row=10,column=0,columnspan=10)

        # TIMER

        self.white_timer = Label(self, text = "insert time", bg = "white", fg = "black")
        self.white_timer.grid(row = 5, column = 11, sticky = W)#get two of these

        self.black_timer = Label(self, text = "insert time", bg = "black", fg = "white")
        self.black_timer.grid(row = 0, column = 11, sticky = W)

        self.seconds_bttn = Button(self, text = "How much seconds?", command = self.set_seconds)
        self.seconds_bttn.grid(row = 1, column = 12, sticky = E)

        self.seconds_ent = Entry(self)
        self.seconds_ent.grid(row = 1, column = 11, sticky = W)

        self.inc_bttn = Button(self, text = "Increment", command = self.set_increment)
        self.inc_bttn.grid(row = 2, column = 12, sticky = E)

        self.inc_ent = Entry(self)
        self.inc_ent.grid(row = 2, column = 11, sticky = W)


root = Tk()
root.title('Board GUI')
app = Application(root)
root.mainloop()