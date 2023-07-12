#import pyttsx3
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
import speech_recognition as sr

start_ms =0 #start of clip in milliseconds
end_ms =10000 #end of clip in milliseconds
palavras = ["Horas", "Temperatura"] # palavras chave para activar certas funções
informa = (
        "Opções \n"
        "{words}\n"
        "Escolhe uma opção\n"
    ).format(words=', '.join(palavras))
PROMPT_LIMIT=5 # Tentativas para entender a pessoa
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
        response["transcription"] = recognizer.recognize_google(audio, language='pt-PT')
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
################################################################# Inicio do programa ########################################################################
while True:
    #O programa só inicia se for detetada a presença humana
    humano=False
    while humano==False:
        pass # sensor PIR para detetar a pessoa

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
################################################################# Inicio da conversa ########################################################################
    while humano==True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        horas=int(current_time[0:2])
        minutos=int(current_time[3:5])

        if horas>=6 and horas<12:
            text="Bom dia"
        elif horas>=12 and horas<20:
            text="Boa tarde"
        elif (horas>=20 and horas<24) or (horas>=00 and horas<6):
            text="Boa noite"
        
        audio = gTTS(text=text, lang='pt-pt')
        audio.save("message.mp3")
        audiofile ="message.mp3" #path to audiofile
        sound = AudioSegment.from_file(audiofile, format="mp3")
        splice = sound[start_ms:end_ms]
        play(splice)
        time.sleep(1)

        audio = gTTS(text='Está tudo bem contigo?', lang='pt-pt')
        audio.save("message.mp3")

        audiofile ="message.mp3" #path to audiofile


        sound = AudioSegment.from_file(audiofile, format="mp3")
        splice = sound[start_ms:end_ms]
        play(splice)
        time.sleep(1)

        audio = gTTS(text='O que posso fazer por ti?', lang='pt-pt')
        audio.save("message.mp3")
        audiofile ="message.mp3" #path to audiofile
        sound = AudioSegment.from_file(audiofile, format="mp3")
        splice = sound[start_ms:end_ms]
        play(splice)
        time.sleep(1)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
############################################################### Espera pela resposta ########################################################################
        print(informa)
        time.sleep(1)
        for i in range(PROMPT_LIMIT):
            print('Guess {}. Speak!'.format(i+1))
            Escolha = recognize_speech_from_mic(recognizer, microphone)
            if Escolha["transcription"]:
                break
            if not Escolha["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # Mostra o que entendeu
        print("You said: {}".format(Escolha["transcription"]))
        
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
############################################################### Revela a hora atual #########################################################################
        if(Escolha["transcription"].lower() == palavras[1].lower()):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)

            horas=int(current_time[0:2])
            minutos=int(current_time[3:5])

            print(horas)
            print(minutos)
            if horas==1:
                text="É uma hora e " + num2words(minutos,lang='pt') + " minutos"
            elif horas==2:
                text="São duas horas e " + num2words(minutos,lang='pt') + " minutos"
            elif horas==1 and minutos==1:
                text="É uma hora e um minuto"
            elif horas==2 and minutos==1:
                text="É duas horas e um minuto"
            else:
                text="São "+ num2words(horas,lang='pt') + " horas e " + num2words(minutos,lang='pt') + " minutos"

            audio = gTTS(text=text, lang='pt-pt')
            audio.save("message.mp3")

            audiofile ="message.mp3" #path to audiofile

            sound = AudioSegment.from_file(audiofile, format="mp3")
            splice = sound[start_ms:end_ms]
            play(splice)
            time.sleep(1)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#################################################### Conselhos sobre o que vestir consoante a temperatura ###################################################
        elif Escolha["transcription"].lower() == palavras[2].lower():
            
            temperatura_exterior=20

            if temperatura_exterior>=17 and temperatura_exterior<=25:
                text="Está uma temperatura amena, devias levar uma casaco fino"
            elif temperatura_exterior>=10 and temperatura_exterior<17:
                text="Está um pouco de frio, devias levar um casaco"
            elif temperatura_exterior<=10:
                text="Está muito frio, leva roupa bem quente!"
            else:
                text="Hoje está um dia quente, devias levar uma roupa mais fresca"
            audio = gTTS(text=text, lang='pt-pt')
            audio.save("message.mp3")

            audiofile ="message.mp3" #path to audiofile

            sound = AudioSegment.from_file(audiofile, format="mp3")
            splice = sound[start_ms:end_ms]
            play(splice)
            time.sleep(1)
