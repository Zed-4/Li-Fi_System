from vosk import Model, KaldiRecognizer
from threading import Thread
import pyaudio

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
                command = result[14:-3]
                listening = False
                stream.close()
                return command

        except OSError:
            pass


def options(command):
    print(f"command was: {command}")

    # quit = "close the interface"
    # smoke = "trigger smoke sensor"
    # temperature = "what is the temperature"
    # humidity = "what is the humidity"
    # pressure = "what is the pressure"
    # doorOpen = "open the door"
    # doorClose = "close the door"
    # hello = "hello"
    # readTime = "what time is it"
    # clear = "clear the console"
    # ringOn = "turn the light on"
    # ringOff = "turn the light off"
    # ringWhite = "turn the light white"
    # ringRed = "turn the light red"
    # ringGreen = "turn the light green"
    # ringBlue = "turn the light blue"
    # ringLow = "turn the light intensity low"
    # ringMedium = "turn the light intensity medium"
    # ringHigh = "turn the light intensity high"

    closeProgram = "quit"
    smoke = "smoke"
    temperature = "temperature"
    humidity = "humidity"
    pressure = "pressure"
    doorOpen = "open"
    doorClose = "close"
    hello = "hello"
    readTime = "time"
    clear = "clear"
    ringOn = "light on"
    ringOff = "light off"
    ringWhite = "light color white"
    ringRed = "light color red"
    ringGreen = "light color green"
    ringBlue = "light color blue"
    ringLow = "intensity low"
    ringMedium = "intensity medium"
    ringHigh = "intensity hi"

    if command == "":
        pass
    elif closeProgram in command:
        print("Program has been terminated. Goodbye!")
        print("-------------------------------------------------------------------")
        quit()
    elif smoke in command:
        print("Smoke detected!")
    elif temperature in command:
        print("temperature detected!")
    elif humidity in command:
        print("humidity detected!")
    elif pressure in command:
        print("pressure detected!")
    elif doorOpen in command:
        print("doorOpen detected!")
    elif doorClose in command:
        print("doorClose detected!")
    elif hello in command:
        print("hello detected!")
    elif readTime in command:
        print("readTime detected!")
    elif clear in command:
        print("Screen cleared!")
    elif ringOn in command:
        print("ringOn detected!")
    elif ringOff in command:
        print("ringOff detected!")
    elif ringWhite in command:
        print("ringWhite detected!")
    elif ringRed in command:
        print("ringRed detected!")
    elif ringGreen in command:
        print("ringGreen detected!")
    elif ringBlue in command:
        print("ringBlue detected!")
    elif ringLow in command:
        print("ringLow detected!")
    elif ringMedium in command:
        print("ringMedium detected!")
    elif ringHigh in command:
        print("ringHigh detected!")
    else:
        print("Command Invalid")


def voiceInput():
    while True:
        command = get_command()
        options(command)


t1 = Thread(target=voiceInput)
t1.start()
