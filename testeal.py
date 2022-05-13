from datetime import datetime as dt
from re import I
import pandas as pd
import requests
from requests import Timeout
import time

# Reading excel file
orch = pd.read_excel("myfile.xls", engine= "openpyxl")
#print(orch)
# Getting index and name of the event
name = pd.DataFrame(orch,columns = ['Nome'])

# getting name and url to handle event 
eventurl = pd.DataFrame(orch, columns=['Nome','Url'])

# getting hour of event
hrs = pd.DataFrame(orch,columns=['Nome','Hora'])

# getting day of event
days = pd.DataFrame(orch,columns=['Nome','Dia'])

# Getting hour of the day, flows must be triggred at 6:50 (UTC - 3) Brasília Hour
currenttime = time.strftime("%H:%M") # actual hour, must sum +3, due to instance being from UK

# getting actual day of the week  
actualday = dt.today().strftime('%A') # getting actual day of the week

## Function Trigger
def trigger(name):
    url = eventurl.loc[eventurl.Nome == name,'Url'].values[0]
    try:
        request = requests.post(url) # Http request sender

    except Timeout:
        print(f"Http Request unsucessfull on {actualday} at {currenttime}, content: {request.json}") # returning failure http requests
    else:
        print(f"Http Request sucessfull on {actualday} at {currenttime}, content: {request.json}") # returning sucess http requests

def Manager(name,hora,days):
    if actualday in days and hora == actualday:
        print(f"Flow {name} being executed on {actualday} at {hr}")
        trigger(name)
    else:
        print(f"Flow {name} must not be excuted now")

if __name__ == '__main__':
    for colname in name.index:
        evento, hr,day  = name["Nome"][colname], hrs["Hora"][colname], days["Dia"][colname]
        print(f"Evento: {evento}, Hora: {hr}, Dia: {day}")
        Manager(evento,hr,days)