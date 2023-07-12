import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import time
import os
from configparser import ConfigParser
from datetime import datetime
import requests

######################################LIGAÇÂO AO API DE TEMPO#######################################
url = 'api.openweathermap.org/data/2.5/forecast/daily?q={}&units=metric&cnt=7&appid={}'
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

#######################################FUNÇÂO DE REQUEST DA METEOROLOGIA##########################
def Tempo(cidade):
    resultado = requests.get(url.format(cidade, api_key))
    if resultado:
        json = resultado.json()
        # Cidade, Pais, Temperatura, icon, tempo
        cidade = json['city']['name']
        pais = json['location']['country']
        Lista_Dia = json['forecast']['time']['day']
        print(Lista_Dia)
        Lista_Temp = json['forecast']['temperature']['day']
        final = (cidade,pais,Lista_Dia,Lista_Temp)
        return final
    else:
        messagebox.showerror('Error')
        return None


###################################FUNÇÂO QUE ALETRA OS PARAMETROS PARA MOSTRAR#########################
def Mostrar():
    pesquisa = Tempo('Ovar')
    if pesquisa:
        local_lbl['text'] = '{}, {}'.format(pesquisa[0],pesquisa[1])
        dia_lbl['text'] = '{:.2f}ºC'.format(pesquisa[2])
        tempo_lbl['text'] = pesquisa[4]
    else:
        messagebox.showerror('Error')



#########################################"MAIN"###################################################################
app = Tk(className='APP NAME' )
###################################### set fullscreen
app.attributes('-fullscreen', True)
####################################set window color
app.configure(bg='#33495f')

local_lbl = Label(app, text='Local', font=('bold',20), fg='white', bg='#33495f')
local_lbl.pack()

dia_lbl = Label(app, text='Dia', fg='white', bg='#33495f')
dia_lbl.pack()

tempo_lbl = Label(app, text='Tempo', fg='white', bg='#33495f')
tempo_lbl.pack()
Mostrar()
app.mainloop()