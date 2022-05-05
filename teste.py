from datetime import datetime
from threading import Timer
# idéias:
# encapsular essa função, para coordenar os fluxos, tendo como parametros o dia da semana, hora e minuto
# para descobirir o dia da semana, preciso fazer o cálculo de que dia do mes é este durante a semana 
# (usando x.weekday, podemos comparar em um dicionário o dia da semana requisitado em um dicionário)
week_days = {0:"Monday",1:"Tuesday",2:"Wendesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}

x=datetime.today()
y=x.replace(day=x.day, hour=10, minute=51, second=0, microsecond=0)
delta_t=y-x
print(y.day)
secs=delta_t.seconds+1


def organizador(hora,minuto):
    x=datetime.today() # obtém os dados referentes ao dia atual
    y=x.replace(day=x.day, hour=hora, minute=minuto) # insere detalhes em relação ao dia, hora e minutos 
    delta_t=y-x #

    

    secs=delta_t.seconds+1
    return secs 


# encapsular função de disparador do fluxo
def hello_world():
    return "hello world"
    #...
# chamada do disparador
t = Timer(secs, hello_world)
t.start()