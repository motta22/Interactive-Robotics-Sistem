import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import time
import datetime as dt
import os
from configparser import ConfigParser
from datetime import datetime
import requests
from tkcalendar import Calendar, DateEntry
import ctypes

change = False
change2 = True
conta = 0
up = ""
up2 = ""
contaTemperatura=0
contaCalendario=0
contaMusica=0
# text2=""

######################################LIGAÇÂO AO API DE TEMPO#######################################
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


#####################################FUNÇÂO DO CLOCK#################################################
def tick():  # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    clock.config(text=time2)
    # text=leficheiro()
    clock.after(200, tick)
    # print("tick")
    return (text)


#######################################FUNÇÂO DE REQUEST DA METEOROLOGIA##########################
def Tempo(cidade):
    resultado = requests.get(url.format(cidade, api_key))
    if resultado:
        json = resultado.json()
        # Cidade, Pais, Temperatura, icon, tempo
        cidade = json['name']
        pais = json['sys']['country']
        temp_Kelvin = json['main']['temp']
        temp_Celsius = temp_Kelvin - 273.15
        icon = json['weather'][0]['icon']
        tempo = json['weather'][0]['main']
        final = (cidade, pais, temp_Celsius, icon, tempo)
        return final
    else:
        messagebox.showerror('Error')
        return None


###################################FUNÇÂO QUE ALETRA OS PARAMETROS PARA MOSTRAR#########################
def Mostrar():
    pesquisa = Tempo('Coimbra')
    if pesquisa:
        local_lbl['text'] = '{}, {}'.format(pesquisa[0], pesquisa[1])
        temp_lbl['text'] = '{:.2f}ºC'.format(pesquisa[2])
        tempo_lbl['text'] = pesquisa[4]
    else:
        messagebox.showerror('Error')


#####################################FUNÇÂO UPDATE DO GIF#####################################################
def update(ind, frames, frameCnt):
    global conta, change, up, contaTemperatura, contaCalendario, contaMusica

    # print(frame)
    text2 = leficheiro()
    if text2 == "False\n" and conta == 1:
        conta = 0
        change = False
        contaTemperatura=0
        contaCalendario=0
        MudarSI()
    if contaTemperatura == 0 and text2 == "Temperatura\n":
        MudarCI()
    if contaCalendario == 0 and text2 == "Calendario\n":
        MudarCI()
    if contaMusica == 0 and text2 == "Musica\n":
        MudarCI()
    if contaTemperatura == 1:
        frame = frames[ind]
        ind += 1
        # print(up)
        if ind == frameCnt:
            ind = 0
        panel.configure(image=frame)

    app.after_cancel(up)
    app.after(100, update, ind, frames, frameCnt)
    app.after_cancel(up)

def update2(ind, frames, frameCnt):
    global up2
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    panel2.configure(image=frame)
    app.after_cancel(up2)
    app.after(50, update2, ind, frames, frameCnt)
    app.after_cancel(up2)

#################################FUNÇÂO SAIR##################################################################
def close_window():
    app.destroy()  # destroying the main window


def DefenirImagemBack():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    horas = int(current_time[0:2])
    minutos = int(current_time[3:5])
    if horas >= 6 and horas < 7:
        texto = 'bg/sunrise.jpg'
    elif horas >= 7 and horas < 8:
        texto = 'bg/sunrise1.jpg'
    elif (horas >= 8 and horas < 13):
        texto = 'bg/morning.jpg'
    elif horas >= 13 and (horas < 17 and ((minutos >= 0 and minutos < 30) or (minutos >= 30 and minutos <= 59))):
        texto = 'bg/afternoon.jpg'
    elif (horas == 17 and (((minutos >= 0 and minutos < 30) or (minutos >= 30 and minutos <= 59)))):
        texto = 'bg/sunset1.jpg'
    elif (horas == 18 and (minutos >= 0 and minutos < 30)):
        texto = 'bg/sunset2.jpg'
    elif (horas == 18 and (minutos >= 30 and minutos < 59)):
        texto = 'bg/sunset3.jpg'
    elif (horas >= 19 and horas < 24) or (horas >= 00 and horas < 6):
        texto = 'bg/dark.jpg'
#####################SO PARA WINDOWS######################
    ctypes.windll.user32.SystemParametersInfoW(20, 0,"D:/Faculdade/4ºano/1ºsemestre/Sistemas e Robos Interativos/Projeto/Projeto Python/"+texto,0)
##########################################################
    return texto


def leficheiro():
    # global text2
    f = open('comunica.txt', 'r')
    text = f.read()
    f.close()
    app.after(100, leficheiro)
    #print(text)
    return (text)


def MudarCI():
    #print("oi")
    global change, up, contaTemperatura, contaCalendario, contaMusica
    change = True
    text=leficheiro()
    background_label['image'] = ''
    background_label['bg'] = '#33495f'
    panel2.place_forget()
    if text == "Temperatura\n" and contaTemperatura == 0:
        cal.pack_forget()
        print("oi")
        pesquisa = Tempo("Coimbra")
        local_lbl['text'] = '{}, {}'.format(pesquisa[0], pesquisa[1])
        local_lbl['bg'] = '#33495f'
        temp_lbl['text'] = '{:.2f}ºC'.format(pesquisa[2])
        temp_lbl['bg'] = '#33495f'
        tempo_lbl['text'] = pesquisa[4]
        tempo_lbl['bg'] = '#33495f'
        clock['bg'] = '#33495f'
        local_lbl.pack()
        tempo_lbl.pack()
        temp_lbl.pack()
        pesquisa = Tempo('Coimbra')
        if pesquisa[3] == '01n':
            frameCnt = 1
            frames = [PhotoImage(file='Gifs/moon.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]
            img = ImageTk.PhotoImage(Image.open('Gifs/moon.gif'), format="gif -index 2")
            panel['image'] = img
            panel.pack()
        else:
            if pesquisa[3] == '01d':
                frameCnt = 1
                frames = [PhotoImage(file='Gifs/clear_sky.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]
                img = ImageTk.PhotoImage(Image.open('Gifs/clear_sky.gif'), format="gif -index 2")
                panel['image'] = img
                panel.pack()
            else:
                if pesquisa[3] == '02d':
                    frameCnt = 24
                    frames = [PhotoImage(file='Gifs/few_clouds.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]
                    img = ImageTk.PhotoImage(Image.open('Gifs/few_clouds.gif'), format="gif -index 2")
                    panel['image'] = img
                    panel.pack()
                else:
                    if pesquisa[3] == '02n':
                        frameCnt = 24
                        frames = [PhotoImage(file='Gifs/night_few_clouds.gif', format='gif -index %i' % (i)) for i in
                                  range(frameCnt)]
                        img = ImageTk.PhotoImage(Image.open('Gifs/night_few_clouds.gif'), format="gif -index 2")
                        panel['image'] = img
                        panel.pack()
                    else:
                        if pesquisa[3] == '03d' or pesquisa[3] == '03n' or pesquisa[3] == '04d' or pesquisa[3] == '04n' or \
                                pesquisa[3] == '50d' or pesquisa[3] == '50n':
                            frameCnt = 19
                            frames = [PhotoImage(file='Gifs/broken_clouds.gif', format='gif -index %i' % (i)) for i in
                                      range(frameCnt)]
                            img = ImageTk.PhotoImage(Image.open('Gifs/broken_clouds.gif'), format="gif -index 2")
                            panel['image'] = img
                            panel.pack()
                        else:
                            if pesquisa[3] == '09d' or pesquisa[3] == '09n':
                                frameCnt = 22
                                frames = [PhotoImage(file='Gifs/shower_rain.gif', format='gif -index %i' % (i)) for i in
                                          range(frameCnt)]
                                img = ImageTk.PhotoImage(Image.open('Gifs/shower_rain.gif'), format="gif -index 2")
                                panel['image'] = img
                                panel.pack()
                            else:
                                if pesquisa[3] == '10d' or pesquisa[3] == '10n':
                                    frameCnt = 19
                                    frames = [PhotoImage(file='Gifs/rain.gif', format='gif -index %i' % (i)) for i in
                                              range(frameCnt)]
                                    img = ImageTk.PhotoImage(Image.open('Gifs/rain.gif'), format="gif -index 2")
                                    panel['image'] = img
                                    panel.pack()
                                else:
                                    if pesquisa[3] == '11d' or pesquisa[3] == '11n':
                                        frameCnt = 17
                                        frames = [PhotoImage(file='Gifs/thunderstorm.gif', format='gif -index %i' % (i)) for
                                                  i in range(frameCnt)]
                                        img = ImageTk.PhotoImage(Image.open('Gifs/thunderstorm.gif'), format="gif -index 2")
                                        panel['image'] = img
                                        panel.pack()
                                    else:
                                        if pesquisa[3] == '13d' or pesquisa[3] == '13n':
                                            frameCnt = 16
                                            frames = [PhotoImage(file='Gifs/snow.gif', format='gif -index %i' % (i)) for i
                                                      in range(frameCnt)]
                                            img = ImageTk.PhotoImage(Image.open('Gifs/snow.gif'), format="gif -index 2")
                                            panel['image'] = img
                                            panel.pack()
        contaTemperatura = 1
        contaCalendario = 0
        contaMusica=0
    elif text == "Calendario\n" and contaCalendario == 0:
        local_lbl.pack_forget()
        tempo_lbl.pack_forget()
        temp_lbl.pack_forget()
        panel.pack_forget()
        cal.pack(fill="both", expand=True)
        contaTemperatura=0
        contaCalendario=1
        contaMusica=0
        frames = ""
        frameCnt = 0

    elif text == "Musica\n" and contaMusica == 0:

        print("entrei na Musica")

        cal.pack_forget()
        local_lbl.pack_forget()
        tempo_lbl.pack_forget()
        temp_lbl.pack_forget()
        panel.pack_forget()

        contaCalendario=0
        contaTemperatura=0
        contaMusica=1
        frames = ""
        frameCnt = 0

    else:
        frames=""
        frameCnt=0
    up = app.after(0, update, 0, frames, frameCnt)
    app.after(1000, MudaPainel)
    #clock.place(x='1810', y='1050')

    # #MudarSI()
    # mudar_btn = Button(app, text='Mudar', bg='white', command=MudarSI, height=1, width=20)
    # mudar_btn.place(x='30', y='1045')


def MudaPainel():
    text2 = leficheiro()
    global conta, up
    if up != "":
        app.after_cancel(up)
    print("Painel")
    # print(conta)
    if (text2 == "False\n" and conta == 1):
        conta = 0
        print("Entrou SI")
        MudarSI()
        # app.after(100,MudaPainel)
    elif text2 == "False\n":
        MudarSI()
        # app.after(100,MudaPainel)
    elif text2 == "True\n" and conta == 0:
        conta = 1
        print("Entrou CI")
        MudarCI()
    # app.after(100,MudaPainel)


def MudarSI():
    global change2, change, up2
    background_label['image'] = filename
    local_lbl.pack_forget()
    tempo_lbl.pack_forget()
    cal.pack_forget()
    # tempo_lbl.pack_forget()
    temp_lbl.pack_forget()
    panel.pack_forget()
    clock.place_forget()
    frameCnt = 48
    frames = [PhotoImage(file='Gifs/sleepy2.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]
    img = ImageTk.PhotoImage(Image.open('Gifs/sleepy2.gif'), format="gif -index 2")
    panel2['image'] = img
    panel2.place(x='0', y='780')
    #print("oi")
    text = leficheiro()
    if (text == "True\n"):
        MudarCI()
    # print(text)
    if (change == False):
        # print(text)
        # app.after(1000,MudarSI)
        app.after(1000, MudaPainel)
    # MudarSI()
    up2 = app.after(0, update2, 0, frames, frameCnt)
    return (text)


#########################################"MAIN"###################################################################
app = Tk(className='APP NAME')
app.attributes('-fullscreen', True)
app.wm_attributes('-transparentcolor', 'grey')

Humano = leficheiro()
print("Main")

text = DefenirImagemBack()
imagem = Image.open(text)
imagem = imagem.resize((1960, 1280), Image.ANTIALIAS)
filename = ImageTk.PhotoImage(imagem)
background_label = Label(app, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
local_lbl = Label(app, text='', font=('bold', 20), fg='white')

today = dt.date.today()
mindate = dt.date(year=2020, month=11, day=29)
maxdate = today + dt.timedelta(days=5)
# cal = Calendar(app, font="Arial 14", selectmode='day',
#  mindate=mindate, maxdate=maxdate, disabledforeground='red',
#   cursor="hand1", year=2018, month=2, day=5)

cal = Calendar(app, font="Arial 14", disabledbackground='SlateGray4', disabledforeground='black',
        selectmode='day', year=today.year, month=today.month, day=today.day, state="disabled", 
        selectbackground='SlateGray3', selectforeground='maroon')


clock = Label(app, font=('times', 20, 'bold'), fg='white', bg='black')

temp_lbl = Label(app, text='', fg='white')

tempo_lbl = Label(app, text='', fg='white')

panel = Label(app, image='', bg='#33495f', width='300', height='300')
panel2 = Label(app, image='', width='300', height='300', bg ='grey')
# panel1 = Label(app, image='', bg='#33495f', width='400', height='400')
# frameCnt = 19
# frames = [PhotoImage(file='Gifs/rain.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]
# img = ImageTk.PhotoImage(Image.open('Gifs/rain.gif'), format="gif -index 2")
# panel1['image'] = img
# panel1.pack()
# panel1.after(0,update,0,frames,frameCnt)
# mudar_btn = Button(app, text='Mudar', bg='white', command=MudarCI, height=1, width=20)
# mudar_btn.place(x='30', y='1045')
if (Humano == "True\n"):
    MudarCI()
elif Humano == "False\n":
    MudarSI()

tick()
app.after(1000)
app.mainloop()




