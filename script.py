#!/usr/bin/env python3
from datetime import datetime as dt
from threading import Timer
import time, sched
import schedule
import requests
from requests.exceptions import Timeout

# Getting hour of the day, flows must be triggred at 6:50 (UTC - 3) Brasília Hour
currenttime = time.strftime("%H:%M") # actual hour, must sum +3, due to instance being from UK
# print(type(currenttime))
# Getting current day of the week
dayofweek = dt.today().strftime('%A')
 
week_days = {0:"Monday",1:"Tuesday",2:"Wendesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"} #days of the week

urls = {
    "stockout": 'https://prod-154.westus.logic.azure.com:443/workflows/95a2d9a704674e38b2b44596b7cdd878/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=RRCU5_EHl6xHkzhpKgrIVOCntQzCzFCzvkUecphDxaI'
}

day = dt.today() # getting today's date  

#
class Event:
    def __init__(self,name,days,hour,minute):
        self.name = name
        self.hour = hour
        self.minute = minute
        self.days = list(days)
        self.date = day.weekday()   # day of the week, same as week_days dict Ex: Monday = 0
    
    # getter to identify which event has been trigger
    def getevent(self):
        evento, dia, hora = self.name, self.day, f"{self.hour}:{self.minute}"
        print(f'Triggering flow {evento},on {dia},at {hora}')

    # Flow Trigger
    def trigger(self,name):
        try:
            request = requests.post(urls[name]) # Http request sender 
        except Timeout:
            print(f"Http Request unsucessfull on {week_days[self.actday]} at {currenttime}, content: {request.json}") # returning sucess http requests
        else:
            print(f"Http Request sucessfull on {week_days[self.actday]} at {currenttime}, content: {request.json}") # returning sucess http requests
    # Flow manager, gets hours and minutes and excecution name of the requested Flows
    def manager(self): 
        hr = f"{self.hour}:{self.minute}"
        exc_days = self.days
        currt_day = self.date
        if (currt_day in exc_days):
            if(currenttime == hr):
                self.trigger(self.name)
            # schedule.every().day.at(hr).do(self.trigger(self.name))
        
if __name__ == '__main__':
    stockout = Event("stockout",[0,2,4],15,29)
    stockout.manager()