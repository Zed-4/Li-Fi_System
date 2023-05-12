import tkinter as tk
from tkinter import ttk
from ttkwidgets import TickScale
from threading import Thread
from random import *
import time
import sys
import pyttsx3
import adafruit_lps2x
import smbus
import RPi.GPIO as GPIO
import os
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import pygame
import neopixel

#Constants
LDR_THRESHOLD = 0.18
PERIOD = .02
TEMP_THRESHOLD = 40.00
DOOR_PIN_NO = 18

# Light
pixel_pin = board.D21
# The number of NeoPixels
num_pixels = 12
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB                                                               
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2
    , auto_write=False, pixel_order=ORDER
)
intensity = 50
percent = int((255*intensity)/100)
# Door Servo

GPIO.setmode(GPIO.BCM)

GPIO.setup(DOOR_PIN_NO,GPIO.OUT)
servo1 = GPIO.PWM(DOOR_PIN_NO,50)

servo1.start(0)

#Text To Voice
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("rate", 170)
engine.setProperty("voice", voices[44].id)

#Sound
pygame.mixer.init()
pygame.mixer.music.load("./LiFiSounds/SmokeAlert.wav")

#Temp, Pressure Sensor
i2c = board.I2C()
lps = adafruit_lps2x.LPS22(i2c)
time.sleep(1.0)

#Temp, Humidity Sensor
address = 0x38
i2cbus = smbus.SMBus(1)
time.sleep(0.5)
data = i2cbus.read_i2c_block_data(address, 0x71,1)
if ( data[0] | 0x08) == 0:
    print("Initialization error")

#ADC Setup
from adafruit_mcp3xxx.analog_in import AnalogIn
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22)
mcp = MCP.MCP3008(spi, cs)

#Channels of Smoke sensor and LDR
smokeChannel = AnalogIn(mcp, MCP.P0)
LDRChannel = AnalogIn(mcp, MCP.P1)

# Checks for user login credentials
def loginValidateAdmin():
    if (varUsernameAdmin.get() == usernameAdmin and varPasswordAdmin.get() == passwordAdmin):
        varUsernameAdmin.set("")
        varPasswordAdmin.set("")
        print("ADMIN Login successful!")
        deletetab()
        global tab2
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text='ADMIN')
        tabControl.select(tab2)
        adminLogged()
    else:
        ttk.Label(tab2, text="Wrong username/password combination!", foreground='red', font=("segoe UI", 12)).place(x=190, y=370)


# Admin page before loggin
def admin():
    global labelLoginAdmin
    labelLoginAdmin = ttk.Label(tab2, text="ADMIN Login Status!", foreground="red", font=("Consolas", 12, "bold"))
    labelLoginAdmin.place(x=5, y=10)
    ttk.Label(tab2, text="Login into Admin for full access!", foreground="orange", font=("Consolas", 16, "bold")).place(x=10, y=50)
    ttk.Label(tab2, text="This section is for adjusting", font=("segoe UI", 22, "bold")).place(x=450, y=190)
    ttk.Label(tab2, text="Admin privileged settings!", font=("segoe UI", 22, "bold")).place(x=450, y=230)
    ttk.Label(tab2, text="Username", font=("segoe UI", 20, "bold")).place(x=140, y=100)
    ttk.Label(tab2, text="Password", font=("segoe UI", 20, "bold")).place(x=140, y=220)
    ttk.Entry(tab2, textvariable=varUsernameAdmin, font=('segoe UI', 15, 'bold')).place(x=70, y=150)
    ttk.Entry(tab2, textvariable=varPasswordAdmin, show="*", font=('segoe UI', 15, 'bold')).place(x=70, y=270)
    ttk.Button(tab2, text="Login", command=loginValidateAdmin).place(x=150, y=320)


# Admin page after Logged in
def adminLogged():
    panedAdminFirst = ttk.PanedWindow(tab2)
    panedAdminFirst.grid(row=1, column=0, pady=(5, 30), sticky="nw", rowspan=3)
    panedAdminLogin = ttk.Frame(panedAdminFirst, width=350, height=40)
    panedAdminFirst.add(panedAdminLogin, weight=1)
    panedAdminLogin.pack_propagate(False)

    panedAdmin = ttk.PanedWindow(tab2)
    panedAdmin.grid(row=1, column=0, pady=(50, 100), padx=(40, 50), sticky="n", rowspan=3)
    pane_smokeThershold = ttk.Frame(panedAdmin, width=350, height=200)
    panedAdmin.add(pane_smokeThershold, weight=1)
    pane_smokeThershold.pack_propagate(False)

    panedAdminOne = ttk.PanedWindow(tab2)
    panedAdminOne.grid(row=1, column=1, pady=(50, 100), padx=(50, 40), sticky="n", rowspan=3)
    pane_lifiThershold = ttk.Frame(panedAdminOne, width=350, height=200)
    panedAdminOne.add(pane_lifiThershold, weight=1)
    pane_lifiThershold.pack_propagate(False)

    panedThree = ttk.PanedWindow(tab2)
    panedThree.grid(row=2, column=0, pady=(250, 100), sticky="ne", rowspan=3)
    pane_SeparatorThree = ttk.Frame(panedThree, width=512, height=50)
    panedThree.add(pane_SeparatorThree, weight=1)
    pane_SeparatorThree.pack_propagate(False)
    panedFour = ttk.PanedWindow(tab2)
    panedFour.grid(row=2, column=1, pady=(250, 100), sticky="nw", rowspan=3)
    pane_SeparatorFour = ttk.Frame(panedFour, width=512, height=50)
    panedFour.add(pane_SeparatorFour, weight=1)
    pane_SeparatorFour.pack_propagate(False)

    panedAdminTwo = ttk.PanedWindow(tab2)
    panedAdminTwo.grid(row=3, column=0, pady=(405, 5), padx=(50, 100), sticky="n", rowspan=3)
    pane_light = ttk.Frame(panedAdminTwo, width=350, height=150)
    panedAdminTwo.add(pane_light, weight=1)
    pane_light.pack_propagate(False)

    labelLoginAdmin = ttk.Label(panedAdminLogin, text="ADMIN Logged in!", foreground="green", font=("Consolas", 12, "bold"))
    labelLoginAdmin.pack(side="top", fill="both", anchor="w", pady=(5, 5), padx=(5, 5))

    ttk.Label(pane_lifiThershold, text="Receiver Threshold", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(5, 5))
    TickScale(pane_lifiThershold, variable=v1, orient='horizontal', from_=0, to=2, tickinterval=1, resolution=0.01, length=250).pack(side="top", fill="none", anchor="center", pady=(5, 5), padx=(5, 5))
    v1.set(2)
    ttk.Button(pane_lifiThershold, text="SET", command=adjustThreshold).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(5, 5))

    ttk.Separator(pane_SeparatorThree, orient="horizontal").pack(fill="x", expand=True)
    ttk.Separator(pane_SeparatorFour, orient="horizontal").pack(fill="x", expand=True)

    #ttk.Label(pane_quitAdmin1, text="Close User Interface", font=("segoe UI", 12, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 10))
    #ttk.Button(pane_quitAdmin1, text="QUIT!", command=cancel).pack(side="top", fill="none", anchor="center", pady=(5, 5))


# Deletes the Admin tab to initialize it
def deletetab():
    for item in tabControl.winfo_children():
        if str(item) == (tabControl.select()):
            item.destroy()
            return


# Closes the program. Used for Buttons
def cancel():
    window.destroy()
    sys.exit()


# Static print for Values. Replace it so it is dynamic real numbers
def randomValue():
    while True:
        num = uniform(55, 100)
        var.set(str((round(num, 2))) + "°")

        numOne = uniform(0, 100)
        varOne.set("%" + str((round(numOne, 1))))

        numTwo = uniform(0, 20)
        varTwo.set(str((round(numTwo, 2))) + " PSI")

        numThree = randint(0, 1)

        global varProgress
        numFour = randint(0, 100)
        varProgress.set(numFour)
        if numThree == 0:
            door = "Closed"
            labelColor.config(foreground="red")
        else:
            door = "Open"
            labelColor.config(foreground="green")
        varThree.set(str(door))
        pane_listValues.update_idletasks()
        time.sleep(0.8)
        break

# Static print for Values. Replace it so it is dynamic real numbers
def defaultValue():
    var.set("N/A" + "°")

    varOne.set("%" + "N/A")

    varTwo.set("N/A " + "PSI")

    global varProgress
    numFour = randint(0, 100)
    varProgress.set(numFour)

    door = "CLOSED"
    labelColor.config(foreground="red")
    varThree.set(str(door))
    pane_listValues.update_idletasks()

# Static print into console. Replace it with Transmitter sent requests
def loop():
    listbox.insert("end", "Transmission Started:")
    listbox.itemconfig(0, {'fg': 'green'})
#     for i in range(50):
#         listbox.insert("end", f"Hello, this is a test for scrollbar and size: Test #{i}")
#         time.sleep(0.2)


# Clears the Console's screen
def clearConsole():
    listbox.delete(0, "end")
    listbox.insert("end", "Transmission Started:")
    listbox.itemconfig(0, {'fg': 'green'})


# For test purposes for some buttons to work
# remove and replace with needed functions
def adjustThreshold():
    global LDR_THRESHOLD
    LDR_THRESHOLD = v1.get()
    print("Photodiode threshold: " + str(LDR_THRESHOLD))
    listbox.insert("end","Photodiode threshold: " + str(LDR_THRESHOLD))


# To switch between dark and light mode
def themeSwitch():
    global themeTCL
    global themeFiles
    if varTheme.get() == 0:
        listbox.config(foreground="#313131", background="white")
        switch.config(text="Light Mode")
        window_style.theme_use("forest-light")
    elif varTheme.get() == 1:
        listbox.config(foreground="white", background="#313131")
        switch.config(text="Dark Mode")
        window_style.theme_use("forest-dark")


def get_ldr():
    voltage = LDRChannel.voltage
    return True if voltage > LDR_THRESHOLD else False

def print_humidity():
    i2cbus.write_i2c_block_data(address,0xac,[0x33,0x00])
    time.sleep(0.1)
    data = i2cbus.read_i2c_block_data(address,0x71,7)

    Traw = ((data[3] & 0xf) << 16 ) + (data[4] << 8 ) + data[5]
    temperature = 200*float(Traw)/2**20 - 50

    Hraw = ((data[3] & 0xf0) >> 4 ) + (data[1] << 12 ) + ( data[2] << 4)
    humidity = 100*float(Hraw)/2**20
    
    print("Humidity: " + str(humidity) + '\n\n')
    listbox.insert("end","Humidity: " + str(round(humidity,2)) + '\n\n')
    varOne.set("%" + str(round(humidity,2)))
    engine.runAndWait()

def print_temp():
    print("Sensor 1 temperature: %.2f c" % lps.temperature)
    var.set(str(round(lps.temperature,2)) + "° C")
    listbox.insert("end","Sensor 1 temperature: %.2f c" + str(round(lps.temperature,2)))
    

def print_pressure():
    print("Sensor 1 pressure: %.2f hPa" % round(lps.pressure, 2))
    listbox.insert("end","Sensor 1 pressure: %.2f hPa" % round(lps.pressure, 2))
    varTwo.set(str(round(lps.pressure,2)) + "%.2f hPa")
    
def get_byte():
    ret = 0
    time.sleep(PERIOD*1.5)
    for i in range(0, 8):
        ret = ret | get_ldr() << i
        time.sleep(PERIOD)
    return ret

def open_door():
    angle = 0.0
    servo1.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)

def close_door():
    angle = 180.0
    servo1.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)

def print_byte(my_byte):
    if(chr(my_byte)) == 's':
        if(not pygame.mixer.music.get_busy()):
            pygame.mixer.music.load("./LiFiSounds/SmokeAlert.wav")
            pygame.mixer.music.play()
    elif(chr(my_byte)) == 't':
        engine.say("Reading Temperature")
        engine.runAndWait()
        print_temp()
        
    elif(chr(my_byte)) == 'h':
        engine.say("Reading Humidity")
        engine.runAndWait()
        print_humidity()
    elif(chr(my_byte)) == 'p':
        engine.say("Reading Air Pressure")
        engine.runAndWait()
        print_pressure()
    elif(chr(my_byte)) == 'o':
        engine.say("Opening Door")
        engine.runAndWait()
        open_door()
        labelColor.config(foreground="green")
        varThree.set("OPEN")
    elif(chr(my_byte)) == 'c':
        engine.say("Closing Door")
        engine.runAndWait()
        close_door()
        labelColor.config(foreground="red")
        varThree.set("CLOSED")
    elif(chr(my_byte)) == 'l':
        os.system('clear')
        print("Screen Cleared")
    elif(chr(my_byte)) == 'w':
        ring_white(percent)
        time.sleep(2)
    elif(chr(my_byte)) == 'r':
        ring_red(percent)
        time.sleep(2)
    elif(chr(my_byte)) == 'g':
        ring_green(percent)
        time.sleep(2)
    elif(chr(my_byte)) == 'b':
        ring_blue(percent)
        time.sleep(2)
    elif(chr(my_byte)) == 'f':
        ring_white(0)
        time.sleep(2)
    #print(chr(my_byte))

def print_byte2(my_byte):
    print(chr(my_byte))

def ring_white(x):
    pixels.fill((x,x,x))
    pixels.show()
    
def ring_red(x):
    pixels.fill((0,x,0))
    pixels.show()
    
def ring_green(x):
    pixels.fill((x, 0,0))
    pixels.show()
 
def ring_blue(x):
    pixels.fill((0, 0, x))
    pixels.show()
    
def ring_off():
    pixels.fill((0,0,0))
    pixels.show()
    
def calibrate_rcvr():
    voltage = LDRChannel.voltage
    LDR_THRESHOLD = voltage-0.025
    if (LDR_THRESHOLD<0):
        LDR_THRESHOLD=0
    listbox.insert("end","New Receiver Threshold: " + str(round(LDR_THRESHOLD,2)))
    

# Replace bulbicon.ico with bulbicon.xbm for raspberry pi
# update the path accordingly
imageIcon = "@/home/mellowship/Documents/LiFiProject/Receiver/Images/bulbIcon.xbm"

# Main Window Setup
window = tk.Tk()
window.title("RECEIVER")
tabControl = ttk.Notebook(window)
window.geometry("1024x600")
window.iconbitmap(imageIcon)

# Window Theme (forest-light.tcl and forest-dark.tcl)
# call the sources now and switching using CheckButton later
window.tk.call("source", "forest-light.tcl")
window.tk.call("source", "forest-dark.tcl")

# Initializing the starting theme .theme_use()
window_style = ttk.Style(window)
window_style.theme_use("forest-light")

# Variables
v1 = tk.DoubleVar()
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
varTheme = tk.IntVar()
varTheme.set(0)

# Centering the Main window on the screen
x_cordinate = int((window.winfo_screenwidth()/2) - (window.winfo_width()/2))
y_cordinate = int((window.winfo_screenheight()/2) - (window.winfo_height()/2))
window.geometry("+{}+{}".format(x_cordinate, y_cordinate))

# Adding Tabs to main window
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='MAIN SCREEN')
tabControl.add(tab2, text='ADMIN')
tabControl.pack(expand=1, fill="both")

# Making many smaller windows or "Panes"
# For elements such as Console, Sensors, and Values and etc... to sit inside
panedZero = ttk.PanedWindow(tab1)
panedZero.grid(row=0, column=2, padx=(0, 20), pady=(5, 5), sticky="ne", rowspan=3)
pane_switch = ttk.Frame(panedZero)
panedZero.add(pane_switch, weight=1)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=1, column=0, pady=(5, 5), sticky="n", rowspan=3)
pane_console = ttk.Frame(panedOne)
panedOne.add(pane_console, weight=1)

panedTwo = ttk.PanedWindow(tab1)
panedTwo.grid(row=1, column=1, pady=(5, 5), sticky="n", rowspan=3)
pane_list = ttk.Frame(panedTwo)
panedTwo.add(pane_list, weight=1)

panedThree = ttk.PanedWindow(tab1)
panedThree.grid(row=1, column=2, pady=(5, 5), sticky="nw", rowspan=3)
pane_listValues = ttk.Frame(panedThree)
panedThree.add(pane_listValues, weight=1)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=3, column=1, sticky="ne", rowspan=3)
pane_SeparatorOne = ttk.Frame(panedOne, width="250")
panedOne.add(pane_SeparatorOne, weight=1)
pane_SeparatorOne.pack_propagate(False)
panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=3, column=2, sticky="nw", rowspan=3)
pane_SeparatorTwo = ttk.Frame(panedOne, width="150")
panedOne.add(pane_SeparatorTwo, weight=1)
pane_SeparatorTwo.pack_propagate(False)

panedFour = ttk.PanedWindow(tab1)
panedFour.grid(row=3, column=1, padx=(60, 5), pady=(5, 5), sticky="n", rowspan=3)
pane_listProgress = ttk.Frame(panedFour)
panedFour.add(pane_listProgress, weight=1)

pane_Calibrate = ttk.Frame(panedFour, width=200, height=90)
panedFour.add(pane_Calibrate, weight=1)

# Adding label and a Listbox for console
ttk.Label(pane_console, text="Console", font=("Consolas", 20, "bold")).pack(side="top", fill="both")
listbox = tk.Listbox(pane_console, background="white", foreground="black", width=35, height=15, font=18)
listbox.pack(side="left", fill="both")

# Adding a Scrollbar to the listbox
scrollbar = ttk.Scrollbar(pane_console)
scrollbar.pack(side="left", fill="both")
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
buttonSet = ttk.Button(tab1, text="Clear", command=clearConsole).grid(row=4, column=0)

# CheckButton to toggle Light\Dark mode
switch = ttk.Checkbutton(pane_switch, text="Light Mode", variable=varTheme, command=themeSwitch, style="Switch")
switch.pack(side="top", fill="both", anchor="e", pady=(5, 5), padx=(5, 5))

# All the Labels for the panel on the right (Sensors)
ttk.Label(pane_list, text="Sensors", font=("Consolas", 20, "bold")).pack(side="top", fill="both")
ttk.Label(pane_list, text="temperature", font=("Consolas", 20)).pack(side="top", fill="both")
ttk.Label(pane_list, text="Humididty", font=("Consolas", 20)).pack(side="top", fill="both")
ttk.Label(pane_list, text="Pressure", font=("Consolas", 20)).pack(side="top", fill="both")
ttk.Label(pane_list, text="Door", font=("Consolas", 20, "bold")).pack(side="top", fill="both")
ttk.Label(pane_list, text="Status", font=("Consolas", 20)).pack(side="top", fill="both")

# Replace all these variables with real number counterparts
var = tk.StringVar()
varOne = tk.StringVar()
varTwo = tk.StringVar()
varThree = tk.StringVar()
varRcvr = tk.StringVar()
varProgress = tk.DoubleVar()
varProgress.set(0)

# All the Labels for the panel on the right (Values)
ttk.Label(pane_listValues, text="Values", font=("Consolas", 20, "bold")).pack(side="top", fill="both")
ttk.Label(pane_listValues, textvariable=var, foreground="green", font=("Consolas", 20)).pack(side="top", fill="both")
ttk.Label(pane_listValues, textvariable=varOne, foreground="green", font=("Consolas", 20)).pack(side="top", fill="both")
ttk.Label(pane_listValues, textvariable=varTwo, foreground="green", font=("Consolas", 20)).pack(side="top", fill="both")
ttk.Label(pane_listValues, text="", font=("Consolas", 20)).pack(side="top", fill="both")
labelColor = ttk.Label(pane_listValues, textvariable=varThree, font=("Consolas", 20))
labelColor.pack(side="top", fill="both")

# Screen Separators to seperate the elements for aesthetics
ttk.Separator(pane_SeparatorOne, orient="horizontal").pack(fill="x", expand=True)
ttk.Separator(pane_SeparatorTwo, orient="horizontal").pack(fill="x", expand=True)

# Light intensity + Progressbar
ttk.Label(pane_listProgress, text="Light Intensity", font=("Consolas", 20)).pack(side="top", fill="both")
ttk.Progressbar(pane_listProgress, value=45, variable=varProgress, mode="determinate").pack(side="top", fill="both")
rcvLabel = ttk.Label(pane_listProgress, textvariable=varRcvr, font=("Consolas", 20))
rcvLabel.pack(side="top", fill="both")
ttk.Button(pane_Calibrate, text="CALIBRATE", command=calibrate_rcvr).pack(side="top", fill="none", anchor="center", pady=(10,10))
# Quit button and Label for tab1
#ttk.Label(pane_quitAdmin, text="Close User Interface", font=("segoe UI", 12, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 10))
#ttk.Button(pane_quitAdmin, text="QUIT!", command=cancel).pack(side="top", fill="none", anchor="center", pady=(10, 10))


def lightBar():
    while True:
        voltage = LDRChannel.voltage
        percent = (voltage/1.5) * 100
        varProgress.set(percent)
        varRcvr.set(str(round(LDRChannel.voltage,3)) + " V")
        time.sleep(.5)

# Thread for the loop to work with the main window loop
# ".daemon" needed if other while loops inflict with "mainloop()"
t = Thread(target=admin).start()
t1 = Thread(target=loop)
t1.daemon = True
t1.start()
t2 = Thread(target=defaultValue)
t2.daemon = True
t2.start()
t3 = Thread(target=lightBar)
t3.daemon = True
t3.start()



def mainRcvr():
    first = True
    while True:
        current_state = get_ldr()
        if (first):
            previous_state = current_state
            first = False
        if ((current_state != previous_state)):
            #print_byte(get_byte())
            print_byte(get_byte())
        previous_state = current_state
        if ( lps.temperature > TEMP_THRESHOLD and not pygame.mixer.music.get_busy()):
            pygame.mixer.music.load("./LiFiSounds/TemperatureSensorAlert.wav")
            pygame.mixer.music.play()
#      print('Raw ADC Value: ', smokeChannel.value)
#      if(float(str(smokeChannel.voltage)) > 1.0 and not pygame.mixer.music.get_busy()):
#         pygame.mixer.music.play()
#      print('LDR Reading: ' + str(LDRChannel.voltage) + 'V')
#      time.sleep(0.1)

main_thread = Thread(target=mainRcvr)
main_thread.start()
window.mainloop()
