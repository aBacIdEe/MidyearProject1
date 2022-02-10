from Timer import Timer 
import time
import tkinter
from tkinter.constants import W, E, N

class Application(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.create_widgets()
        self.set_obj = 0

    def create_widgets(self):
        self.timer = tkinter.Label(self)
        self.timer.grid(row = 0, column = 0, sticky = W)

        tkinter.Label(self, text = "How much seconds?").grid(row = 1, column = 0, sticky = E)
        self.seconds_ent = tkinter.Entry(self)
        self.seconds_ent.grid(row = 1, column = 1, sticky = W)

        self.seconds_bttn = tkinter.Button(self, command = self.set_seconds)
        self.seconds_bttn.grid(row = 1, column = 2, sticky = N)

        tkinter.Label(self, text = "Incrememnt").grid(row = 2, column = 0, sticky = E)
        self.inc_ent = tkinter.Entry(self)
        self.inc_ent.grid(row = 2, column = 1, sticky = W)

        self.inc_bttn = tkinter.Button(self, command = self.set_incrememnt)
        self.inc_bttn.grid(row = 2, column = 2, sticky = N)

        tkinter.Label(self, text = "Give time").grid(row = 3, column = 0, sticky = E)
        self.give_time_ent = tkinter.Entry(self)
        self.give_time_ent.grid(row = 3, column = 1, sticky = W)

        self.add_inc_bttn = tkinter.Button(self, text = "increment", command = self.add_increment)
        self.add_inc_bttn.grid()

    def set_seconds(self):
        self.seconds = int(self.seconds_ent.get())
        self.set_obj += 1
        
    def set_incrememnt(self):
        self.increment = int(self.inc_ent.get())
        self.set_obj += 1

    def set_object(self):
        if self.set_obj >= 2:
            self.obj = Timer(self.seconds, self.increment)
            self.start_timer()

    def start_timer(self):
        self.timer['text'] = self.obj.string()
    
    def add_increment(self):
        pass

root = tkinter.Tk()
root.title("Timer GUI")
app = Application(root)
root.mainloop()