'''
School_helper is a voice assistant for problems I face in school..
It has useful commands like Translation, Dictionary, Synonym, Calculations,  Web search and Link Open.
How it works is. I have made another project in arduino called Smart Table. a sensor is attached at the bottom
of my table and it detects my movements and acts as a trigger or a wake word for the voice assistant.

After triggering the assistant you can use commands like:

    Translate <text> <language_to_translate_to> ; for eg: translate this is a pen polish
        Languages avaiable are German, Japanese, English, Polish. 
    Define <Word>; defines <Word>
    Synonym  <Word>; finds synonyms for <Word>
    Calculate  <Mathematical exprecian>
    Search  <text> ; Searches <text> in Google
    Open <link> ; Opens link

'''
J_mode="mouse"
import os
oSlider=29
nSlider=0
import keyboard
#keyboard.press_and_release('shift+w')
import wikipedia as wiki
from PyDictionary import PyDictionary
dictionary=PyDictionary()
import speech_recognition as sr
from translate import Translator as tra
import serial
from pynput.mouse import Button, Controller as C

mouse = C()
from langdetect import detect
import random
import time
import webbrowser
import pyttsx3

# to install all libraries type:
# pip install keyboard wikipedia PyDictionary SpeechRecognition translate serial pynput langdetect pyttsx3
# if you encounter any problems with "lxml" then uninstall it by : pip uninstall lxml 
# and reinstall with: pip install lxml
r= sr.Recognizer()
langs= {'german': 1,
        'english':2,
        'polish':4,
        'japanese':3}
colors={'red':1,
        'green':2,
        'blue':3,
        'purple':4,
        'violet':4,
        'yellow':5,
        'light blue':6}
port = 'COM4'
greetings=['How can I help you?', 'Hello!', 'What Can I Do for you?', 'Here to help.', "Need something?", "May I help you?"]
controller=serial.Serial(port,9600)
seperator=' '
def Gmap( x,  in_min,  in_max, out_min, out_max):
  return int((x - in_min) * (out_max - out_min) / (in_max - in_min ) + out_min)

class Bot:
    def __init__(self,name,lang='english',rate=122): # default lang is 2: female US Enlgish.
        self.name=name
        self.lang=lang
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice',self.voices[langs[lang]].id)
    def listVoices(self):
        for voice in self.voices:
            print("Voice: ")
            print(" - ID: %s" % voice.id)
            print(" - Name: %s" % voice.name)
            print(" - Languages: %s" % voice.languages)
            print(" - Gender: %s" % voice.gender)
            print(" - Age: %s" % voice.age)
    def setDefaultVoice(self):
        self.engine.setProperty('voice',self.voices[langs[self.lang]].id)
    def RecordAudio(self):   # function to record and recognize text from Mic
        self.setDefaultVoice()
        with sr.Microphone() as source:
            
            audio = r.listen(source)
            try:
                voice_data= r.recognize_google(audio)
                voice_data=voice_data.lower()
                cmd=str(voice_data)
                return cmd
            except sr.RequestError:
                self.Speak('Sorry, My Speach Service is down')
            except sr.UnknownValueError:
                self.Speak("Sorry, I did not catch that.")
    def Functions(self,cmd, search=False, toSearch=""):

        try:

            if search and "yes" in cmd:
                return self.google(toSearch=toSearch)
            elif search and "no" in cmd:
                return "Okay"

            elif cmd.startswith("translate"):        # say " Translate <sentence to translate> <language to translate to>"
                toTranslate=cmd.split("translate ",1)[1]
                toLang=cmd.split()[-1]
                toTranslate=seperator.join((toTranslate.split(" ")[:-1]))
                froLang=detect(toTranslate)
                print(froLang)
                translator= tra(to_lang=toLang, from_lang=froLang)
                self.engine.setProperty('voice',self.voices[langs[toLang]].id)
                translation = translator.translate(str(toTranslate))
                print(toTranslate, 'in', toLang, ':', translation)
                return translation

            elif cmd.startswith("search"): # say "search <title to search>"

                toGoogle=cmd.split("search",1)[1]
                return self.google(toSearch=toGoogle)

            elif cmd.startswith("open"): # say "Open <link to open>"
                self.setDefaultVoice()
                toOpen=cmd.split("open",1)[1]
                toOpen=toOpen.replace(' ','')
                url='http://'+toOpen
                webbrowser.get().open(url)
                return "Opened " + toOpen

            elif cmd.startswith('synonym'):  # say "Synonym <word to find synonyms for>"
                toSynonym=cmd.split("synonym",1)[1]
                Synonym=str(dictionary.synonym(toSynonym))
                return Synonym
            elif cmd.startswith('define'): # say "define <word to define>"
                toDefine=cmd.split("define",1)[1]
                define=str(dictionary.meaning(toDefine))
                return define

            elif cmd.startswith('calculate'): # say "calculate <mathermatical expression>"
                toCalc=cmd.split("calculate",1)[1]
                return str(eval(toCalc)) + '.'
            elif cmd.startswith('close tab'):
                #toDo=cmd.split("command",1)[1]
                #if toDo== "close tab":

                keyboard.press_and_release('ctrl+w')
                return "Closed Current Tab"
            
            elif cmd.startswith('color') or cmd.startswith('colour'):
                toColor = cmd.split('color ',1)[1]
                print(colors[toColor])
                controller.write((str(colors[toColor])).encode())
                return "Changed Color to " + str(toColor)
            
            elif cmd.startswith('repeat'):
                toRepeat = cmd.split('repeat ',1)[1]
                return toRepeat

            elif cmd.startswith('exit'): # say "exit"
                exit()

            else:
                self.Speak("Command unavailable. Do you want me to Google " +cmd + "?")
                res=self.RecordAudio()
                return self.Functions(cmd=res, search=True, toSearch=cmd)
        except Exception as e: # you can listen to the exception by changing: return "An Error Occured"  -> return e
            return "An Error occurred"

    def Speak(self,toSay):
        self.engine.say(toSay)
        self.engine.runAndWait()
        self.engine.stop()
    def google(self, toSearch):
        self.setDefaultVoice()
        url='http://google.com/search?q='+toSearch
        webbrowser.get().open(url)
        return "Search results for " + toSearch
bot=Bot("Name")   #initialising <bot> object    #give any name you want.
bot.Speak("Connected to Smart Table v2")
while True:
    controller.write(('0').encode())
    wake=str(controller.readline())  # Reading data from SmartTable and storing into <wake> (str)
    wake=wake.replace('\\r\\n','').replace('\'','').replace('b','') # Removing unnecessary characters from <wake>
    print(wake)
    if wake=='w': #checking is the sensor reads true.
        bot.Speak(random.choice(greetings))
        voice_data=bot.RecordAudio()
        print("You said:",voice_data)
        bot.Speak(bot.Functions(voice_data))
    else:
        wake=wake.split(':')
        y=int(wake[0])
        x=-int(wake[1])
        nSlider=Gmap(int(wake[2]),1,27,0,10)
        mouse.move(x*10,y*10)
        print(x,y,nSlider,sep=":")
        
        
    
    