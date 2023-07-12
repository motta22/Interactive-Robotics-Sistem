# import argparse
# import os
# import time
# import random
# import requests
# import ctypes
# import platform
#
# def set_wallpaper():
#     #Check the operating system
#     system_name = platform.system().lower()
#     path = ''
#     if system_name =='linux':
#         path = os.getcwd()+'/temp.jpg'
#         command = "gsettings set org.gnome.desktop.background picture-uri file:" + path
#         os.system(command)
#     elif system_name == 'windows':
#         path = 'bg/sunrise.jpg'
#         ctypes.windll.user32.SystemParametersInfoW(20,0,path,0)


import ctypes
ctypes.windll.user32.SystemParametersInfoW(20, 0, "D:/Faculdade/4ºano/1ºsemestre/Sistemas e Robos Interativos/Projeto/Projeto Python/bg/sunrise.jpg" , 0)