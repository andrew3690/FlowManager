import sched
import time
from requests.exceptions import Timeout
import requests
from datetime import datetime as dt

currenttime = time.strftime("%H:%M") # actual hour, must sum +3, due to instance being from UK
actualday = dt.today().strftime('%A')
week_days = ["Monday","Tuesday","Wendesday","Thursday","Friday","Saturday","Sunday"] #days of the week

urls = {
    # Stockout
    "stockout": 'https://prod-154.westus.logic.azure.com:443/workflows/95a2d9a704674e38b2b44596b7cdd878/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=RRCU5_EHl6xHkzhpKgrIVOCntQzCzFCzvkUecphDxaI',
    "reportdi": 'https://prod-108.westus.logic.azure.com:443/workflows/8895e7b9f59547ffac8b53fa42ecddab/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=TuNClx63T1rbvoCVjuCZkFbhyCz1lQocbi7g1Z--9xM'
    #"reporta4":,
    #"reportInterA4":,
    #"reportstock":,
    #"reportusa":,
    #"reporthomedepot":,
    #"topline":,
    #"dailyexcels":
}
  
# instance is created
scheduler = sched.scheduler(time.time,
                            time.sleep)
  
# function to print time and
# name of the event
def trigger(name):
    try:
        request = requests.post(urls[name]) # Http request sender 
    except Timeout:
        print(f"Http Request unsucessfull on {actualday} at {currenttime}, content: {request.json}") # returning sucess http requests
    else:
        print(f"Http Request sucessfull on {actualday} at {currenttime}, content: {request.json}") # returning sucess http requests
  
# printing starting time
  
# event x with delay of 1 second
# enters queue using enterabs method
if (currenttime == "7:00" and actualday in week_days):
        stockout = scheduler.enterabs(time.time(), 1,
                         trigger, 
                         argument = ("stockout", ))

        reportdi = scheduler.enterabs(time.time()+1, 1,
                         trigger, 
                         argument = ("reportdi", ))

'''
reporta4 = scheduler.enterabs(time.time()+1, 2,
                         trigger, 
                         argument = ("reporta4", ));
'''
# executing the events
scheduler.run()