from cProfile import label
from tkinter import *
from PIL import Image, ImageTk

class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        bttn = PhotoImage(file='images/blackbishoppiece.png')
        b = Button(self, image=bttn)
        b.grid(row=0,column=0)

root = Tk()
app = Application(root)
root.mainloop()