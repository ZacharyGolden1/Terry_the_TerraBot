from monitor import *
import os
from datetime import datetime 
class LoggingMonitor(Monitor):

    def __init__(self, period=10):
        super(LoggingMonitor, self).__init__("LoggingMonitor", period)
        # Put any iniitialization code here
        # BEGIN STUDENT CODE
        self.filename = None
        # END STUDENT CODE

    def perceive(self):
        # BEGIN STUDENT CODE
        self.sensordata =  self.sensordata
        self.time = self.sensordata['unix_time']
        self.actuator_state =  self.actuator_state
        self.clock_time = datetime.utcfromtimestamp(self.time)
        # END STUDENT CODE
      
    
    def clock_time(self,unix):
        return datetime.utcfromtimestamp(unix)
    
    def monitor(self):
        folder = "allLogs"
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        if (not self.filename):
            self.filename = os.path.join(folder,f"log{int(self.time)}.txt")
        with open(self.filename, 'a') as f:
            time = str(self.clock_time)
            f.write(time)
            for key in self.sensordata:
                f.write(f", {key}: {self.sensordata[key]}")
            for key in self.actuator_state:
                f.write(f", {key}: {self.actuator_state[key]}")
            f.write("\n")

