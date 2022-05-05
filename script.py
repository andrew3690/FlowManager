#!/usr/bin/env python3
from datetime import datetime as dt
import time, sched
import requests

# Getting hour of the day, flows must be triggred at 6:50 (UTC - 3) Brasília Hour
currenttime = time.strftime("%H:%M") # actual hour, must sum +3, due to instance being from UK
print(type(currenttime))
# Getting current day of the week
dayofweek = dt.today().strftime('%A')

#days of the week 
week_days = {0:"Monday",1:"Tuesday",2:"Wendesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}
#days = week_days[0:5:2]  # slacing specific days for Stockout and USA reports sending

#
urls = {
    "stockout": 'https://www.google.com/'#'https://prod-154.westus.logic.azure.com:443/workflows/95a2d9a704674e38b2b44596b7cdd878/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=RRCU5_EHl6xHkzhpKgrIVOCntQzCzFCzvkUecphDxaI'
}

hora = {
    "9:34": "stockout"
}
#
class Event:
    def __init__(self):
        self.evento = evento
        self.dia = dia
        self.hora = hora

    # getter to identify, wich event has been trigger
    def getevent(self):
        event, day, hour= self.evento, self.dia, self.hora
        return f'Triggrering flow {event},on {day},at {hour}'
    
    # Flow Trigger
    def trigger(self,name):
        request = requests.post(urls[name])
    

    def controller(self):
        sched.every(5).seconds.do(self.trigger("stockout"))
    
a = Event
    


        




# Morning daily reports
def Daily_Manager(x):
    #while True:
        #try:
        # Reports Fretes A4, Reporte Diário Metais, Pincéis e Tubos.
    if (x == "8:24"):
        r = requests.post(urls["stockout"])
        print(f"A4 - Reports Fretes, request sucessfull at {x}, content: {r.text}")
		#time.sleep(10)
		#r = requests.post()
		#print(f"A1 - Reporte Diário Metais, Pincéis e Tubos, request sucessfull at {x}, content: {r.text}")		
		#Report Internacional A4
        '''
		elif (x == "10:10"):
			#r = requests.post()
			#print(f"A4 - Report Internacional, request sucessfull at {x}, content: {r.text})
		'''
		
		# Enviar Reportes A1
        '''
		elif (x == "10:45"):
			#r = requests.post()
			#print(f"A1 - Enviar Reportes A1, request sucessfull at {x}, content: {r.text}")
		'''

		# A1 - Enviar Reportes A1, A4 - HomeDepot Inventory Report
        '''
		elif (x == "11:00"):
			#r = requests.post()
			#return f"A4 - HomeDepot Inventory Report, request sucessfull at {x}, content: {r.text}"
			#time.sleep(10)
			#r = requests.post()
			#return f"A1 - Enviar Reportes A1, request sucessfull at {x}, content: {r.text}"
		'''
        '''
		#Note: on  wendesdays, mondays and fridays the Http request must be sent at 10:50, on tuesdays and thursdays must be sent at 10:40 AM
		# Stockout
		if (dayofweek in days): 
			if (x == "10:50"):
				#r = requests.post()
				#print(f"A4 - Stockout, request sucessfull at {x}, content: {r.text}")
				pass
		else:
			if (x == "10:40"):
				#r = requests.post()
				#print(f"A4 - Stockout, request sucessfull at {x}, content: {r.text}")
				pass
				
		#Note: on  wendesdays, mondays and fridays the Http request must be done at 11:10, on tuesdays and thursdays must be sent at 11:00 AM 
		# Report USA - OrdersBookedA4
		if (dayofweek in days and (x == "11:10")): 
			#r = requests.post()
			#print(f"A4 - Stockout, request sucessfull at {x}, content: {r.text}")
			pass
		elif(dayofweek not in days and x == "11:00"):
			#r = requests.post()
			#print(f"A4 - Stockout, request sucessfull at {x}, content: {r.text}")
			pass
		'''
# Montlhy manager to manage reports that must be sent in moth-to-month frequency
def Monthlhy_Manager(y):
	pass

manager = Daily_Manager(currenttime)
print(manager)

# brazilian_time = brazilian.localize(hour)
# print(f'São {hour}:{minute} no Brasil%s')

