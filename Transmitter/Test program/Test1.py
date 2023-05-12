from vosk import Model, KaldiRecognizer
from datetime import datetime
import RPi.GPIO as GPIO
import tkinter as tk
from threading import Thread
import pyaudio
import time
import os

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP

#cd Downloads/voice_recognition/
#python recognitionFinal.py

MQ2_THRESHOLD = 0.8
LED_PIN = 4
PERIOD = 0.05
active = True

#----------------------------------Smoke Stuff START-------------------------------------------------
#pygame.mixer.init()
#pygame.mixer.music.load("/home/mellowship/Documents/Smoke Sensor Example/LiFiSounds/SmokeAlert.wav")

from adafruit_mcp3xxx.analog_in import AnalogIn
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

#--MCP3008 chip is conected to GPIO Pin 5
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

#--Smoke sensor is connected to channel 0 on the MCP3008 Chip
smokeChannel = AnalogIn(mcp, MCP.P4)
#-----------------------------------Smoke Stuff END--------------------------------------------------

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

model = Model(
    r"/home/mellowship/Downloads/voice_recognition/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 44100)

mic = pyaudio.PyAudio()

listening = False

def get_command():
    listening = True
    
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=8192)
    
    stream.start_stream()
    
    while listening:

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
def send_byte(my_byte):
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(PERIOD)

    for b in [int(x) for x in '{:08b}'.format(my_byte)][::-1]:
        GPIO.output(LED_PIN, GPIO.LOW if b == 0 else GPIO.HIGH)
        time.sleep(PERIOD)

    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(PERIOD)

def condition(response):
    
    string_length = len(response)
    
    print(f"Transmitting command ... \'{response}\'")
    
    #for i in range(0, string_length):
        #send_byte(ord(response[i]))
    #time.sleep(1)
        
    #print("-------------------------------------------------------------------")
    if response == "":
            pass
    elif response == "quit":
        print("Program has been terminated. Goodbye!")
        print("-------------------------------------------------------------------")
        quit()
    elif response[0:5] == "smoke":
        #engine.say("Hello, i'm lie-fi!")
        print("Smoke detected!")
        # engine.runAndWait()
        send_byte(ord("s"))
    elif response[0:11] == "temperature":
        #engine.say("Tempreture is 79°F")
        #print("Tempreture is 79°F 🌡️")
        # engine.runAndWait()
        send_byte(ord("t"))
    elif response[0:8] == "humidity":
        #engine.say("humidity is ")
        #print("humidity is ")
        # engine.runAndWait()
        send_byte(ord("h"))
    elif response[0:8] == "pressure":
        #engine.say("pressure is ")
        #print("pressure is ")
        # engine.runAndWait()
        send_byte(ord("p"))
    elif response[0:4] == "open":
        #engine.say("door is opening")
        #print("door is opening")
        # engine.runAndWait()
        send_byte(ord("o"))
    elif response[0:5] == "close":
        #engine.say("door is closing")
        #print("door is closing")
        # engine.runAndWait()
        send_byte(ord("c"))
    elif response[0:5] == "hello":
        #engine.say("Hello, i'm lie-fi!")
        print("Hello, i'm li-fi!")
        # engine.runAndWait()
    elif response[0:4] == "time":
        now = datetime.now()
        #engine.say('\t[%I:%M:%S %p]')
        print(now.strftime('\t[%I:%M:%S %p]'), "😁")
        # engine.runAndWait()
    elif response[0:5] == "clear":
        #engine.say('\t[%I:%M:%S %p]')
        send_byte(ord("l"))
        cls()
        print("Screen cleared!")
    #print("-------------------------------------------------------------------")
def micReady():
    print("Preparing microphone port...")
    command = get_command()
    print("Mic Ready!")
    print("-------------------------------------------------------------------")
def voiceCommand():
    while True:
        command = get_command()
        
        if (command == "hey mellow"):
            print("How can I help?")
            command = get_command()
            condition(command)
            print(f"command sent: \'{command}\'")
            print("-------------------------------------------------------------------")
        else:
            pass
def keyboardCommand():
    command = varEntry.get()
    condition(command)
    print(f"command sent: \'{command}\'")
    print("-------------------------------------------------------------------")
def continuosUpdateSmokeSensorValue():
    while True:
        smokeSensorValue.set(str(round(smokeChannel.voltage, 4)))
        time.sleep(0.1)
def sendMQ2Data():
    global MQ2_THRESHOLD
    currentSmokeSensorValue = float(str(smokeChannel.voltage))
    while True:
        if currentSmokeSensorValue > MQ2_THRESHOLD:
            send_byte(ord("s"))
        time.sleep(0.1)
def setMQ2Thershold():
    global MQ2_THRESHOLD
    MQ2_THRESHOLD = v1.get()
def hint():
    hint = tk.Tk()
    hint.title("HELP SCREEN")
    hint.geometry("600x250+760+200")
    tk.Label(hint, text = "Valid Commands", fg = "blue", font=("segoe UI", 18)).grid(row=0, column=1)
    tk.Label(hint, text = "hello, clear, time", font=("segoe UI", 16)).grid(row=1, column=1)
    tk.Label(hint, text = "-------->", font=("segoe UI", 16)).grid(row=1, column=2)
    tk.Label(hint, text = "Extra commands", font=("segoe UI", 16)).grid(row=1, column=3)
    tk.Label(hint, text = "Description", fg = "blue", font=("segoe UI", 18)).grid(row=0, column=3)
    tk.Label(hint, text = "Smoke", font=("segoe UI", 16)).grid(row=2, column=1)
    tk.Label(hint, text = "Temperature", font=("segoe UI", 16)).grid(row=3, column=1)
    tk.Label(hint, text = "Humidity", font=("segoe UI", 16)).grid(row=4, column=1)
    tk.Label(hint, text = "Pressure", font=("segoe UI", 16)).grid(row=5, column=1)
    tk.Label(hint, text = "Open", font=("segoe UI", 16)).grid(row=6, column=1)
    tk.Label(hint, text = "Close", font=("segoe UI", 16)).grid(row=7, column=1)
    tk.Label(hint, text = "-------->", font=("segoe UI", 16)).grid(row=2, column=2)
    tk.Label(hint, text = "-------->", font=("segoe UI", 16)).grid(row=3, column=2)
    tk.Label(hint, text = "-------->", font=("segoe UI", 16)).grid(row=4, column=2)
    tk.Label(hint, text = "-------->", font=("segoe UI", 16)).grid(row=5, column=2)
    tk.Label(hint, text = "-------->", font=("segoe UI", 16)).grid(row=6, column=2)
    tk.Label(hint, text = "-------->", font=("segoe UI", 16)).grid(row=7, column=2)
    tk.Label(hint, text = "Trigger Smoke sensor", font=("segoe UI", 16)).grid(row=2, column=3)
    tk.Label(hint, text = "Trigger Temperature sensor", font=("segoe UI", 16)).grid(row=3, column=3)
    tk.Label(hint, text = "Trigger humidity sensor", font=("segoe UI", 16)).grid(row=4, column=3)
    tk.Label(hint, text = "Trigger pressure sensor", font=("segoe UI", 16)).grid(row=5, column=3)
    tk.Label(hint, text = "Open door", font=("segoe UI", 16)).grid(row=6, column=3)
    tk.Label(hint, text = "Close door", font=("segoe UI", 16)).grid(row=7, column=3)
    hint.update()
    
print("-------------------------------------------------------------------")
window = tk.Tk()
window.title("TRANSMITTER")
window.geometry("550x250+200+200")

smokeSensorValue = tk.StringVar()
smokeSensorValue.set("N/A")

varEntry = tk.StringVar()
varEntry.set("")

v1 = tk.DoubleVar()
v1.set(MQ2_THRESHOLD)

#labelRec = tk.Label(window, text = "Voice Recognition").grid(row=0, column=0)
#buttonCapture = tk.Button(window, text = "Capture", command = voiceCommand).grid(row=1, column=0)
labelKeyboard = tk.Label(window, text="Keyboard").grid(row=0, column=1)
userInput = tk.Entry(window, textvariable=varEntry, bd=1, relief="solid").grid(row=1, column=1)
buttonSend = tk.Button(window, text="Send", command=keyboardCommand).grid(row=2, column=1)

labelSmokeSensor = tk.Label(window, text="Smoke Sensor").grid(row=0, column=3)
labelSmokeSensorValue = tk.Label(window, textvariable=smokeSensorValue, fg="green", font=("segoe UI", 25)).grid(row=1, column=3)

labelThershold = tk.Label(window, text="Smoke Thershold").grid(row=0, column=2)
s1 = tk.Scale(window, variable=v1, from_=0, to=2, resolution=0.1, orient="horizontal").grid(row=1, column=2)
buttonSet = tk.Button(window, text="Set", command=setMQ2Thershold).grid(row=2, column=2)

labelThershold = tk.Label(window, text="").grid(row=2, column=3)
labelThershold = tk.Label(window, text="").grid(row=3, column=3)
labelThershold = tk.Label(window, text="").grid(row=4, column=3)
labelThershold = tk.Label(window, text="").grid(row=5, column=3)
labelThershold = tk.Label(window, text="").grid(row=6, column=3)
labelThershold = tk.Label(window, text="Help Window").grid(row=7, column=3)
buttonHint = tk.Button(window, text="Help!", command=hint).grid(row=8, column=3)
    #window.update()
    #window.update_idletasks()
#labelSmokeSensor.pack()
#labelSmokeSensorValue.pack()
#labelVoice.pack()
#labelKeyboard.pack()
#userInput.pack()
#button.pack()

#def sensorLoop():
    #var.set("Not N/A")
    #window.update()
    #window.update_idletasks()
    #time.sleep(1)
    
#sensorLoop()
micReady()
t1 = Thread(target = voiceCommand)
t1.start()
t2 = Thread(target = sendMQ2Data)
t2.start()
t3 = Thread(target = continuosUpdateSmokeSensorValue)
t3.start()
window.mainloop()
#try:
    #while active:
            #voiceCommand()
            #num = random.random()
            #num = round(num, 4)
            #print('Raw ADC Value: ', str(smokeChannel.voltage))
            #print(f"Raw ADC Value: {num}")
            #window.update()
            #var.set(str(round(smokeChannel.voltage, 4)))
            #window.update_idletasks()
        #if(float(str(smokeChannel.voltage)) > MQ2_THRESHOLD):
                        # SMOKE SENSOR ABOVE THRESHOLD
            #send_byte(ord("s"))
            #time.sleep(0.1)
#except KeyboardInterrupt:
    #GPIO.cleanup()
