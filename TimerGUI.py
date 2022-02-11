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
        self.time_over = False

    def create_widgets(self):
        self.timer = tkinter.Label(self)
        self.timer.grid(row = 0, column = 0, sticky = W)

        tkinter.Button(self, text = "How much seconds?", command = self.set_seconds).grid(row = 1, column = 0, sticky = E)
        self.seconds_ent = tkinter.Entry(self)
        self.seconds_ent.grid(row = 1, column = 1, sticky = W)

        tkinter.Button(self, text = "Increment", command = self.set_increment).grid(row = 2, column = 0, sticky = E)
        self.inc_ent = tkinter.Entry(self)
        self.inc_ent.grid(row = 2, column = 1, sticky = W)


        tkinter.Button(self, text = "Give time", command = self.give_time).grid(row = 3, column = 0, sticky = E)
        self.give_time_ent = tkinter.Entry(self)
        self.give_time_ent.grid(row = 3, column = 1, sticky = W)


    def set_seconds(self):
        self.seconds = int(self.seconds_ent.get())
        self.set_obj += 1
        self.set_object()
        
    def set_increment(self):
        self.increment = int(self.inc_ent.get())
        self.set_obj += 1
        self.set_object()

    def set_object(self):
        if self.set_obj >= 2:
            self.obj = Timer(self.seconds, self.increment)
            self.start_timer()
            self.update()

    def start_timer(self):
        self.timer['text'] = self.obj.string()
    
    def add_increment(self):
        self.obj.add_increment()
        self.start_timer()

    def give_time(self):
        self.obj.time += int(self.give_time_ent.get())
        self.start_timer()

    def update(self):
        if self.obj.time > 0:
            self.obj.time -= 1
            self.start_timer()
            self.after(1000, self.update)
        else: self.time_over = True
            

root = tkinter.Tk()
root.title("Timer GUI")
app = Application(root)
root.mainloop()