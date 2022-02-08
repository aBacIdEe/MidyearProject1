import time

class Timer():
    def __init__(self, time, increment):
        #time is given as number of seconds
        self.time = time #should be less than a day
        self.increment = increment
        self.resume_timer()

    def __str__(self):
        minutes = -1
        hours = -1
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
        if self.time > 0:
            while truefalse == True:
                time.sleep(1)
                self.time -= 1
        #what do I do when time runs out?

    def add_increment(self):
        self.time += self.increment
        #this should be done when a player makes a move

obj = Timer(1000,10)
print(str(obj))
obj.resume_timer()
print(str(obj))
obj.resume_timer()
print(str(obj))
obj.resume_timer()
print(str(obj))
obj.resume_timer()
print(str(obj))
obj.resume_timer()
print(str(obj))
obj.resume_timer()
print(str(obj))