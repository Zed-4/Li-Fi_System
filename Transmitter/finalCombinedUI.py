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
from math import exp

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP

#cd Downloads/voice_recognition/
#python recognitionFinal.py

MQ2_THRESHOLD = 5000
LED_PIN = 4
PERIOD = 0.02
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
cs = digitalio.DigitalInOut(board.D22)
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

def loginValidateAdmin():
    if (varUsernameAdmin.get() == usernameAdmin and varPasswordAdmin.get() == passwordAdmin):
        varUsernameAdmin.set("")
        varPasswordAdmin.set("")
        print("ADMIN Login successful!")
        deletetab()
        global tab3
        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3, text='ADMIN')
        tabControl.select(tab3)
        labelLogin.config(text="ADMIN Logged in!")
        adminLogged()
    else:
        ttk.Label(tab3, text="Wrong username/password combination!", foreground='red', font=("segoe UI", 12)).place(x=190, y=370)


def loginValidate():
    if (varUsername.get() == username and varPassword.get() == password):
        varUsername.set("")
        varPassword.set("")
        print("User Login successful!")
        labelLogin.config(text="User Logged in!")
        labelLoginAdmin.config(text="User Logged in!", foreground="red")
        window.deiconify()
        loginWindow.destroy()
    else:
        global tries
        tries -= 1
        global triesY_axis
        global triesColor
        my_canvas.create_text(220, triesY_axis, text=f"Wrong username/password combination! Tries left: {tries}", fill=triesColor, font=("segoe UI", 12))
        triesY_axis += 20
        triesColor = "red"
        if tries == 0:
            cancel()


def login():
    loginWindow.lift()
    loginWindow.focus_force()
    my_canvas.create_text(160, 20, text="Please Login for full access!", fill="orange", font=("Consolas", 12))
    my_canvas.create_text(850, 200, text="     Team\nMellowship", fill="#1661DA", font=("segoe UI", 32, 'bold'))
    my_canvas.create_text(850, 350, text="Li-Fi SYSTEM", fill="#15E8F3", font=("segoe UI", 32, 'bold'))
    my_canvas.create_text(140, 100, text="Username", fill="white", font=("Consolas", 20, "bold"))
    my_canvas.create_text(140, 220, text="Password", fill="white", font=("Consolas", 20, "bold"))
    InputLoginUser = ttk.Entry(loginWindow, textvariable=varUsername, font=('segoe UI', 15, 'bold')).place(x=70, y=150)
    InputLoginPass = ttk.Entry(loginWindow, textvariable=varPassword, show="*", font=('segoe UI', 15, 'bold')).place(x=70, y=270)
    buttonSendLogin = ttk.Button(loginWindow, text="Login", command=loginValidate).place(x=100, y=320)
    buttonSendLogin = ttk.Button(loginWindow, text="Cancel", command=cancel).place(x=220, y=320)
    loginWindow.update()

def admin():
    global labelLoginAdmin
    labelLoginAdmin = ttk.Label(tab3, text="User Login Status!", foreground="green", font=("Consolas", 12, "bold"))
    labelLoginAdmin.place(x=15, y=10)
    ttk.Label(tab3, text="Login into Admin for full access!", foreground="orange", font=("Consolas", 16, "bold")).place(x=30, y=50)
    ttk.Label(tab3, text="This section is for adjusting", font=("segoe UI", 22, "bold")).place(x=450, y=190)
    ttk.Label(tab3, text="Admin privileged settings!", font=("segoe UI", 22, "bold")).place(x=450, y=230)
    ttk.Label(tab3, text="Username", font=("segoe UI", 20, "bold")).place(x=140, y=100)
    ttk.Label(tab3, text="Password", font=("segoe UI", 20, "bold")).place(x=140, y=220)
    ttk.Entry(tab3, textvariable=varUsernameAdmin, font=('segoe UI', 15, 'bold')).place(x=70, y=150)
    ttk.Entry(tab3, textvariable=varPasswordAdmin, show="*", font=('segoe UI', 15, 'bold')).place(x=70, y=270)
    ttk.Button(tab3, text="Login", command=loginValidateAdmin).place(x=150, y=320)
    loginWindow.update()


def adminLogged():
    panedAdminFirst = ttk.PanedWindow(tab3)
    panedAdminFirst.grid(row=1, column=0, padx=(15, 0), pady=(5, 30), sticky="nw", rowspan=3)
    panedAdminLogin = ttk.Frame(panedAdminFirst, width=350, height=40)
    panedAdminFirst.add(panedAdminLogin, weight=1)
    panedAdminLogin.pack_propagate(False)

    panedAdmin = ttk.PanedWindow(tab3)
    panedAdmin.grid(row=1, column=0, pady=(50, 100), padx=(40, 50), sticky="n", rowspan=3)
    pane_smokeThershold = ttk.Frame(panedAdmin, width=350, height=200)
    panedAdmin.add(pane_smokeThershold, weight=1)
    pane_smokeThershold.pack_propagate(False)

    panedAdminOne = ttk.PanedWindow(tab3)
    panedAdminOne.grid(row=1, column=1, pady=(50, 100), padx=(50, 40), sticky="n", rowspan=3)
    pane_lifiThershold = ttk.Frame(panedAdminOne, width=350, height=200)
    panedAdminOne.add(pane_lifiThershold, weight=1)
    pane_lifiThershold.pack_propagate(False)

    panedThree = ttk.PanedWindow(tab3)
    panedThree.grid(row=2, column=0, pady=(250, 100), sticky="n", rowspan=3)
    pane_SeparatorThree = ttk.Frame(panedThree, width=512, height=50)
    panedThree.add(pane_SeparatorThree, weight=1)
    pane_SeparatorThree.pack_propagate(False)
    panedFour = ttk.PanedWindow(tab3)
    panedFour.grid(row=2, column=1, pady=(250, 100), sticky="n", rowspan=3)
    pane_SeparatorFour = ttk.Frame(panedFour, width=512, height=50)
    panedFour.add(pane_SeparatorFour, weight=1)
    pane_SeparatorFour.pack_propagate(False)

    panedAdminTwo = ttk.PanedWindow(tab3)
    panedAdminTwo.grid(row=3, column=0, pady=(320, 10), padx=(50, 100), sticky="n", rowspan=3)
    pane_light = ttk.Frame(panedAdminTwo, width=350, height=150)
    panedAdminTwo.add(pane_light, weight=1)
    pane_light.pack_propagate(False)

    panedOne = ttk.PanedWindow(tab3)
    panedOne.grid(row=3, column=1, pady=(200, 5), sticky="n", rowspan=3)
    pane_console = ttk.Frame(panedOne)
    panedOne.add(pane_console, weight=1)

    # Adding label and a listboxAdmin for console
    ttk.Label(pane_console, text="Console", font=("Consolas", 20, "bold")).pack(side="top", fill="none", anchor="nw")
    butt = ttk.Button(pane_console, text="CLEAR", command=clearConsole)
    butt.pack(side="bottom", fill="none", pady=(4, 0))
    butt1 = ttk.Button(pane_console, text="CHECK", command=checkList)
    butt1.pack(side="top", fill="none", pady=(0, 4))
    global listboxAdmin
    listboxAdmin = tk.Listbox(pane_console, background="white", foreground="black", width=40, height=6, font=("Consolas", 15, "bold"))
    listboxAdmin.pack(side="left", fill="both")
    listboxAdmin.insert("end", "Test all peripherals: 'CHECK' button")
    listboxAdmin.itemconfig(0, {'fg': 'orange'})
    listboxAdmin.insert("end", "------------------------------------------------------------")
    # Adding a Scrollbar to the listboxAdmin
    scrollbar = ttk.Scrollbar(pane_console)
    scrollbar.pack(side="left", fill="both")
    listboxAdmin.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listboxAdmin.yview)

    # panedAdminFour = ttk.PanedWindow(tab3)
    # panedAdminFour.grid(row=3, column=1, padx=(298, 5), pady=(440, 5), sticky="n", rowspan=3)
    # pane_quitAdmin = ttk.Frame(panedAdminFour, width=200, height=90)
    # panedAdminFour.add(pane_quitAdmin, weight=1)
    # pane_quitAdmin.pack_propagate(False)

    labelLoginAdmin = ttk.Label(panedAdminLogin, text="ADMIN Logged in!", foreground="green", font=("Consolas", 12, "bold"))
    labelLoginAdmin.pack(side="top", fill="both", anchor="nw", pady=(5, 5), padx=(0, 5))

    ttk.Label(pane_smokeThershold, text="Smoke Thershold", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(5, 5))
    TickScale(pane_smokeThershold, variable=varSmoke, orient='horizontal', from_=0, to=10000, tickinterval=5000, resolution=50, length=250).pack(side="top", fill="none", anchor="center", pady=(5, 5), padx=(5, 5))
    ttk.Button(pane_smokeThershold, text="SET", command=setMQ2Thershold).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(5, 5))#tMQ2Thershold).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(5, 5))
    varSmoke.set(MQ2_THRESHOLD)#tMQ2Thershold).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(5, 5))

    ttk.Label(pane_lifiThershold, text="Light Period", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(5, 5))
    # TickScale(pane_lifiThershold, variable=varThershold, orient='horizontal', from_=0, to=1, tickinterval=0.01, resolution=0.001, length=250).pack(side="top", fill="none", anchor="center", pady=(5, 5), padx=(5, 5))
    ttk.Entry(pane_lifiThershold, textvariable=varThershold, font=('segoe UI', 15, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 5), padx=(5, 5))
    ttk.Button(pane_lifiThershold, text="SET", command=setLightThreshold).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(5, 5))
    varThershold.set(PERIOD)

    ttk.Separator(pane_SeparatorThree, orient="horizontal").pack(fill="x", expand=True)
    ttk.Separator(pane_SeparatorFour, orient="horizontal").pack(fill="x", expand=True)

    ttk.Label(pane_light, text="Light Switch", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(5, 5))
    ttk.Radiobutton(pane_light, text="ON", variable=varLightTest, value=1, command=lightSwitchTest).pack(side="top", fill="none", anchor="nw", pady=(5, 5), padx=(100, 5))
    ttk.Radiobutton(pane_light, text="OFF", variable=varLightTest, value=0, command=lightSwitchTest).pack(side="top", fill="none", anchor="nw", pady=(5, 10), padx=(100, 5))

    ttk.Label(tab3, text="Close User Interface", font=("segoe UI", 12, 'bold')).place(x=818, y=463)
    ttk.Button(tab3, text="QUIT!", command=cancel).place(x=852, y=485)

def checkList():
    listboxAdmin.insert("end", "Microphone Check:")
    listboxAdmin.yview("end")
    listboxAdmin.insert("end", "     Passed")
    listboxAdmin.yview("end")
    listboxAdmin.itemconfig("end", {'fg': 'green'})

    listboxAdmin.insert("end", "Smoke Sensor Check:")
    listboxAdmin.yview("end")
    checkSmoke()
    listboxAdmin.insert("end", "LED light User Check:")
    listboxAdmin.yview("end")

    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(LED_PIN, GPIO.HIGH)

    global popupWindow
    popupWindow = tk.Tk()
    popupWindow.title("Check List")
    popupWindow.geometry("400x100")
    x_cordinate = int((popupWindow.winfo_screenwidth()/2) - (popupWindow.winfo_width()/2))
    y_cordinate = int((popupWindow.winfo_screenheight()/2) - (popupWindow.winfo_height()/2))
    popupWindow.geometry("+{}+{}".format(x_cordinate, y_cordinate))
    ttk.Label(popupWindow, text="Did the LED light Blinked 3 times?", font=("Consolas", 12, 'bold')).pack()
    ttk.Button(popupWindow, text="YES", command=LEDCheckYes).pack(side="left", padx=(50, 0))
    ttk.Button(popupWindow, text="NO", command=LEDCheckNo).pack(side="right", padx=(0, 50))


def LEDCheckYes():
    listboxAdmin.insert("end", "     Passed")
    listboxAdmin.itemconfig("end", {'fg': 'green'})
    listboxAdmin.insert("end", "------------------------------------------------------------")
    listboxAdmin.yview("end")
    popupWindow.destroy()


def LEDCheckNo():
    listboxAdmin.insert("end", "     Failed")
    listboxAdmin.itemconfig("end", {'fg': 'red'})
    listboxAdmin.insert("end", "------------------------------------------------------------")
    listboxAdmin.yview("end")
    popupWindow.destroy()


def checkSmoke():
    if (smokePPM < 10000) and (smokePPM != 0):
        listboxAdmin.insert("end", "     Passed")
        listboxAdmin.itemconfig("end", {'fg': 'green'})
        listboxAdmin.insert("end", f"     With value of {smokeSensorValue.get()} ppm")
        listboxAdmin.yview("end")
    else:
        listboxAdmin.insert("end", "     Failed")
        listboxAdmin.itemconfig("end", {'fg': 'red'})
        listboxAdmin.insert("end", f"     With value of {smokeSensorValue.get()} ppm")
        listboxAdmin.yview("end")


# Clears the Console's screen
def clearConsole():
    listboxAdmin.delete(0, "end")
    listboxAdmin.insert("end", "Test all peripherals: 'CHECK' button")
    listboxAdmin.itemconfig(0, {'fg': 'orange'})
    listboxAdmin.insert("end", now.strftime(f'[%I:%M:%S %p] Mellow: Screen Cleared!'))
    listboxAdmin.itemconfig("end", {'fg': 'green'})
    listboxAdmin.insert("end", "------------------------------------------------------------")


def deletetab():
    for item in tabControl.winfo_children():
        if str(item) == (tabControl.select()):
            item.destroy()
            return


def cancel():
    GPIO.output(LED_PIN, GPIO.LOW)
    window.destroy()
    sys.exit()


def lightSwitchTest():
    if varLightTest.get() == 1:
        GPIO.output(LED_PIN, GPIO.HIGH)
    if varLightTest.get() == 0:
        GPIO.output(LED_PIN, GPIO.LOW)


def lightSwitch(): 
    if varLight.get() == 1:
        send_byte(ord("O"))
    elif varLight.get() == 0:
        send_byte(ord("f"))


def lightColor():
    if varRadio.get() == 0:
        send_byte(ord("w"))
    elif varRadio.get() == 1:
        send_byte(ord("r"))
    elif varRadio.get() == 2:
        send_byte(ord("g"))
    elif varRadio.get() == 3:
        send_byte(ord("b"))


def lightIntensity():
    if varIntensity.get() == 1:
        send_byte(ord("x"))
    elif varIntensity.get() == 2:
        send_byte(ord("y"))
    elif varIntensity.get() == 3:
        send_byte(ord("z"))   


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
    now = datetime.now()
    currentTime()
    #listbox.insert("end", now.strftime(f"[%I:%M:%S %p] Mellow: Transmitting \'{response}\'..."))
    listbox.select_clear(listbox.size() - 2)
    listbox.select_set("end")
    listbox.yview("end")
    listbox.itemconfig(0, {'fg': 'black'})
    print(f"Transmitting command ... \'{response}\'")
    
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

    if response == "":
            pass
    elif closeProgram in response:
        print("Program has been terminated. Goodbye!")
        print("-------------------------------------------------------------------")
        cancel()
    elif smoke in response:
        listbox.insert("end", now.strftime('[%I:%M:%S %p] Mellow: Smoke Detected!'))
        listbox.itemconfig("end", {'fg': 'red'})
        listbox.select_clear(listbox.size() - 2)
        listbox.select_set("end")
        listbox.yview("end")
        print("Smoke detected!")
        send_byte(ord("s"))
        commandMessage(response)
    elif temperature in response:
        send_byte(ord("t"))
        commandMessage(response)
    elif humidity in response:
        send_byte(ord("h"))
        commandMessage(response)
    elif pressure in response:
        send_byte(ord("p"))
        commandMessage(response)
    elif doorOpen in response:
        send_byte(ord("o"))
        commandMessage(response)
    elif doorClose in response:
        send_byte(ord("c"))
        commandMessage(response)
    elif hello in response:
        listbox.insert("end", now.strftime('[%I:%M:%S %p] Mellow: Hello, i\'m li-fi!'))
        listbox.select_clear(listbox.size() - 2)
        listbox.select_set("end")
        listbox.yview("end")
        print("Hello, i'm li-fi!")
    elif readTime in response:
        now = datetime.now()
        listbox.insert("end",now.strftime('[%I:%M:%S %p] Mellow: [%I:%M:%S %p] 😁'))
        listbox.select_clear(listbox.size() - 2)
        listbox.select_set("end")
        listbox.yview("end")
        print(now.strftime('\t[%I:%M:%S %p]'), "😁")
    elif clear in response:
        send_byte(ord("l"))
        clearConsoleOne()
        cls()
        print("Screen cleared!")
    elif ringOn in response:
        send_byte(ord("O"))
    elif ringOff in response:
        send_byte(ord("f"))
    elif ringWhite in response:
        send_byte(ord("w"))
    elif ringRed in response:
        send_byte(ord("r"))
    elif ringGreen in response:
        send_byte(ord("g"))
    elif ringBlue in response:
        send_byte(ord("b"))
    elif ringLow:
        send_byte(ord("x"))
    elif ringMedium in response:
        send_byte(ord("y"))
    elif ringHigh in response:
        send_byte(ord("z"))
    else:
        listbox.insert("end",now.strftime('[%I:%M:%S %p] Mellow: Command Invalid!'))
        listbox.itemconfig("end", {'fg': 'red'})
        listbox.select_clear(listbox.size() - 2)
        listbox.select_set("end")
        listbox.yview("end")


def currentTime():
    global now
    now = datetime.now()


def micReady():
    GPIO.output(LED_PIN, GPIO.HIGH)
    currentTime()
    listbox.insert("end", now.strftime('[%I:%M:%S %p] Mellow: Preparing microphone port...'))
    listbox.itemconfig(0, {'fg': 'orange'})
    listbox.select_clear(listbox.size() - 2)
    listbox.select_set("end")
    listbox.yview("end")
    print("Preparing microphone port...")
    command = get_command()
    listbox.insert("end", now.strftime('[%I:%M:%S %p] Mellow: Mic Ready!'))
    listbox.itemconfig(0, {'fg': 'green'})
    listbox.select_clear(listbox.size() - 2)
    listbox.select_set("end")
    listbox.yview("end")
    print("Mic Ready!")
    print("-------------------------------------------------------------------")


def voiceCommand():
    while True:
        command = get_command()
        #print(command)
        if (command == "hey mellow"):
            currentTime()
            send_byte(ord("m"))
            time.sleep(0.5)
            listbox.insert("end", now.strftime('[%I:%M:%S %p] Mellow: How can I help?'))
            listbox.itemconfig("end", {'fg': 'green'})
            listbox.select_clear(listbox.size() - 2)
            listbox.select_set("end")
            listbox.yview("end")
            #print("How can I help?")
            command = get_command()
            condition(command)
            print("-------------------------------------------------------------------")
        else:
            pass


def keyboardCommand():
    command = varEntry.get()
    condition(command)
    print("-------------------------------------------------------------------")


def commandMessage(command):
    listbox.insert("end", now.strftime(f'[%I:%M:%S %p] Mellow: command \'{command}\' sent'))
    listbox.select_clear(listbox.size() - 2)
    listbox.select_set("end")
    listbox.yview("end")


def continuosUpdateSmokeSensorValue():
    while True:
        global smokePPM
        smokePPM = int(mqPPM(smokeChannel.voltage))
        if smokePPM < 300:
            smokeSensorValue.set(str(smokePPM) + "<300")
        elif smokePPM > 10000:
            smokeSensorValue.set(str(smokePPM) + ">10000")
        else:
            smokeSensorValue.set(str(smokePPM))
        time.sleep(0.1)

def mqPPM(voltage):
    ppm = int(exp((voltage+0.89)/0.29))
    return ppm


def sendMQ2Data():
    global MQ2_THRESHOLD
    while True:
        #currentSmokeSensorValue = float(str(smokeChannel.voltage))
        currentSmokeSensorValue = int(str(mqPPM(smokeChannel.voltage)))
        if currentSmokeSensorValue > MQ2_THRESHOLD:
            send_byte(ord("s"))
            time.sleep(2)
        time.sleep(0.1)


def setMQ2Thershold():
    global MQ2_THRESHOLD
    MQ2_THRESHOLD = varSmoke.get()
    smokeSensorTValue.set("Smoke Threshold: " + str(int(MQ2_THRESHOLD)) + " ppm")



def setLightThreshold():
    global PERIOD
    PERIOD = varThershold.get()


def doStuff():
    print("test worked!")


def hint():
    ttk.Label(tab2, text="Valid Commands", foreground="forest green", font=("segoe UI", 38, "bold")).grid(row=0, column=0, sticky="n", pady=(0, 50), padx=(20, 0))
    ttk.Label(tab2, text="hello, clear, time", font=("Consolas", 20)).grid(row=1, column=0, sticky="n")
    ttk.Label(tab2, text="Smoke", font=("Consolas", 20)).grid(row=2, column=0, sticky="n")
    ttk.Label(tab2, text="Temperature", font=("Consolas", 20)).grid(row=3, column=0, sticky="n")
    ttk.Label(tab2, text="Humidity", font=("Consolas", 20)).grid(row=4, column=0, sticky="n")
    ttk.Label(tab2, text="Pressure", font=("Consolas", 20)).grid(row=5, column=0, sticky="n")
    ttk.Label(tab2, text="Open", font=("Consolas", 20)).grid(row=6, column=0, sticky="n")
    ttk.Label(tab2, text="Close", font=("Consolas", 20)).grid(row=7, column=0, sticky="n")
    ttk.Label(tab2, text="On", font=("Consolas", 20)).grid(row=8, column=0, sticky="n")
    ttk.Label(tab2, text="Off", font=("Consolas", 20)).grid(row=9, column=0, sticky="n")
    ttk.Label(tab2, text="white-red-green-blue", font=("Consolas", 20)).grid(row=10, column=0, sticky="n")
    ttk.Label(tab2, text="Intensity: \"low-medium-high\"", font=("Consolas", 20)).grid(row=11, column=0, sticky="n")

    ttk.Separator(tab2, orient="vertical").grid(row=0, column=1, rowspan=12, sticky='ns', padx=(50, 50))

    ttk.Label(tab2, text="Description", foreground="forest green", font=("segoe UI", 38, "bold")).grid(row=0, column=2, sticky="n", pady=(0, 50))
    ttk.Label(tab2, text="Extra commands", font=("segoe UI", 20)).grid(row=1, column=2, sticky="n")
    ttk.Label(tab2, text="Trigger Smoke sensor", font=("segoe UI", 20)).grid(row=2, column=2, sticky="n")
    ttk.Label(tab2, text="Report Temperature", font=("segoe UI", 20)).grid(row=3, column=2, sticky="n")
    ttk.Label(tab2, text="Report humidity", font=("segoe UI", 20)).grid(row=4, column=2, sticky="n")
    ttk.Label(tab2, text="Report pressure", font=("segoe UI", 20)).grid(row=5, column=2, sticky="n")
    ttk.Label(tab2, text="Open door", font=("segoe UI", 20)).grid(row=6, column=2, sticky="n")
    ttk.Label(tab2, text="Close door", font=("segoe UI", 20)).grid(row=7, column=2, sticky="n")
    ttk.Label(tab2, text="Turn lights On", font=("segoe UI", 20)).grid(row=8, column=2, sticky="n")
    ttk.Label(tab2, text="Turn lights Off", font=("segoe UI", 20)).grid(row=9, column=2, sticky="n")
    ttk.Label(tab2, text="Light color Options", font=("segoe UI", 20)).grid(row=10, column=2, sticky="n")
    ttk.Label(tab2, text="Light intensity in 3 settings", font=("segoe UI", 20)).grid(row=11, column=2, sticky="n")
    tab2.update()

def themeSwitch():
    if varSwitch.get() == 0:
        listbox.config(foreground="#313131", background="white")
        switch.config(text="Light Mode")
        window_style.theme_use("forest-light")
    elif varSwitch.get() == 1:
        listbox.config(foreground="white", background="#313131")
        switch.config(text="Dark Mode")
        window_style.theme_use("forest-dark")


def clearConsoleOne():
    listbox.delete(0, "end")
    currentTime()
    listbox.insert("end", now.strftime(f'[%I:%M:%S %p] Mellow: Screen Cleared!'))
    listbox.itemconfig("end", {'fg': 'green'})
    listbox.select_clear(listbox.size() - 2)
    listbox.select_set("end")
    listbox.yview("end")


imageIcon = "@/home/mellowship/Downloads/voice_recognition/Images/bulbIcon.xbm"
imagebg = "/home/mellowship/Downloads/voice_recognition/Images/NASA_1_1024x600.png"

window = tk.Tk()
window.title("TRANSMITTER")
tabControl = ttk.Notebook(window)
window.geometry("1024x600")
window.iconbitmap(imageIcon)

x_cordinate = int((window.winfo_screenwidth()/2) - (window.winfo_width()/2))
y_cordinate = int((window.winfo_screenheight()/2) - (window.winfo_height()/2))
window.geometry("+{}+{}".format(x_cordinate, y_cordinate))

window.tk.call("source", "forest-light.tcl")
window.tk.call("source", "forest-dark.tcl")

window_style = ttk.Style(window)
window_style.theme_use("forest-light")

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tabControl.add(tab1, text ='MAIN SCREEN')
tabControl.add(tab2, text ='HELP SCREEN')
tabControl.add(tab3, text='ADMIN')
tabControl.pack(expand = 1, fill ="both")

loginWindow = tk.Toplevel(window)
loginWindow.title("LOGIN")
loginWindow.geometry("1024x600")
loginWindow.iconbitmap(imageIcon)

x_cordinate = int((loginWindow.winfo_screenwidth()/2) - (loginWindow.winfo_width()/2))
y_cordinate = int((loginWindow.winfo_screenheight()/2) - (loginWindow.winfo_height()/2))
loginWindow.geometry("+{}+{}".format(x_cordinate, y_cordinate))

bg = tk.PhotoImage(file =imagebg)
my_canvas = tk.Canvas(loginWindow, width= 1024, height= 600)
my_canvas.pack(fill= "both", expand= True)
my_canvas.create_image(0,0, image= bg, anchor= "nw")

username = "admin"
password = "admin"
usernameAdmin = "admin"
passwordAdmin = "password"
varUsername = tk.StringVar()
varUsername.set("")
varPassword = tk.StringVar()
varPassword.set("")
varUsernameAdmin = tk.StringVar()
varUsernameAdmin.set("")
varPasswordAdmin = tk.StringVar()
varPasswordAdmin.set("")

smokeSensorValue = tk.StringVar()
smokeSensorValue.set("N/A")
smokeSensorTValue = tk.StringVar()

varEntry = tk.StringVar()
varEntry.set("")

varSmoke = tk.DoubleVar()
varSmoke.set(MQ2_THRESHOLD)
varIntensity = tk.IntVar()
varIntensity.set(0)
varThershold = tk.DoubleVar()
varThershold.set(PERIOD)
varLightTest = tk.IntVar()
varLightTest.set(1)
varIntensity = tk.IntVar()
varIntensity.set(3)
varSwitch = tk.IntVar()
varSwitch.set(0)
varRadio = tk.IntVar()
varLight = tk.IntVar()
varLight.set(0)

paned = ttk.PanedWindow(tab1)
paned.grid(row=0, column=0, padx=(0, 0), pady=(5, 30), sticky="nw", rowspan=3)
pane_login = ttk.Frame(paned, width=512, height=208)
paned.add(pane_login, weight=1)
pane_login.pack_propagate(False)

panedZero = ttk.PanedWindow(tab1)
panedZero.grid(row=0, column=1, padx=(0, 100), pady=(5, 30), sticky="e", rowspan=3)
pane_switch = ttk.Frame(panedZero, width=130, height=208)
panedZero.add(pane_switch, weight=1)
pane_switch.pack_propagate(False)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=1, column=0, pady=(5, 50), sticky="n", rowspan=3)
pane_keyboard = ttk.Frame(panedOne)
panedOne.add(pane_keyboard, weight=1)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=1, column=1, pady=(5, 50), sticky="n", rowspan=3)
pane_smoke = ttk.Frame(panedOne)
panedOne.add(pane_smoke, weight=1)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=2, column=0, pady=(50, 0), sticky="n", rowspan=3)
pane_SeparatorOne = ttk.Frame(panedOne, width=512)
panedOne.add(pane_SeparatorOne, weight=1)
pane_SeparatorOne.pack_propagate(False)
panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=2, column=1, pady=(50, 0), sticky="n", rowspan=3)
pane_SeparatorTwo = ttk.Frame(panedOne, width=512)
panedOne.add(pane_SeparatorTwo, weight=1)
pane_SeparatorTwo.pack_propagate(False)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=3, column=0, pady=(0, 0), sticky="n", rowspan=3)
pane_lighting = ttk.Frame(panedOne)
panedOne.add(pane_lighting, weight=1)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=3, column=1, pady=(0, 0), sticky="n", rowspan=3)
pane_intensity = ttk.Frame(panedOne)
panedOne.add(pane_intensity, weight=1)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=4, column=0, padx=(5, 5), pady=(142, 0), sticky="w", rowspan=3)
pane_voice = ttk.Frame(panedOne)
panedOne.add(pane_voice, weight=1)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=4, column=1, padx=(5, 100), pady=(200, 5), sticky="se", rowspan=3)
pane_quit = ttk.Frame(panedOne)
panedOne.add(pane_quit, weight=1)

switch = ttk.Checkbutton(pane_switch, text="Light Mode", variable=varSwitch, command=themeSwitch, style="Switch")
switch.pack(side="top", fill="none", anchor="e", pady=(5, 5), padx=(0, 0))

labelLogin = ttk.Label(pane_login, text="User Login Status!", foreground="green", font=("Consolas", 12, "bold"))
labelLogin.pack(side="top", fill="none", anchor="nw", pady=(5, 5), padx=(0, 0))

labelKeyboard = ttk.Label(pane_keyboard, text="Keyboard", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(100, 150))
userInput = ttk.Entry(pane_keyboard, textvariable=varEntry, font=('segoe UI', 15, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 5), padx=(100, 150))
buttonSend = ttk.Button(pane_keyboard, text="SEND", command=keyboardCommand).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(100, 150))

labelSmokeSensor = ttk.Label(pane_smoke, text="Smoke Sensor (ppm)", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(150, 100))
labelSmokeSensorValue = ttk.Label(pane_smoke, textvariable=smokeSensorValue, foreground="green", font=("segoe UI", 35, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(150, 100))
labelSmokeThreshold = ttk.Label(pane_smoke, textvariable=smokeSensorTValue, foreground="green", font=("segoe UI", 12, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(150, 100))
smokeSensorTValue.set("Smoke Threshold: " + str(MQ2_THRESHOLD) + " ppm")

ttk.Separator(pane_SeparatorOne, orient="horizontal").pack(fill="x", expand=True)
ttk.Separator(pane_SeparatorTwo, orient="horizontal").pack(fill="x", expand=True)

lightingLabel = ttk.Label(pane_lighting, text="Lighting Setting", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(0, 5), padx=(100, 150))
rbOn = ttk.Radiobutton(pane_lighting, text="ON", variable=varLight, command= lightSwitch, value=1).pack(side="top", fill="none", anchor="nw", pady=(5, 5), padx=(100, 150))
rbOff = ttk.Radiobutton(pane_lighting, text="OFF", variable=varLight, command= lightSwitch, value=0).pack(side="top", fill="none", anchor="nw", pady=(5, 5), padx=(100, 150))

rb = ttk.Radiobutton(pane_lighting, text="WHITE", variable=varRadio, command=lightColor, value=0).pack(side="left", fill="none", anchor="w", pady=(5, 0), padx=(5, 5))
rb1 = ttk.Radiobutton(pane_lighting, text="RED", variable=varRadio, command=lightColor, value=1).pack(side="left", fill="none", anchor="w", pady=(5, 0), padx=(5, 5))
rb2 = ttk.Radiobutton(pane_lighting, text="GREEN", variable=varRadio, command=lightColor, value=2).pack(side="left", fill="none", anchor="w", pady=(5, 0), padx=(5, 5))
rb3 = ttk.Radiobutton(pane_lighting, text="BLUE", variable=varRadio, command=lightColor, value=3).pack(side="left", fill="none", anchor="w", pady=(5, 0), padx=(5, 5))

labelThershold = ttk.Label(pane_intensity, text="Light Intensity", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(0, 10), padx=(50, 100))
s1 = TickScale(pane_intensity, variable=varIntensity, orient='horizontal', from_=1, to=3, tickinterval=1, resolution=1, length=250).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(50, 100))
varIntensity.set(3)
buttonSet = ttk.Button(pane_intensity, text="SET", command=lightIntensity).pack(side="top", fill="none", anchor="center", pady=(5, 0), padx=(50, 100))

ttk.Label(pane_voice, text="Console", font=("Consolas", 20, "bold")).pack(side="top", fill="both")
listbox = tk.Listbox(pane_voice, background="white", foreground="black", width=42, height=5, font=18)
listbox.pack(side="left", fill="both")

scrollbar = ttk.Scrollbar(pane_voice)
scrollbar.pack(side="left", fill="both")
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
buttonSet = ttk.Button(pane_voice, text="Clear", command=clearConsoleOne).pack(side="bottom", fill="none", anchor="s", padx=(5,0))

labelExit = ttk.Label(pane_quit, text="Close User Interface", font=("segoe UI", 12, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 10))
buttonExit = ttk.Button(pane_quit, text="QUIT!", command=cancel).pack(side="top", fill="none", anchor="center", pady=(5, 5))

window.withdraw()
micReady()

t0 = Thread(target=login)
t0.daemon = True
t0.start()

t1 = Thread(target = voiceCommand)
t1.daemon = True
t1.start()

t2 = Thread(target = sendMQ2Data)
t2.daemon = True
t2.start()

t3 = Thread(target = continuosUpdateSmokeSensorValue)
t3.daemon = True
t3.start()

t4 = Thread(target=hint)
t4.daemon = True
t4.start()

t5 = Thread(target=admin)
t5.daemon = True
t5.start()

window.mainloop()