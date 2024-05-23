from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import pyperclip as pc
import os
import time


class TextToAudio():

    def __init__(self, user_name, project_name, firefox_path):
        self.__user_name = user_name
        self.__project_name = project_name
        self.__firefox_path = firefox_path

    def run(self, text):
        self.set_balabolka()
        self.text_to_speech(text)

    def set_balabolka(self):
        language_cfg = open("utils/config/cfg_balabolka.txt", "r")
        text = language_cfg.readlines()
        f = open("C:\\Users\\" + self.__user_name + "\\AppData\\Roaming\\Balabolka\\balabolka.cfg", 'w')
        for txt in text:
            f.write(txt)

    def text_to_speech(self, text):
        try:
            os.remove('utils\\media\\audio.wav')
        except:
            pass
        self.set_balabolka()
        app = Application().start(cmd_line=u'C:\\Program Files (x86)\\Balabolka\\balabolka.exe')
        time.sleep(20)

        title = "Salvează Textul ca Filă Audio cu Microsoft Azure Text-To-Speech"
        time.sleep(5)
        send_keys('+^d')
        while True:
            try:
                app.window_(title_re=title)
                break
            except:
                send_keys('+^d')
        pc.copy(text)
        time.sleep(5)
        send_keys('^v')
        time.sleep(5)
        vbapp = app.window_(title_re=title)
        vbapp.Salvează.click()
        while os.path.isfile('utils\\media\\audio.wav') == False:
            pass
        time.sleep(6)
        send_keys('%{F4}')
        time.sleep(4)
        send_keys('%{F4}')