import time

class Timer():
    def __init__(self, time, increment):
        #time is given as number of seconds
        self.time = time #should be less than a day
        self.increment = increment

    def show_time(self):
        minutes = 0
        hours = 0
        for min in range(0, self.time, 60):
            minutes += 1
        for hour in range(0, minutes, 60):
            hours += 1
        
        minutes = minutes % 60
        seconds = self.time % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

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