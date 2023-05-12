from vosk import Model, KaldiRecognizer
from datetime import datetime
import tkinter as tk
import pyaudio
import os
#import RPi.GPIO as GPIO

model = Model(
    r"G:\Files\Projects\Projects\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 44100)

mic = pyaudio.PyAudio()

listening = False


def get_command():
    listening = True

    stream = mic.open(format=pyaudio.paInt16, channels=1,
                      rate=44100, input=True, frames_per_buffer=8192)
    stream.start_stream()

    while listening:
        stream.start_stream()

        try:
            data = stream.read(4096, exception_on_overflow=False)

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                response = result[14:-3]
                listening = False
                stream.close()
                return response

        except OSError:
            pass

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
cls()

def condition(response):
    print("-------------------------------------------------------------------")
    if response == "":
            pass
    elif response == "quit":
        print("Program has been terminated. Goodbye!")
        print("-------------------------------------------------------------------")
        quit()
    elif response == "hello":
        #engine.say("Hello, i'm lie-fi!")
        print("Hello, i'm li-fi!")
        # engine.runAndWait()
    elif response == "temperature":
        #engine.say("Tempreture is 79°F")
        print("Tempreture is 79°F 🌡️")
        # engine.runAndWait()
    elif response == "time":
        now = datetime.now()
        #engine.say('\t[%I:%M:%S %p]')
        print(now.strftime('\t[%I:%M:%S %p]'), "🕑")
        # engine.runAndWait()
    print("-------------------------------------------------------------------")

def voiceCommand():
    command = get_command()
    print("User said:")
    print(command)
    condition(command)

def keyboardCommand():
    command = userInput.get()
    print("User sent:")
    print(command)
    condition(command)
    
print("-------------------------------------------------------------------")
window = tk.Tk()
window.title("Li-Fi")
window.geometry("200x120")

labelVoice = tk.Button(window, text = "Voice", command = voiceCommand)

labelKeyboard = tk.Label(window, text = "Keyboard")
userInput = tk.Entry(window)

button = tk.Button(window, text = "Send", command = keyboardCommand)

labelVoice.pack()
labelKeyboard.pack()
userInput.pack()
button.pack()

window.mainloop()