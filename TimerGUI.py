import Timer as tm
import time
import tkinter
from tkinter.constants import W

class Application(tkinter.Frame):
    def __init__(self, master, obj):
        super().__init__(master)
        self.grid()
        self.create_widgets()
        self.obj = obj #obj is timer object, maybe make it not it init so it can be changed

    def create_widgets(self):
        self.timer = tkinter.Label(self)
        self.timer.grid(row = 0, column = 0, sticky = W)
        self.timer['text'] = tm.__str__(self.obj)

        self.give_time_bttn = tkinter.Entry(self)
        self.give_time_bttn.grid()



root = tkinter.Tk
root.title("Timer GUI")
app = Application(root)
root.mainloop()