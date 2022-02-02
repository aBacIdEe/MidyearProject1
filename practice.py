from tkinter import *

class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def hover(self, e):
        self.bttn['bg'] = 'red'

    def leave(self, e):
        self.bttn['bg'] = 'blue'

    def create_widgets(self):
        self.bttn = Button(self, text='hi', bg='blue')
        self.bttn.bind('<Enter>', self.hover)
        self.bttn.bind('<Leave>', self.leave)
        self.bttn.grid()

root = Tk()
app = Application(root)
root.mainloop()