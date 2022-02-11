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
        # minutes = -1
        # hours = -1
        # for min in range(0, self.time, 60):
        #     minutes += 1
        # for hour in range(0, minutes, 60):
        #     hours += 1
        
        # minutes = minutes % 60
        # seconds = self.time % 60
        # return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    # def pause_timer(self):
    #     self.update_timer(False)
    #     #this should be done when a player makes a move

    # def resume_timer(self):
    #     self.update_timer(True)
    #     #this should be done when the other player makes a move

    # def update_timer(self, truefalse):
    #     #updates clock every second
    #     if self.time > 0 and truefalse == True:
    #         time.sleep(1)
    #         self.time -= 1
    #     #what do I do when time runs out?

    def add_increment(self):
        self.time += self.increment
        #this should be done when a player makes a move

# obj = Timer(1000,10)
# print(str(obj))
# obj.resume_timer()
# print(str(obj))
# obj.resume_timer()
# print(str(obj))
# obj.resume_timer()
# print(str(obj))
# obj.resume_timer()
# print(str(obj))
# obj.resume_timer()
# print(str(obj))
# obj.resume_timer()
# print(str(obj))