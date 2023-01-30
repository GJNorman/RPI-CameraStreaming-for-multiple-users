
import time
#basic Timer       
class Scheduler():
    def __init__(self, timeoutPeriod:float = 1):
        self.referenceTime = self.getTime()
        self.timeoutPeriod = timeoutPeriod
        
    def getTime(self):
        return time.perf_counter()
    
    #check if "timeoutPeriod" has passed
    #update reference timer if so
    def CheckTimeout(self) -> bool:
        time_now = self.getTime()
        if ((time_now - self.referenceTime) >= self.timeoutPeriod):
            self.referenceTime = time_now #self.getTime()
            return True
        return False
