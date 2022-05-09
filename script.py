#!/usr/bin/env python3
from datetime import datetime as dt
from threading import Timer
import time, sched
import requests
from requests.exceptions import Timeout

# Getting hour of the day, flows must be triggred at 6:50 (UTC - 3) Brasília Hour
currenttime = time.strftime("%H:%M") # actual hour, must sum +3, due to instance being from UK


# Getting current day of the week
dayofweek = dt.today().strftime('%A')

# Days of the week  
week_days = {0:"Monday",1:"Tuesday",2:"Wendesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"} #days of the week

# needing more urls to send Http requests
urls = {
    # Stockout
    "stockout": '',
    # A1 - Reporte Diário Metais, Pincéis e Tubos
	"reportdi": '',
	# Reports Fretes A4
	"reporta4": '',
	# Report Internacional A4	
	"reportInterA4":'',
	# Enviar Reportes A1
	"reporta1": '',
	# Enviar Report A4 - Daily Excels Dura (Orders,Central)
	"reportdailydura": '',
	# Top Line - A1	
	"topline":'',
	# A4 - HomeDepot Inventory Report	
	"homedepot":'',
	# Report USA - OrdersBookedA4	
	"reportusa":''

}

actualday = dt.today().strftime('%A') # getting actual day of the week  

#
class Event:
    def __init__(self,name,days,hour,minute):
        self.name = name
        self.hour = hour
        self.minute = minute
        self.days = list(days)
        self.date = dt.today().strftime('%A')   # day of the week, same as week_days dict Ex: Monday = 0
    
    # getter to identify which event has been trigger
    def getevent(self):
        evento, dia, hora = self.name, actualday, f"{self.hour}:{self.minute}"
        print(f'Triggering flow {evento},on {dia},at {hora}')

    # Flow Trigger
    def trigger(self,name):
        try:
            request = requests.post(urls[name]) # Http request sender
            print(self.getevent())
        except Timeout:
            print(f"Http Request unsucessfull on {week_days[self.actday]} at {currenttime}, content: {request.json}") # returning failure http requests
        else:
            print(f"Http Request sucessfull on {week_days[self.actday]} at {currenttime}, content: {request.json}") # returning sucess http requests
    
    # Flow manager, gets hours and minutes and excecution name of the requested Flows
    def manager(self): 
        hr = f"{self.hour}:{self.minute}"
        exc_days = self.days
        currt_day = self.date
        if (currt_day in exc_days): # evaluating if it is day for excuting the requested flow
            if(currenttime == hr):	# evaluating if current hour is avaliable for sending http request
                self.trigger(self.name)

if __name__ == '__main__':
    # Stockout
    reportstock = Event("stockout",[0,2,4],10,50) # Mondays, wendesdays, fridays
    reportstock = Event("stockout",[1,3],10,40)	  # Tuesdays an Thursdays
    reportstock.manager()

    # A1 - Reporte Diário Metais, Pincéis e Tubos 
    
    reportdi = Event("reportdi",[0,1,2,3,4],10,00) # Every day of the week
    reportdi.manager()

    # Reports Fretes A4
    reporta4 = Event("reporta4",[0,1,2,3,4],10,00) # Every day of the week
    reporta4.manager()

    # Report Internacional A4
    reportInterA4 = Event("reportintera4",[0,2,4],10,10) # Mondays, Wendesdays and Fridays
    reportInterA4.manager()

    # Enviar Reportes A1
    reportstock = Event("stockout",[0,2,4],10,50) # Mondays, Wendesdays and Fridays
    reportstock = Event("stockout",[1,3],10,40) # Tuesdays an Thursdays
    reportstock.manager()

    # Report USA - OrdersBookedA4
    reportusa = Event("reportusa",[0,2,4],11,10) # Mondays, Wendesdays and Fridays
    reportusa = Event("reportusa",[1,3],11,00) # Tuesdays an Thursdays
    reportusa.manager()

    # A4 - HomeDepot Inventory Report
    reporthomedepot = Event("reporthomedepot",[0,2,4],14,00) # Mondays, Wendesdays and Fridays
    reporthomedepot.manager()

    # Top Line - A1
    topline = Event("topline",[0,1,2,3,4],19,00) # Every day of the week
    topline.manager()

    # Enviar Report A4 - Daily Excels Dura (Orders,Central)	
    dailyexcels = Event("dailyexcels",[0,1,2,3,4],00,00) # Every day of the week 
    dailyexcels.manager()