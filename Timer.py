class Timer():
    def __init__(self, time, increment):
        self.time = time
        self.increment = increment

    def __str__(self):
        return self.string()
    
    def string(self):
        mm, ss = divmod(self.time, 60)
        hh, mm = divmod(mm, 60)
        return f"{hh:02d}:{mm:02d}:{ss:02d}"

    def add_increment(self):
        self.time += self.increment
        #this should be done when a player makes a move