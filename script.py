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
    "stockout": 'https://prod-154.westus.logic.azure.com:443/workflows/939f221ae6c642b5a53e911f9239a7bd/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=oE8KaUl0GcZsufQjHqGFd1EFrFjxhF5baU-nwfbvl64',
    # A1 - Reporte Diário Metais, Pincéis e Tubos
	"reportdi": 'https://prod-21.westus.logic.azure.com:443/workflows/3e1ad68b82b0446c93bc8eb9f6a5c57f/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=OU5qwZhocagJo-Nrhkuq33fyrmqJ-F5a-_u4PekERxI',
	# Reports Fretes A4
	"reporta4": 'https://prod-07.westus.logic.azure.com:443/workflows/f49f22e710b94fee93a74ed81dcfc115/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=JNSNVZF3zC8oXoHlhjHQqhoQN_6SDEgeI2p2gHw_aUg',
	# Report Internacional A4	
	"reportInterA4":'https://prod-148.westus.logic.azure.com:443/workflows/010bfcac5b5e4956a2db9dacf3494706/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=-IEEaeoew1quHxttnKrXcte_LVF1ubIlAW2QRENuiqQ',
	# Enviar Reportes A1
	"reporta1": 'https://prod-27.westus.logic.azure.com:443/workflows/21fd4b37ed21406cbe2c5fa17aa6c56b/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=PiHi4N4TwsMinAerVguSXHgLc4zB5LrNqd2xs6_buoc',
	# Enviar Report A4 - Daily Excels Dura (Orders,Central)
	"reportdailydura": 'https://prod-53.westus.logic.azure.com:443/workflows/5db7157bf1c14c5a811e2cba3e4bb0dc/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=klCW_etIs1tN5wDVUO0gEKh37iJXVZpuHrMnSCynVzg',
	# Top Line - A1	
	"topline":'https://prod-180.westus.logic.azure.com:443/workflows/0b105b3827ae46718bff30798ce7bbe7/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=zePvoBCtNc4u434_m97A_BWmuoSASg6E_5lX_o_GX-0',
	# A4 - HomeDepot Inventory Report	
	"homedepot":'https://prod-155.westus.logic.azure.com:443/workflows/0cbef8bdea834111b65f245c4b0ba9b8/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ukkCwi2GRzkWy2C9h5UE77eG5bOixCQsOH-Pt2shkJI',
	# Report USA - OrdersBookedA4	
	"reportusa":'https://prod-66.westus.logic.azure.com:443/workflows/467e2d0393f14bd4b9857fda80eb9263/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=kBRCmKW67X7kQyKU52taJ5mdcmT-uOCaC8UBmXGjYWo'

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