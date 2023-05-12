from vosk import Model, KaldiRecognizer
from datetime import datetime
from termcolor import colored
import keyboard
import pyaudio
import os
#import RPi.GPIO as GPIO

model = Model(
    r"G:\Files\Projects\Projects\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 44100)

mic = pyaudio.PyAudio()
#engine = pyttsx3.init()

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

print("-------------------------------------------------------------------")
print(colored("Options:", 'green'))
print(colored("\tPress ", 'green'), colored("'esc'", 'yellow'), colored(" to exit program!", 'green'))
print(colored("\tPress  ", 'green'), colored("'-'", 'yellow'), colored("  for voice command", 'green'))
print(colored("\tPress  ", 'green'), colored("'+'", 'yellow'), colored("  for keyboard input", 'green'))
print("-------------------------------------------------------------------")

while True:
    if keyboard.is_pressed('-'):
        print(colored("Mic Ready!", 'green'))
        command = get_command()
        print(colored("You said: ", 'green'), colored(f'{command}', 'white'))

        if command == "":
            pass
        elif command == "hello":
            #engine.say("Hello, i'm lie-fi!")
            print("Hello, i'm li-fi! 👋")
            # engine.runAndWait()
        elif command == "temperature":
            #engine.say("Temperature is 79°F")
            print("Temperature is 79°F")
            # engine.runAndWait()
        elif command == "time":
            now = datetime.now()
            #engine.say('\t[%I:%M:%S %p]')
            print(now.strftime('\t[%I:%M:%S %p]'), "🕑")
            # engine.runAndWait()
        print("-------------------------------------------------------------------")

    if keyboard.is_pressed('+'):
        userInput = input(colored("Type in command: ", 'green'))
        command = userInput

        if command == "":
            pass
        elif command == "hello":
            #engine.say("Hello, i'm lie-fi!")
            print("Hello, i'm li-fi!")
            # engine.runAndWait()
        elif command == "temperature":
            #engine.say("Tempreture is 79°F")
            print("Tempreture is 79°F 🌡️")
            # engine.runAndWait()
        elif command == "time":
            now = datetime.now()
            #engine.say('\t[%I:%M:%S %p]')
            print(now.strftime('\t[%I:%M:%S %p]'), "🕑")
            # engine.runAndWait()
        print("-------------------------------------------------------------------")
    
    if keyboard.is_pressed('esc'):
        print(colored("Goodbye!", 'green'))
        print("-------------------------------------------------------------------")
        quit()