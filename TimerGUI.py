import Timer as tm
import time
import tkinter

class Application(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        pass

root = tkinter.Tk
root.title("Timer GUI")
app = Application(root)
root.mainloop()