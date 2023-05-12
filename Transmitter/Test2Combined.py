from vosk import Model, KaldiRecognizer
from datetime import datetime
import RPi.GPIO as GPIO
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from ttkwidgets import TickScale
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
        window.destroy()
        quit()
    elif response[0:5] == "smoke":
        print("Smoke detected!")
        send_byte(ord("s"))
    elif response[0:11] == "temperature":
        send_byte(ord("t"))
    elif response[0:8] == "humidity":
        send_byte(ord("h"))
    elif response[0:8] == "pressure":
        send_byte(ord("p"))
    elif response[0:4] == "open":
        send_byte(ord("o"))
    elif response[0:5] == "close":
        send_byte(ord("c"))
    elif response[0:5] == "hello":
        print("Hello, i'm li-fi!")
    elif response[0:4] == "time":
        now = datetime.now()
        print(now.strftime('\t[%I:%M:%S %p]'), "😁")
    elif response[0:5] == "clear":
        send_byte(ord("l"))
        cls()
        print("Screen cleared!")
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
    #tab2 = ThemedTk(themebg=True)
    #window.set_theme("black")
    #hint.title("HELP SCREEN")
    #hint.geometry("600x250+760+200")

    ttk.Label(tab2, text = "Valid Commands", foreground = "blue", font=("segoe UI", 18, "bold")).grid(row=0, column=1)
    ttk.Label(tab2, text = "hello, clear, time", font=("segoe UI", 16)).grid(row=1, column=1)
    ttk.Label(tab2, text = "-------------->", font=("segoe UI", 16)).grid(row=1, column=2)
    ttk.Label(tab2, text = "Extra commands", font=("segoe UI", 16)).grid(row=1, column=3)
    ttk.Label(tab2, text = "Description", foreground = "blue", font=("segoe UI", 18, "bold")).grid(row=0, column=3)
    ttk.Label(tab2, text = "Smoke", font=("segoe UI", 16)).grid(row=2, column=1)
    ttk.Label(tab2, text = "Temperature", font=("segoe UI", 16)).grid(row=3, column=1)
    ttk.Label(tab2, text = "Humidity", font=("segoe UI", 16)).grid(row=4, column=1)
    ttk.Label(tab2, text = "Pressure", font=("segoe UI", 16)).grid(row=5, column=1)
    ttk.Label(tab2, text = "Open", font=("segoe UI", 16)).grid(row=6, column=1)
    ttk.Label(tab2, text = "Close", font=("segoe UI", 16)).grid(row=7, column=1)
    ttk.Label(tab2, text = "-------------->", font=("segoe UI", 16)).grid(row=2, column=2, padx= (20,20))
    ttk.Label(tab2, text = "-------------->", font=("segoe UI", 16)).grid(row=3, column=2)
    ttk.Label(tab2, text = "-------------->", font=("segoe UI", 16)).grid(row=4, column=2)
    ttk.Label(tab2, text = "-------------->", font=("segoe UI", 16)).grid(row=5, column=2)
    ttk.Label(tab2, text = "-------------->", font=("segoe UI", 16)).grid(row=6, column=2)
    ttk.Label(tab2, text = "-------------->", font=("segoe UI", 16)).grid(row=7, column=2)
    ttk.Label(tab2, text = "Trigger Smoke sensor", font=("segoe UI", 16)).grid(row=2, column=3)
    ttk.Label(tab2, text = "Report Temperature", font=("segoe UI", 16)).grid(row=3, column=3)
    ttk.Label(tab2, text = "Report humidity", font=("segoe UI", 16)).grid(row=4, column=3)
    ttk.Label(tab2, text = "Report pressure", font=("segoe UI", 16)).grid(row=5, column=3)
    ttk.Label(tab2, text = "Open door", font=("segoe UI", 16)).grid(row=6, column=3)
    ttk.Label(tab2, text = "Close door", font=("segoe UI", 16)).grid(row=7, column=3)
    tab2.update()
    
window = ThemedTk(themebg=True)
window.set_theme("black")
window.title("TRANSMITTER")
tabControl = ttk.Notebook(window)
#window.geometry("600x300+760+200")
window.geometry("1024x600")


tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text ='MAIN SCREEN')
tabControl.add(tab2, text ='HELP SCREEN')
tabControl.pack(expand = 1, fill ="both")

smokeSensorValue = tk.StringVar()
smokeSensorValue.set("N/A")

varEntry = tk.StringVar()
varEntry.set("")

v1 = tk.DoubleVar()
v1.set(MQ2_THRESHOLD)

#labelRec = tk.Label(window, text = "Voice Recognition").grid(row=0, column=0)
#buttonCapture = tk.Button(window, text = "Capture", command = voiceCommand).grid(row=1, column=0)

abelKeyboard = ttk.Label(tab1, text = "Keyboard", font = ("segoe UI", 15)).grid(row=0, column=0)
userInput = ttk.Entry(tab1, textvariable = varEntry, font = ('segoe UI', 15, 'bold')).grid(row=1, column=0)
buttonSend = ttk.Button(tab1, text = "SEND", command = keyboardCommand).grid(row=2, column=0)

labelThershold = ttk.Label(tab1, text = "Smoke Thershold", font = ("segoe UI", 15)).grid(row=0, column=1)
#s1 = ttk.Scale(tab1, variable = v1, from_ = 0, to = 2, orient = "horizontal").grid(row=1, column=2)
s1 = TickScale(tab1,variable = v1, orient='horizontal', from_=0, to=1.5, tickinterval=0.5, resolution=0.1, length=250).grid(row=1, column=1)
v1.set(0.8)
buttonSet = ttk.Button(tab1, text = "SET", command = setMQ2Thershold).grid(row=2, column=1)

ttk.Label(tab1, text = "------------------------------------", font=("segoe UI", 16)).grid(row=3, column=1)
ttk.Label(tab1, text = "------------------------------------", font=("segoe UI", 16)).grid(row=3, column=0)
labelSmokeSensor = ttk.Label(tab1, text = "Smoke Sensor", font = ("segoe UI", 15)).grid(row=4, column=0)
labelSmokeSensorValue = ttk.Label(tab1, textvariable = smokeSensorValue, foreground = "green", font = ("segoe UI", 25, 'bold')).grid(row=5, column=0)

labelExit = ttk.Label(tab1, text = "Close User Interface", font = ("segoe UI", 12)).grid(row=5, column=1, sticky="SE")
buttonExit = ttk.Button(tab1, text = "QUIT!", command = window.destroy).grid(row=6, column=1, sticky="SE")

labelThershold = ttk.Label(tab1, text = "").grid(row=2, column=3)
labelThershold = ttk.Label(tab1, text = "").grid(row=3, column=3)
labelThershold = ttk.Label(tab1, text = "").grid(row=4, column=3)
labelThershold = ttk.Label(tab1, text = "").grid(row=5, column=3)
labelThershold = ttk.Label(tab1, text = "").grid(row=6, column=3)

#labelThershold = tk.Label(window, text="Help Window").grid(row=7, column=3)
#buttonHint = tk.Button(window, text="Help!", command=hint).grid(row=8, column=3)
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

t1 = Thread(target = voiceCommand).start()
t2 = Thread(target = sendMQ2Data).start()
t3 = Thread(target = continuosUpdateSmokeSensorValue).start()
t4 = Thread(target=hint).start()

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
