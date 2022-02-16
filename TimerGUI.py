from Timer import Timer 
import tkinter
from tkinter.constants import W, E

class Application(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.create_widgets()
        self.set_obj = 0
        self.white_time_over = False #time over meaning time has ended
        self.black_time_over = True
        self.turn = True #True means white, False means black

    def create_widgets(self):
        self.white_timer = tkinter.Label(self)
        self.white_timer.grid(row = 0, column = 0, sticky = W)#get two of these

        self.black_timer = tkinter.Label(self)
        self.black_timer.grid(row = 0, column = 1, sticky = W)

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
        

    def give_time(self):
        #check who is giving who
        if self.turn == True: self.white.time += int(self.give_time_ent.get())
        else: self.black.time += int(self.give_time_ent.get())
        self.show_timer()

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
            

root = tkinter.Tk()
root.title("Timer GUI")
app = Application(root)
root.mainloop()