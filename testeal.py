from datetime import datetime as dt
import pandas as pd
import requests
from requests import Timeout
import time
import smtplib,ssl

# desired e-mail to send data
sender_email = "videopineaplle16@gmail.com"

# receiver
receiver_email = "andre.l.souza@tigre.com"
# password, store passwords at source code is dangerous, better input it or store it at a safe place
password = input("Testing passwords: ")

# Messages that will be sent

# Initializing
flowsenter = """\
Assunto: Incialização

FLows estão sendo enviados pelo orquestrador."""

#Error
error = """\
Assunto: Erro no envio de emails

Erros no envio de emails, checar o código e confirmar no Power Automate o envio destes."""

# Success
success = """\
Assunto: Sucesso no envio de emails

Fluxos do Power Automate estão sendo processados."""


# Reading excel file
orch = pd.read_excel("myfile.xls", engine= "openpyxl")
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

# Email sender,in order to notify the developer about the fuction status
smtp_server = "smtp.gmail.com" # 
port = 587 # for gmail service is 587, vary by each e-mail service
context = ssl.create_default_context()# creating secure SSL context
try:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo() # printing server status, expected: None
    server.starttls(context=context) # starting secure connection based on create_deafult_context()
    server.ehlo() # printing server status, expected: Ok
    server.login(sender_email,password) # authenticating on server in order to send the emails requested
        
except Exception as erro:
    print(f"Error: {erro}") # errors might happen, pay attention to status codes and their description
    
finally:
    server.quit() # quiting server after email sending

## Function Trigger
def trigger(name):
    url = eventurl.loc[eventurl.Nome == name,'Url'].values[0]
    try:
        request = requests.post(url) # Http request sender

    except Timeout:
        print(f"Http Request unsucessfull on {actualday} at {currenttime}, content: {request.json}") # returning failure http requests
        server.sendmail(sender_email,receiver_email,error)
    else:
        print(f"Http Request sucessfull on {actualday} at {currenttime}, content: {request.json}") # returning sucess http requests
        server.sendmail(sender_email,receiver_email,success)
# scheduler manager, given some time and day of the week, it manages each execution of it
def Manager(name,hora,days):
    if actualday in days and hora == actualday:
        print(f"Flow {name} being executed on {actualday} at {hr}")
        trigger(name)
    else:
        print(f"Flow {name} must not be excuted now")

if __name__ == '__main__':
    server.sendmail(sender_email,receiver_email,flowsenter)
    for colname in name.index:
        evento, hr,day  = name["Nome"][colname], hrs["Hora"][colname], days["Dia"][colname]
        Manager(evento,hr,days)