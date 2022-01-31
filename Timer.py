import time

class Timer():
    def __init__(self, time, increment):
        #time is given as number of seconds
        self.time = time
        self.increment = increment

    def pause_timer(self):
        self.update_timer(False)

    def resume_timer(self):
        self.update_timer(True)

    def update_timer(self, truefalse):
        while truefalse == True:
            # TODO
            pass
        # TODO
        pass

    def add_increment(self):
        #adds given increment to time
        pass