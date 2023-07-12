import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
from time import *
from configparser import ConfigParser
from datetime import datetime
import requests

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

def Tempo(cidade):
    resultado = requests.get(url.format(cidade, api_key))
    if resultado:
        json = resultado.json()
        # Cidade, Pais, Temperatura, icon, tempo, data
        cidade = json['name']
        pais = json['sys']['country']
        temp_Kelvin = json['main']['temp']
        temp_Celsius = temp_Kelvin - 273.15
        icon = json['weather'][0]['icon']
        tempo = json['weather'][0]['main']
        data = json['dt']
        final = (cidade,pais,temp_Celsius,icon,tempo,data)
        return final
    else:
        return None

def Mostrar():
    pesquisa = Tempo('Coimbra')
    if pesquisa:
        local_lbl['text'] = '{}, {}'.format(pesquisa[0],pesquisa[1])
        #icon['image'] = ImageTk.PhotoImage(Image.open('Wheather_icon/{}.png'.format(pesquisa[3])))
        temp_lbl['text'] = '{:.2f}ºC'.format(pesquisa[2])
        tempo_lbl['text'] = pesquisa[4]
        data_lbl['text'] = datetime.utcfromtimestamp(pesquisa[5]).strftime('%d-%m-%Y %H:%M:%S')
    else:
        messagebox.showerror('Error')





app = Tk()
pesquisa=Tempo('Coimbra')
tempo_btn = Button(app, text='Tempo', command=Mostrar)
tempo_btn.pack()

local_lbl = Label(app, text='', font=('bold',20))
local_lbl.pack()

temp_lbl = Label(app, text='')
temp_lbl.pack()


icon = tk.Label(app, image='',bg='black')
icon.pack()


tempo_lbl = Label(app, text='')
tempo_lbl.pack()

data_lbl = Label(app, text='')
data_lbl.pack()



app.mainloop()