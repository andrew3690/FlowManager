#!/usr/bin/env python3
from datetime import datetime as dt
from threading import Timer
import time, sched
import requests

# Getting hour of the day, flows must be triggred at 6:50 (UTC - 3) Brasília Hour
currenttime = time.strftime("%H:%M") # actual hour, must sum +3, due to instance being from UK
print(type(currenttime))
# Getting current day of the week
dayofweek = dt.today().strftime('%A')
 
week_days = {0:"Monday",1:"Tuesday",2:"Wendesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"} #days of the week

urls = {
    "stockout": 'https://prod-154.westus.logic.azure.com:443/workflows/95a2d9a704674e38b2b44596b7cdd878/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=RRCU5_EHl6xHkzhpKgrIVOCntQzCzFCzvkUecphDxaI'
}

hora = {
    ":34": "stockout"
}
#
class Event:
    def __init__(self,name,day,hour,minute):
        self.name = name
        self.hour = hour
        self.minute = minute 
        self.day = week_days[day] # day of the week, same as week_days dict Ex: Monday = 0 

    # getter to identify which event has been trigger
    def getevent(self):
        evento, dia, hora = self.name, self.day, self.hour
        return f'Triggrering flow {evento},on {dia},at {hora}'

    # Flow Trigger
    def trigger(self,name):
        request = requests.post(urls[name]) # Http request sender
        date = dt.today()   # getting today's date
        actday = date.weekday() # getting current day of the week
        return f"Http Request sucessfull on {week_days[actday]} at {currenttime}, content: {request.json}" # returning sucess http requests  

    # Flow manager, gets hours and minutes and excecution name of the requested Flows
    def manager(self):
        x=dt.today()                                                # getting today's date 
        y=x.replace(day=x.day, hour=self.hour, minute=self.minute)  # formating day,hour and minute of the event execution   
        tgr = self.trigger(self.name)                               # Http POST request
        t = Timer(y,tgr)                                            # function caalling Timer
        t.start()                                                   # triggering data flow (Problem: compassion bettwen datetime.datetime and int can't be done)

stockout = Event("stockout",0,15,52)
stockout.trigger("stockout")
stockout.manager()  
