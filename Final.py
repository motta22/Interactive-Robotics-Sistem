import speech_recognition as sr
from gtts import gTTS
from datetime import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests
from pydub import AudioSegment
from pydub.playback import play
from num2words import num2words
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from configparser import ConfigParser

With_gif = 300
heigth_gif = 300
num=0
######################################LIGAÇÂO AO API DE TEMPO#######################################
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

######################################## Speech Recognition ##########################################
start_ms = 0  # start of clip in milliseconds
end_ms = 10000  # end of clip in milliseconds
# palavras chave para activar certas funções
palavras = ["Horas", "Meteorologia"]
informa = (
    "Opções \n"
    "{words}\n"
    "Escolhe uma opção\n"
).format(words=', '.join(palavras))
PROMPT_LIMIT = 5  # Tentativas para entender a pessoa
recognizer = sr.Recognizer()
microphone = sr.Microphone()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
###################################################################### Funções ##############################################################################


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(
            audio, language='pt-PT')
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

# FUNÇÂO DO CLOCK


def tick():
    time2 = time.strftime('%H:%M:%S')
    clock.config(text=time2)
    clock.after(200, tick)

# FUNÇÂO DE REQUEST DA METEOROLOGIA


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

# FUNÇÂO QUE ALETRA OS PARAMETROS PARA MOSTRAR


def Mostrar():
    pesquisa = Tempo('Coimbra')
    if pesquisa:
        local_lbl['text'] = '{}, {}'.format(pesquisa[0], pesquisa[1])
        temp_lbl['text'] = '{:.2f}ºC'.format(pesquisa[2])
        tempo_lbl['text'] = pesquisa[4]
    else:
        messagebox.showerror('Error')

# FUNÇÂO UPDATE DO GIF


def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    panel.configure(image=frame)
    app.after(100, update, ind)

# FUNÇÂO SAIR


def close_window():
    app.destroy()

def speak():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    horas = int(current_time[0:2])
    minutos = int(current_time[3:5])

    if horas >= 6 and horas < 12:
        text = "Bom dia"
    elif horas >= 12 and horas < 20:
        text = "Boa tarde"
    elif (horas >= 20 and horas < 24) or (horas >= 00 and horas < 6):
        text = "Boa noite"

    audio = gTTS(text=text, lang='pt-pt')
    audio.save("message.mp3")
    audiofile = "message.mp3"  # path to audiofile
    sound = AudioSegment.from_file(audiofile, format="mp3")
    splice = sound[start_ms:end_ms]
    play(splice)
    time.sleep(1)

    audio = gTTS(text='Está tudo bem contigo?', lang='pt-pt')
    audio.save("message.mp3")

    audiofile = "message.mp3"  # path to audiofile

    sound = AudioSegment.from_file(audiofile, format="mp3")
    splice = sound[start_ms:end_ms]
    play(splice)
    time.sleep(1)

    audio = gTTS(text='O que posso fazer por ti?', lang='pt-pt')
    audio.save("message.mp3")
    audiofile = "message.mp3"  # path to audiofile
    sound = AudioSegment.from_file(audiofile, format="mp3")
    splice = sound[start_ms:end_ms]
    play(splice)
    time.sleep(1)
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
    ############################################################### Espera pela resposta ########################################################################
    print(informa)
    time.sleep(1)
    for i in range(PROMPT_LIMIT):
        print('Tentativa {}. Fala!'.format(i+1))
        Escolha = recognize_speech_from_mic(recognizer, microphone)
        if Escolha["transcription"]:
            break
        if not Escolha["success"]:
            break
        Text = "Desculpa mas não percebi, podes voltar a repetir?"
        audio = gTTS(text=text, lang='pt-pt')
        audio.save("message.mp3")
        audiofile = "message.mp3"  # path to audiofile
        sound = AudioSegment.from_file(audiofile, format="mp3")
        splice = sound[start_ms:end_ms]
        play(splice)
        time.sleep(1)
    # Mostra o que entendeu
    print("You said: {}".format(Escolha["transcription"]))

        #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
        ############################################################### Revela a hora atual #########################################################################
    if(Escolha["transcription"].lower() == palavras[0].lower()):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        horas = int(current_time[0:2])
        minutos = int(current_time[3:5])

        print(horas)
        print(minutos)
        if horas == 1:
            text = "É uma hora e " + num2words(minutos, lang='pt') + " minutos"
        elif horas == 2:
            text = "São duas horas e " + num2words(minutos, lang='pt') + " minutos"
        elif horas == 1 and minutos == 1:
            text = "É uma hora e um minuto"
        elif horas == 2 and minutos == 1:
            text = "É duas horas e um minuto"
        else:
            text = "São " + num2words(horas, lang='pt') + " horas e " + num2words(minutos, lang='pt') + " minutos"

        audio = gTTS(text=text, lang='pt-pt')
        audio.save("message.mp3")

        audiofile = "message.mp3"  # path to audiofile

        sound = AudioSegment.from_file(audiofile, format="mp3")
        splice = sound[start_ms:end_ms]
        play(splice)
        time.sleep(1)

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------#
    #################################################### Conselhos sobre o que vestir consoante a temperatura ###################################################
    elif Escolha["transcription"].lower() == palavras[1].lower():

        temperatura_exterior = 20

        if temperatura_exterior >= 17 and temperatura_exterior <= 25:
            text = "Está uma temperatura amena, devias levar um casaco fino"
        elif temperatura_exterior >= 10 and temperatura_exterior < 17:
            text = "Está um pouco de frio, devias levar um casaco"
        elif temperatura_exterior <= 10:
            text = "Está muito frio, leva roupa bem quente!"
        else:
            text = "Hoje está um dia quente, devias levar uma roupa mais fresca"
        audio = gTTS(text=text, lang='pt-pt')
        audio.save("message.mp3")

        audiofile = "message.mp3"  # path to audiofile

        sound = AudioSegment.from_file(audiofile, format="mp3")
        splice = sound[start_ms:end_ms]
        play(splice)
        time.sleep(1)

    else:
        print("Acabou!")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
################################################################# Inicio do programa ########################################################################

# O programa só inicia se for detetada a presença humana
humano = True
if humano == False:
    window1 = Tk(className='Sleep time')
    window1.attributes('-fullscreen', True)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    horas = int(current_time[0:2])
    minutos = int(current_time[3:5])
    print(horas)
    print(minutos)
    horas=18
    minutos=31
    if horas >= 6 and horas < 7:
        text = 'bg/sunrise.jpg'
    elif horas >= 7 and horas < 8:
        text = 'bg/sunrise1.jpg'
    elif (horas >= 8 and horas < 13):
        text = 'bg/morning.jpg'
    elif horas >= 13 and (horas <= 17 and (minutos>=0 and minutos<30)):
        text = 'bg/afternoon.jpg'
    elif (horas == 17 and (minutos>=30 and minutos<59)):
        text = 'bg/sunset1.jpg'
    elif (horas == 18 and (minutos>=0 and minutos<30)):
        text = 'bg/sunset2.jpg'
    elif (horas == 18 and (minutos>=30 and minutos<59)):
        text = 'bg/sunset3.jpg'
    elif (horas >= 19 and horas < 24) or (horas >= 00 and horas < 6):
        text ='bg/dark.jpg'

    imagem = Image.open(text)
    imagem = imagem.resize((1960, 1280), Image.ANTIALIAS)
    filename = ImageTk.PhotoImage(imagem)
    background_label = Label(window1, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # sensor PIR para detetar a pessoa
    window1.mainloop()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
################################################################# Inicio da conversa ########################################################################
elif humano == True:
    window2 = Tk(className='Interaction')
    window2.attributes('-fullscreen', True)
    
    speak()
    print('a')
    window2.mainloop()
    



