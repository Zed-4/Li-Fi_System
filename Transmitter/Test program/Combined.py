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
import sys

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

flag = True
tries = 3
triesY_axis = 370
triesColor = "orange"
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

def loginValidate():
    if (varUsername.get() == username and varPassword.get() == password):
        print("Login successful!")
        window.deiconify()
        loginWindow.destroy()
        global flag
        flag = False
    else:
        global tries
        tries -= 1
        global triesY_axis
        global triesColor
        my_canvas.create_text(190, triesY_axis, text = f"Wrong username/password combination! Tries left: {tries}", fill= triesColor, font = ("segoe UI", 12))
        #print(f"Wrong username/password combination! Tries left: ", {tries})
        triesY_axis += 20
        triesColor = "red"
        if tries == 0:
            cancel()
def login():
    my_canvas.create_text(140, 20, text= "Please Login for full access!", fill= "#15E8F3", font = ("segoe UI", 16))
    my_canvas.create_text(850, 200, text= "     Team\nMellowship", fill= "#0B3E91", font = ("segoe UI", 32, 'bold'))
    my_canvas.create_text(850, 350, text= "Li-Fi SYSTEM", fill= "#15E8F3", font = ("segoe UI", 32, 'bold'))
    my_canvas.create_text(140, 100, text= "Username", fill= "white", font = ("segoe UI", 20))
    my_canvas.create_text(140, 220, text= "Password", fill= "white", font = ("segoe UI", 20))
    #labelUserLogin = ttk.Label(loginWindow, text = "Please Login for full access!", font = ("segoe UI", 12)).place(x=5, y=20)
    #labelUserLogin = ttk.Label(loginWindow, text = "Username", font = ("segoe UI", 20)).place(x=140, y=100)
    InputLoginUser = ttk.Entry(loginWindow, textvariable = varUsername, font = ('segoe UI', 15, 'bold')).place(x=70, y=150)
    #labelUserPass = ttk.Label(loginWindow, text = "Password", font = ("segoe UI", 20)).place(x=140, y=220)
    InputLoginPass = ttk.Entry(loginWindow, textvariable = varPassword, show="*", font = ('segoe UI', 15, 'bold')).place(x=70, y=270)
    buttonSendLogin = ttk.Button(loginWindow, text = "Login", command = loginValidate).place(x=100, y=320)
    buttonSendLogin = ttk.Button(loginWindow, text = "Cancel", command = cancel).place(x=200, y=320)
    loginWindow.update()
def cancel():
    window.destroy() #Removes the toplevel window
    loginWindow.destroy() #Removes the hidden root window
    sys.exit() #Ends the script

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
def doStuff():
    if varLight == 1:
        GPIO.output(LED_PIN, GPIO.HIGH)
    elif varLight == 1:
        GPIO.output(LED_PIN, GPIO.LOW)
    print("I did it")
def hint():
    ttk.Label(tab2, text = "Valid Commands", foreground = "light blue", font=("segoe UI", 38, "bold")).grid(row=0, column=1, sticky="n")
    ttk.Label(tab2, text = "hello, clear, time", font=("segoe UI", 20)).grid(row=1, column=1, sticky="n")
    ttk.Label(tab2, text = "Smoke", font=("segoe UI", 20)).grid(row=2, column=1, sticky="n")
    ttk.Label(tab2, text = "Temperature", font=("segoe UI", 20)).grid(row=3, column=1, sticky="n")
    ttk.Label(tab2, text = "Humidity", font=("segoe UI", 20)).grid(row=4, column=1, sticky="n")
    ttk.Label(tab2, text = "Pressure", font=("segoe UI", 20)).grid(row=5, column=1, sticky="n")
    ttk.Label(tab2, text = "Open", font=("segoe UI", 20)).grid(row=6, column=1, sticky="n")
    ttk.Label(tab2, text = "Close", font=("segoe UI", 20)).grid(row=7, column=1, sticky="n")
    ttk.Label(tab2, text = "On", font=("segoe UI", 20)).grid(row=8, column=1, sticky="n")
    ttk.Label(tab2, text = "Off", font=("segoe UI", 20)).grid(row=9, column=1, sticky="n")
    ttk.Label(tab2, text = "RGB", font=("segoe UI", 20)).grid(row=10, column=1, sticky="n")
    ttk.Label(tab2, text = "Intensity \"%0-100\"", font=("segoe UI", 20)).grid(row=11, column=1, sticky="n")

    ttk.Label(tab2, text = "⩤⩥", foreground = "gray", font=("segoe UI", 20)).grid(row=1, column=2, padx= (120,180))
    ttk.Label(tab2, text = "⩤⩥", foreground = "gray", font=("segoe UI", 20)).grid(row=2, column=2, padx= (120,180))
    ttk.Label(tab2, text = "⩤⩥", foreground = "gray", font=("segoe UI", 20)).grid(row=3, column=2, padx= (120,180))
    ttk.Label(tab2, text = "⩤⩥", foreground = "gray", font=("segoe UI", 20)).grid(row=4, column=2, padx= (120,180))
    ttk.Label(tab2, text = "⩤⩥", foreground = "gray", font=("segoe UI", 20)).grid(row=5, column=2, padx= (120,180))
    ttk.Label(tab2, text = "⩤⩥", foreground = "gray", font=("segoe UI", 20)).grid(row=6, column=2, padx= (120,180))
    ttk.Label(tab2, text = "⩤⩥", foreground = "gray", font=("segoe UI", 20)).grid(row=7, column=2, padx= (120,180))
    ttk.Label(tab2, text = "⩤⩥", foreground = "gray", font=("segoe UI", 20)).grid(row=8, column=2, padx= (120,180))
    ttk.Label(tab2, text = "⩤⩥", foreground = "gray", font=("segoe UI", 20)).grid(row=9, column=2, padx= (120,180))
    ttk.Label(tab2, text = "⩤⩥", foreground = "gray", font=("segoe UI", 20)).grid(row=10, column=2, padx= (120,180))
    ttk.Label(tab2, text = "⩤⩥", foreground = "gray", font=("segoe UI", 20)).grid(row=11, column=2, padx= (120,180))

    ttk.Label(tab2, text = "Description", foreground = "light blue", font=("segoe UI", 38, "bold")).grid(row=0, column=3, sticky="n")
    ttk.Label(tab2, text = "Extra commands", font=("segoe UI", 20)).grid(row=1, column=3, sticky="n")
    ttk.Label(tab2, text = "Trigger Smoke sensor", font=("segoe UI", 20)).grid(row=2, column=3, sticky="n")
    ttk.Label(tab2, text = "Report Temperature", font=("segoe UI", 20)).grid(row=3, column=3, sticky="n")
    ttk.Label(tab2, text = "Report humidity", font=("segoe UI", 20)).grid(row=4, column=3, sticky="n")
    ttk.Label(tab2, text = "Report pressure", font=("segoe UI", 20)).grid(row=5, column=3, sticky="n")
    ttk.Label(tab2, text = "Open door", font=("segoe UI", 20)).grid(row=6, column=3, sticky="n")
    ttk.Label(tab2, text = "Close door", font=("segoe UI", 20)).grid(row=7, column=3, sticky="n")
    ttk.Label(tab2, text = "Turn lights On", font=("segoe UI", 20)).grid(row=8, column=3, sticky="n")
    ttk.Label(tab2, text = "Turn lights Off", font=("segoe UI", 20)).grid(row=9, column=3, sticky="n")
    ttk.Label(tab2, text = "Light color Options", font=("segoe UI", 20)).grid(row=10, column=3, sticky="n")
    ttk.Label(tab2, text = "Light intensity in %", font=("segoe UI", 20)).grid(row=11, column=3, sticky="n")
    tab2.update()
    
window = ThemedTk(themebg=True)
window.set_theme("breeze")
window.title("TRANSMITTER")
tabControl = ttk.Notebook(window)
#window.geometry("600x300+760+200")
window.geometry("1024x600")
window.iconbitmap(r"@/home/mellowship/Downloads/voice_recognition/Images/bulbIcon.xbm")

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text ='MAIN SCREEN')
tabControl.add(tab2, text ='HELP SCREEN')
tabControl.pack(expand = 1, fill ="both")

loginWindow = tk.Toplevel(window)
#loginWindow = ThemedTk(themebg=True)
#loginWindow.set_theme("breeze")
loginWindow.title("LOGIN")
loginWindow.geometry("1024x600")
loginWindow.iconbitmap(r"@/home/mellowship/Downloads/voice_recognition/Images/bulbIcon.xbm")
#412x430

bg = tk.PhotoImage(file = r"/home/mellowship/Downloads/voice_recognition/Images/NASA_1_1024x600.png")
my_canvas = tk.Canvas(loginWindow, width= 1024, height= 600)
my_canvas.pack(fill= "both", expand= True)
my_canvas.create_image(0,0, image= bg, anchor= "nw")

username = "admin"
password = "admin"
varUsername = tk.StringVar()
varUsername.set("")
varPassword = tk.StringVar()
varPassword.set("")

smokeSensorValue = tk.StringVar()
smokeSensorValue.set("N/A")

varEntry = tk.StringVar()
varEntry.set("")

v1 = tk.DoubleVar()
v1.set(MQ2_THRESHOLD)
v2 = tk.DoubleVar()
varRadio = tk.IntVar()
varLight = tk.IntVar()

#labelRec = tk.Label(window, text = "Voice Recognition").grid(row=0, column=0)
#buttonCapture = tk.Button(window, text = "Capture", command = voiceCommand).grid(row=1, column=0)

labelSmokeSensor = ttk.Label(tab1, text = "Lighting Setting", font = ("segoe UI", 20)).grid(row=4, column=1)
rbOn = ttk.Radiobutton(tab1, text="ON",command= doStuff, variable=varLight, value=1).place(x=700, y=325)
rbOff = ttk.Radiobutton(tab1, text="OFF",command= doStuff, variable=varLight, value=0).place(x=700, y=350)

rb = ttk.Radiobutton(tab1, text="WHITE",variable=varRadio, value=0).place(x=760, y=325)
rb1 = ttk.Radiobutton(tab1, text="RED",variable=varRadio, value=1).place(x=760, y=350)
rb2 = ttk.Radiobutton(tab1, text="GREEN",variable=varRadio, value=2).place(x=760, y=375)
rb3 = ttk.Radiobutton(tab1, text="BLUE",variable=varRadio, value=3).place(x=760, y=400)

labelThershold = ttk.Label(tab1, text = "Light Intensity", font = ("segoe UI", 20)).grid(row=4, column=0)
s1 = TickScale(tab1,variable = v2, orient='horizontal', from_=0, to=100, tickinterval=20, resolution=10, length=250).grid(row=5, column=0)
v2.set(0.8)
buttonSet = ttk.Button(tab1, text = "SET", command = doStuff).grid(row=6, column=0)

labelKeyboard = ttk.Label(tab1, text = "Keyboard", font = ("segoe UI", 20)).grid(row=0, column=0, pady= (20,0))
userInput = ttk.Entry(tab1, textvariable = varEntry, font = ('segoe UI', 15, 'bold')).grid(row=1, column=0)
buttonSend = ttk.Button(tab1, text = "SEND", command = keyboardCommand).grid(row=2, column=0)

labelThershold = ttk.Label(tab1, text = "Smoke Thershold", font = ("segoe UI", 20)).grid(row=0, column=1, pady= (20,0))
s1 = TickScale(tab1,variable = v1, orient='horizontal', from_=0, to=1.5, tickinterval=0.5, resolution=0.1, length=250).grid(row=1, column=1)
v1.set(0.8)
buttonSet = ttk.Button(tab1, text = "SET", command = setMQ2Thershold).grid(row=2, column=1)

ttk.Label(tab1, text = " ⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥", foreground = "gray", font=("segoe UI", 18)).grid(row=3, column=0, pady= (50,50))
ttk.Label(tab1, text = "⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥⩤⩥", foreground = "gray", font=("segoe UI", 18)).grid(row=3, column=1, pady= (50,50))

labelSmokeSensor = ttk.Label(tab1, text = "Smoke Sensor", font = ("segoe UI", 20)).grid(row=7, column=0, pady=(50,0))
labelSmokeSensorValue = ttk.Label(tab1, textvariable = smokeSensorValue, foreground = "green", font = ("segoe UI", 35, 'bold')).grid(row=8, column=0)

labelExit = ttk.Label(tab1, text = "Close User Interface", font = ("segoe UI", 12, 'bold')).place(x=850, y=500)
buttonExit = ttk.Button(tab1, text = "QUIT!", command = window.destroy).place(x=880, y=530)

# labelThershold = ttk.Label(tab1, text = "").grid(row=2, column=3)
# labelThershold = ttk.Label(tab1, text = "").grid(row=3, column=3)
# labelThershold = ttk.Label(tab1, text = "").grid(row=4, column=3)
# labelThershold = ttk.Label(tab1, text = "").grid(row=5, column=3)
# labelThershold = ttk.Label(tab1, text = "").grid(row=6, column=3)

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
t5 = Thread(target=login).start()
window.withdraw()
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
