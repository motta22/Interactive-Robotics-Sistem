from tkinter import *
import time
import os


#######################################################################################################
#                                       Variables from the screen                                     #
#######################################################################################################

# WIDTH = 1000#1920
# HEIGHT = 562.5#1080

# xc = WIDTH/2
# yc = HEIGHT/2
# center = [xc, yc]



#######################################################################################################
#                               INFO ABOUT AVAILABLE GIF EMOTIONS                                     #
#######################################################################################################

#No. of frames in the GIF's:
#frameCnt = 48   #HAPPY & WINK & CONFUSED & PARTY & SLEEPY
#frameCnt = 24   #HOT & CRY & SAD & HAND
#frameCnt = 25   #MASK
#frameCnt = 60   #BIRTHDAY & THINKING & TONGUE
#frameCnt = 61   #HOME
#frameCnt = 49   #NOTIFICATIONS
#frameCnt = 30   #TALKCOFFEE



#############################################################################
#                            FUNCTION DEFINITION                            #
#############################################################################

def showEmotion(emotion):      #, parent):

    emotionList = ['hot', 'cry', 'sad', 'hands', 'happy', 'wink', 'confused', 
                'party', 'sleepy', 'birthday', 'thinking', 'tongue', 'mask', 'home', 'notification', 'talk']

    if emotion in emotionList:

        if (emotion == 'hot') or (emotion == 'cry') or (emotion == 'sad') or (emotion == 'hands'):
            frameCnt = 24
        elif (emotion == 'happy') or (emotion == 'wink') or (emotion == 'confused') or (emotion == 'party') or (emotion == 'sleepy'):
            frameCnt = 48
        elif (emotion == 'birthday') or (emotion == 'thinking') or (emotion == 'tongue'):
            frameCnt = 60
        elif (emotion == 'mask'):
            frameCnt = 25
        elif (emotion == 'home'):
            frameCnt = 61
        elif (emotion == 'notification'):
            frameCnt = 49
        elif (emotion == 'talk'):
            frameCnt = 30
        
        image = ('gifs\\' + emotion + '.gif')
        frames = [PhotoImage(file=image ,format = 'gif -index %i' %(i)) for i in range(frameCnt)]

        return[frames,frameCnt]
    else:
        #print('ERROR!!! Invalid Emotion')
        exit()



def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    GIF.configure(image=frame)
    tk.after(50, update, ind)



################################################################################
#                            PROGRAM IMPLEMENTACION                            #
################################################################################

tk = Tk()

# PARÂMETROS A CHAMAR NO CÓDIGO PRINCIPAL
emotion = 'happy'        #ATENÇÃO AOS NOMES!!! SE FOR MAL ESCRITO NÃO FAZ NADA

GIF = Label(tk)
GIF.pack()


[frames, frameCnt] = showEmotion(emotion)
tk.after(0, update, 0)
tk.mainloop()



####################################################################
#                            REFERENCES                            #
####################################################################
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://ezgif.com/