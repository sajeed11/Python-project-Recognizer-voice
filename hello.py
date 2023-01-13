from tkinter import *
from vosk import Model,KaldiRecognizer
import pyaudio
import pyttsx3
import json
import os
from playsound import playsound
import msvcrt as m
import smtplib
import sys



def main():
    root= Tk()
    gui = Window(root)
    gui.root.mainloop()
    return None

def send_email():
    root1 = Tk()
    gui1 = Window1(root1)
    gui1.root1.mainloop()
    return None

class Window1:
    def __init__(self,root1):
        self.root1 = root1
        self.root1.title('Tkinter Sens Email')
        self.textspace = Text(self.root1)
        self.textspace.grid(row=0,column=0)
        #Button to send the email
        Button(self.root1, text="Send",command=self.send).grid(row=0,column=1)
    def send(self):
        sendgui = Tk()
        sendgui.geometry('560x100')
        filecontents1 = self.textspace.get(0.0,END)
        def send():
            server = smtplib.SMTP(host="smtp.gmail.com",port=587)
            server.ehlo()
            server.starttls()
            server.login(user= sender.get(),password= password.get())#Password for my email using gmail:'dwijofnksmygvwwf'
            server.sendmail(from_addr=sender.get(),to_addrs= receiver.get(),msg= filecontents1)
            sendgui.destroy()
            return None
        labeltest1 =  Label(sendgui, text="Sender")
        labeltest1.grid(row=0,column=0)
        sender = Entry(sendgui, width=70)
        sender.grid(row=0,column=1)
        labeltest2 =  Label(sendgui, text="Password")
        labeltest2.grid(row=1,column=0)
        password = Entry(sendgui, width=40)
        password.grid(row=1,column=1)
        labeltest3 =  Label(sendgui, text="Receiver")
        labeltest3.grid(row=2,column=0)
        receiver = Entry(sendgui, width=70)
        receiver.grid(row=2,column=1) 
        Button(sendgui, text="Send", command= send).grid(row=3, column=2)
        return None
    pass

class Window:
    def __init__(self,root):
        self.root=root
        self.root.title('Tkinter notepad')
        #Create Text field
        self.textspace = Text(self.root)
        self.textspace.grid(row=0,column=0)
        #Create open and save file
        Button(self.root, text="Save",command=self.savefile).grid(row=0,column=1)    
    def savefile(self):
        savegui = Tk()
        savegui.geometry('560x50')
        filecontents = self.textspace.get(0.0,END)
        def writefile():
            with open(file_name.get() + '.txt', 'w+') as file:
                file.write(filecontents)
                file.close()
                savegui.destroy()
            return None    
        labeltest =  Label(savegui, text="File Name")
        labeltest.grid(row=0,column=0)
        file_name = Entry(savegui, width=40)
        file_name.grid(row=0,column=1)
        Button(savegui, text="Save", command= writefile).grid(row=0, column=2)
        return None
    pass


def wait():
    m.getch()

Sadjed_Assistant=pyttsx3.init()
voice=Sadjed_Assistant.getProperty('voices')
assistant_voice_id='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
Sadjed_Assistant.setProperty('voice',assistant_voice_id)

def speak(audio):
    print('Sadjed_A:' + audio)
    Sadjed_Assistant.say(audio)
    Sadjed_Assistant.runAndWait()

model = Model('assets/vosk-model-en-us-0.22-lgraph')    

rec = KaldiRecognizer(model,16000)
cap=pyaudio.PyAudio()
stream=cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

#The main methode
def startTalking():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data)==0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result= json.loads(result)
            print('Boss:'+ result['text'])
            stream.start_stream()
            if "play music" in result['text']:
                os.system('cls')
                stream.stop_stream()
                print('Boss:'+ result['text'])
                speak('This is some music for you')
                os.startfile('SadBoyProlific - Dead and Cold (Lyrics) - i wish i was dead and cold.mp3')
                speak('Assistant is paused')
                wait()
                speak('What else')
                stream.start_stream()
            elif 'send email' in  result['text']:
                os.system('cls')
                stream.stop_stream()
                speak('I will to send your email')
                send_email()
                print('Mail was sent')
                speak('Your message was sent')
                stream.start_stream()
                print("...")
                print('Listenning')
            elif 'make a note' in result['text']:
                    os.system('cls')
                    stream.stop_stream()
                    speak('Write your note and save it')
                    #wait()
                    main()
                    speak('Your note was saved')
                    stream.start_stream()
                    print("...")
                    print('Listenning')
            elif 'stop' in result['text']:
                    os.system('cls')
                    stream.stop_stream()
                    speak('Assistant is off, Goodbye')
                    sys.exit(123)        
    return None

startTalking()