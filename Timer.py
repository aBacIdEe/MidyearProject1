import time

class Timer():
    def __init__(self, time, increment):
        #time is given as number of seconds
        self.time = time
        self.increment = increment

    def pause_timer(self):
        self.update_timer(False)
        #this should be done when a player makes a move

    def resume_timer(self):
        self.update_timer(True)
        #this should be done when the other player makes a move

    def update_timer(self, truefalse):
        #updates clock every second
        while truefalse == True:
            # TODO
            pass
        # TODO
        pass

    def add_increment(self):
        self.time += self.increment
        #this should be done when a player makes a move