import tkinter as tk
from tkinter import ttk
import random
import time
from threading import Thread
from ttkwidgets import TickScale
import sys

tries = 3
triesY_axis = 370
triesColor = "orange"


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
        my_canvas.create_text(190, triesY_axis, text=f"Wrong username/password combination! Tries left: {tries}", fill=triesColor, font=("segoe UI", 12))
        triesY_axis += 20
        triesColor = "red"
        if tries == 0:
            cancel()


def login():
    loginWindow.lift()
    loginWindow.focus_force()
    my_canvas.create_text(140, 20, text="Please Login for full access!", fill="orange", font=("Consolas", 12))
    my_canvas.create_text(850, 200, text="     Team\nMellowship", fill="#1661DA", font=("segoe UI", 32, 'bold'))
    my_canvas.create_text(850, 350, text="Li-Fi SYSTEM", fill="#15E8F3", font=("segoe UI", 32, 'bold'))
    my_canvas.create_text(140, 100, text="Username", fill="white", font=("Consolas", 20, "bold"))
    my_canvas.create_text(140, 220, text="Password", fill="white", font=("Consolas", 20, "bold"))
    InputLoginUser = ttk.Entry(loginWindow, textvariable=varUsername, font=('segoe UI', 15, 'bold')).place(x=70, y=150)
    InputLoginPass = ttk.Entry(loginWindow, textvariable=varPassword, show="*", font=('segoe UI', 15, 'bold')).place(x=70, y=270)
    buttonSendLogin = ttk.Button(loginWindow, text="Login", command=loginValidate).place(x=100, y=320)
    buttonSendLogin = ttk.Button(loginWindow, text="Cancel", command=cancel).place(x=200, y=320)
    loginWindow.update()


def admin():
    global labelLoginAdmin
    labelLoginAdmin = ttk.Label(tab3, text="User Login Status!", foreground="green", font=("Consolas", 12, "bold"))
    labelLoginAdmin.place(x=5, y=10)
    ttk.Label(tab3, text="Login into Admin for full access!", foreground="orange", font=("Consolas", 16, "bold")).place(x=10, y=50)
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
    panedAdminFirst.grid(row=1, column=0, pady=(5, 30), sticky="nw", rowspan=3)
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
    panedThree.grid(row=2, column=0, pady=(220, 5), sticky="n", rowspan=3)
    pane_SeparatorThree = ttk.Frame(panedThree, width=512, height=50)
    panedThree.add(pane_SeparatorThree, weight=1)
    pane_SeparatorThree.pack_propagate(False)
    panedFour = ttk.PanedWindow(tab3)
    panedFour.grid(row=2, column=1, pady=(220, 5), sticky="n", rowspan=3)
    pane_SeparatorFour = ttk.Frame(panedFour, width=512, height=50)
    panedFour.add(pane_SeparatorFour, weight=1)
    pane_SeparatorFour.pack_propagate(False)

    panedAdminTwo = ttk.PanedWindow(tab3)
    panedAdminTwo.grid(row=3, column=0, pady=(250, 10), padx=(50, 100), sticky="n", rowspan=3)
    pane_light = ttk.Frame(panedAdminTwo, width=350, height=400)
    panedAdminTwo.add(pane_light, weight=1)
    # pane_light.pack_propagate(False)

    panedOne = ttk.PanedWindow(tab3)
    panedOne.grid(row=3, column=1, pady=(250, 5), sticky="n", rowspan=3)
    pane_console = ttk.Frame(panedOne)
    panedOne.add(pane_console, weight=1)

    # Adding label and a Listbox for console
    ttk.Label(pane_console, text="Console", font=("Consolas", 20, "bold")).pack(side="top", fill="none", anchor="nw")
    butt = ttk.Button(pane_console, text="CLEAR", command=clearConsole)
    butt.pack(side="bottom", fill="none", pady=(4, 0))
    butt1 = ttk.Button(pane_console, text="CHECK", command=checkList)
    butt1.pack(side="top", fill="none", pady=(0, 4))
    global listbox
    listbox = tk.Listbox(pane_console, background="white", foreground="black", width=40, height=6, font=("Consolas", 15, "bold"))
    listbox.pack(side="left", fill="both")
    listbox.insert("end", "Test all peripherals: 'CHECK' button")
    listbox.itemconfig(0, {'fg': 'orange'})
    listbox.insert("end", "------------------------------------------------------------")
    # Adding a Scrollbar to the listbox
    scrollbar = ttk.Scrollbar(pane_console)
    scrollbar.pack(side="left", fill="both")
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # panedAdminFour = ttk.PanedWindow(tab3)
    # panedAdminFour.grid(row=3, column=2, padx=(315, 5), pady=(462, 5), sticky="n", rowspan=3)
    # pane_quitAdmin = ttk.Frame(panedAdminFour, width=200, height=90)
    # panedAdminFour.add(pane_quitAdmin, weight=1)
    # pane_quitAdmin.pack_propagate(False)

    labelLoginAdmin = ttk.Label(panedAdminLogin, text="ADMIN Logged in!", foreground="green", font=("Consolas", 12, "bold"))
    labelLoginAdmin.pack(side="top", fill="both", anchor="w", pady=(5, 5), padx=(5, 5))

    ttk.Label(pane_smokeThershold, text="Smoke Thershold", font=("Consolas", 20, "bold")).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(5, 5))
    TickScale(pane_smokeThershold, variable=v1, orient='horizontal', from_=0, to=1.5, tickinterval=0.5, resolution=0.1, length=250).pack(side="top", fill="none", anchor="center", pady=(5, 5), padx=(5, 5))
    v1.set(0.8)
    ttk.Button(pane_smokeThershold, text="SET", command=doStuff).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(5, 5))

    ttk.Label(pane_lifiThershold, text="Light Thershold", font=("Consolas", 20, "bold")).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(5, 5))
    TickScale(pane_lifiThershold, variable=v1, orient='horizontal', from_=0, to=3, tickinterval=1, resolution=0.1, length=250).pack(side="top", fill="none", anchor="center", pady=(5, 5), padx=(5, 5))
    v3.set(2)
    ttk.Button(pane_lifiThershold, text="SET", command=doStuff).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(5, 5))

    ttk.Separator(pane_SeparatorThree, orient="horizontal").pack(fill="x", expand=True)
    ttk.Separator(pane_SeparatorFour, orient="horizontal").pack(fill="x", expand=True)

    ttk.Label(pane_light, text="Light Switch", font=("Consolas", 20, "bold")).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(5, 5))
    ttk.Radiobutton(pane_light, text="ON", variable=b, value=1).pack(side="top", fill="none", anchor="nw", pady=(5, 5), padx=(100, 5))
    ttk.Radiobutton(pane_light, text="OFF", variable=b, value=0).pack(side="top", fill="none", anchor="nw", pady=(5, 10), padx=(100, 5))

    ttk.Label(tab3, text="Close User Interface", font=("segoe UI", 12, 'bold')).place(x=851, y=468)
    ttk.Button(tab3, text="QUIT!", command=cancel).place(x=880, y=505)


def checkList():
    listbox.insert("end", "Microphone Check:")
    listbox.yview("end")
    listbox.insert("end", "     Passed")
    listbox.yview("end")
    listbox.itemconfig("end", {'fg': 'green'})

    listbox.insert("end", "Smoke Sensor Check:")
    listbox.yview("end")
    checkSmoke()
    listbox.insert("end", "LED light Check:")
    listbox.yview("end")

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
    listbox.insert("end", "     Passed")
    listbox.itemconfig("end", {'fg': 'green'})
    listbox.insert("end", "------------------------------------------------------------")
    listbox.yview("end")
    popupWindow.destroy()


def LEDCheckNo():
    listbox.insert("end", "     Failed")
    listbox.itemconfig("end", {'fg': 'red'})
    listbox.insert("end", "------------------------------------------------------------")
    listbox.yview("end")
    popupWindow.destroy()


def checkSmoke():
    if (var.get() > "0.1") and (var.get() < "2") and (var.get() != "0"):
        listbox.insert("end", "     Passed")
        listbox.itemconfig("end", {'fg': 'green'})
        listbox.insert("end", f"     With value of {var.get()}V")
        listbox.yview("end")
    else:
        listbox.insert("end", "     Failed")
        listbox.itemconfig("end", {'fg': 'red'})
        listbox.insert("end", f"     With value of {var.get()}V")
        listbox.yview("end")


# Clears the Console's screen
def clearConsole():
    listbox.delete(0, "end")
    listbox.insert("end", "Test all peripherals: 'CHECK' button")
    listbox.itemconfig(0, {'fg': 'orange'})
    listbox.insert("end", "------------------------------------------------------------")


def deletetab():
    for item in window.winfo_children():
        if str(item) == (window.select()):
            item.destroy()
            return


def cancel():
    window.destroy()
    sys.exit()


def hint():
    ttk.Label(tab2, text="Valid Commands", foreground="forest green", font=("segoe UI", 38, "bold")).grid(row=0, column=0, sticky="n", padx=(20, 0))
    ttk.Label(tab2, text="hello, clear, time", font=("Consolas", 20)).grid(row=1, column=0, sticky="n")
    ttk.Label(tab2, text="Smoke", font=("Consolas", 20)).grid(row=2, column=0, sticky="n")
    ttk.Label(tab2, text="Temperature", font=("Consolas", 20)).grid(row=3, column=0, sticky="n")
    ttk.Label(tab2, text="Humidity", font=("Consolas", 20)).grid(row=4, column=0, sticky="n")
    ttk.Label(tab2, text="Pressure", font=("Consolas", 20)).grid(row=5, column=0, sticky="n")
    ttk.Label(tab2, text="Open", font=("Consolas", 20)).grid(row=6, column=0, sticky="n")
    ttk.Label(tab2, text="Close", font=("Consolas", 20)).grid(row=7, column=0, sticky="n")
    ttk.Label(tab2, text="On", font=("Consolas", 20)).grid(row=8, column=0, sticky="n")
    ttk.Label(tab2, text="Off", font=("Consolas", 20)).grid(row=9, column=0, sticky="n")
    ttk.Label(tab2, text="RGB", font=("Consolas", 20)).grid(row=10, column=0, sticky="n")
    ttk.Label(tab2, text="Intensity \"%0-100\"", font=("Consolas", 20)).grid(row=11, column=0, sticky="n")

    ttk.Separator(tab2, orient="vertical").grid(row=0, column=1, rowspan=12, sticky='ns', padx=(100, 100))

    ttk.Label(tab2, text="Description", foreground="forest green", font=("segoe UI", 38, "bold")).grid(row=0, column=2, sticky="n")
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
    ttk.Label(tab2, text="Light intensity in %", font=("segoe UI", 20)).grid(row=11, column=2, sticky="n")
    tab2.update()


def doStuff():
    print("I did it")


def deletetab():
    for item in tabControl.winfo_children():
        if str(item) == (tabControl.select()):
            item.destroy()
            return


def smokeValue():
    while True:
        num = random.random()
        num = round(num, 4)
        var.set(str(round(num, 4)))
        time.sleep(0.3)


def themeSwitch():
    global themeTCL
    global themeFiles
    if v4.get() == 0:
        listbox.config(foreground="#313131", background="white")
        switch.config(text="Light Mode")
        window_style.theme_use("forest-light")
    elif v4.get() == 1:
        listbox.config(foreground="white", background="#313131")
        switch.config(text="Dark Mode")
        window_style.theme_use("forest-dark")


imageIcon = r"C:\Users\abtin\OneDrive\Documents\Projects\Recognition\Recognition\Images\bulbIcon.ico"
imagebg = r"C:\Users\abtin\OneDrive\Documents\Projects\Recognition\Recognition\Images\NASA_1_1024x600.png"

window = tk.Tk()
window.title("TRANSMITTER")
tabControl = ttk.Notebook(window)
window.geometry("1024x600")
window.iconbitmap(imageIcon)

window.tk.call("source", "forest-light.tcl")
window.tk.call("source", "forest-dark.tcl")

window_style = ttk.Style(window)
window_style.theme_use("forest-light")

x_cordinate = int((window.winfo_screenwidth()/2) - (window.winfo_width()/2))
y_cordinate = int((window.winfo_screenheight()/2) - (window.winfo_height()/2))
window.geometry("+{}+{}".format(x_cordinate, y_cordinate))

loginWindow = tk.Toplevel(window)
loginWindow.title("LOGIN")
loginWindow.geometry("1024x600")
loginWindow.iconbitmap(imageIcon)

x_cordinate = int((loginWindow.winfo_screenwidth()/2) - (loginWindow.winfo_width()/2))
y_cordinate = int((loginWindow.winfo_screenheight()/2) - (loginWindow.winfo_height()/2))
loginWindow .geometry("+{}+{}".format(x_cordinate, y_cordinate))

bg = tk.PhotoImage(file=imagebg)
my_canvas = tk.Canvas(loginWindow, width=1024, height=600)
my_canvas.pack(fill="both", expand=True)
my_canvas.create_image(0, 0, image=bg, anchor="nw")

global var
var = tk.StringVar()
var.set("N/A")
v1 = tk.DoubleVar()
v2 = tk.DoubleVar()
v3 = tk.DoubleVar()
v4 = tk.IntVar()
v4.set(0)
varEntry = tk.StringVar()
varEntry.set("")

username = "admin"
password = "admin"
usernameAdmin = "admin"
passwordAdmin = "password"
varUsername = tk.StringVar()
varUsername.set("admin")
varPassword = tk.StringVar()
varPassword.set("admin")
varUsernameAdmin = tk.StringVar()
varUsernameAdmin.set("admin")
varPasswordAdmin = tk.StringVar()
varPasswordAdmin.set("password")

r = tk.IntVar()
b = tk.IntVar()

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tabControl.add(tab1, text='MAIN SCREEN')
tabControl.add(tab2, text='HELP SCREEN')
tabControl.add(tab3, text='ADMIN')
tabControl.pack(expand=1, fill="both")

panedZero = ttk.PanedWindow(tab1)
panedZero.grid(row=0, column=1, padx=(0, 10), pady=(5, 30), sticky="e", rowspan=3)
pane_switch = ttk.Frame(panedZero, width=130, height=208)
panedZero.add(pane_switch, weight=1)
pane_switch.pack_propagate(False)

paned = ttk.PanedWindow(tab1)
paned.grid(row=0, column=0, pady=(5, 30), sticky="n", rowspan=3)
pane_login = ttk.Frame(paned, width=512, height=208)
paned.add(pane_login, weight=1)
pane_login.pack_propagate(False)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=1, column=0, pady=(5, 50), sticky="n", rowspan=3)
pane_keyboard = ttk.Frame(panedOne)
panedOne.add(pane_keyboard, weight=1)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=1, column=1, pady=(5, 50), sticky="n", rowspan=3)
pane_smoke = ttk.Frame(panedOne)
panedOne.add(pane_smoke, weight=1)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=2, column=0, pady=(100, 100), sticky="n", rowspan=3)
pane_SeparatorOne = ttk.Frame(panedOne, width=512)
panedOne.add(pane_SeparatorOne, weight=1)
pane_SeparatorOne.pack_propagate(False)
panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=2, column=1, pady=(100, 100), sticky="n", rowspan=3)
pane_SeparatorTwo = ttk.Frame(panedOne, width=512)
panedOne.add(pane_SeparatorTwo, weight=1)
pane_SeparatorTwo.pack_propagate(False)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=3, column=0, pady=(5, 50), sticky="n", rowspan=3)
pane_lighting = ttk.Frame(panedOne)
panedOne.add(pane_lighting, weight=1)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=3, column=1, pady=(5, 50), sticky="n", rowspan=3)
pane_intensity = ttk.Frame(panedOne)
panedOne.add(pane_intensity, weight=1)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=4, column=1, padx=(5, 20), pady=(220, 5), sticky="se", rowspan=3)
pane_quit = ttk.Frame(panedOne)
panedOne.add(pane_quit, weight=1)

switch = ttk.Checkbutton(pane_switch, text="Light Mode", variable=v4, command=themeSwitch, style="Switch")
switch.pack(side="top", fill="both", anchor="e", pady=(5, 5), padx=(5, 5))

labelLogin = ttk.Label(pane_login, text="User Login Status!", foreground="green", font=("Consolas", 12, "bold"))
labelLogin.pack(side="top", fill="both", anchor="w", pady=(5, 5), padx=(5, 5))

labelKeyboard = ttk.Label(pane_keyboard, text="Keyboard", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(100, 150))
userInput = ttk.Entry(pane_keyboard, textvariable=varEntry, font=('segoe UI', 15, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 5), padx=(100, 150))
buttonSend = ttk.Button(pane_keyboard, text="SEND", command=doStuff).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(100, 150))

labelSmokeSensor = ttk.Label(pane_smoke, text="Smoke Sensor", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(150, 100))
labelSmokeSensorValue = ttk.Label(pane_smoke, textvariable=var, foreground="green", font=("segoe UI", 35, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(150, 100))

ttk.Separator(pane_SeparatorOne, orient="horizontal").pack(fill="x", expand=True)
ttk.Separator(pane_SeparatorTwo, orient="horizontal").pack(fill="x", expand=True)

lightingLabel = ttk.Label(pane_lighting, text="Lighting Setting", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(100, 150))
rbOn = ttk.Radiobutton(pane_lighting, text="ON", variable=b, value=1).pack(side="top", fill="none", anchor="nw", pady=(5, 5), padx=(100, 150))
rbOff = ttk.Radiobutton(pane_lighting, text="OFF", variable=b, value=0).pack(side="top", fill="none", anchor="nw", pady=(5, 5), padx=(100, 150))

rb = ttk.Radiobutton(pane_lighting, text="WHITE", variable=r, value=0).pack(side="left", fill="none", anchor="w", pady=(5, 5), padx=(5, 5))
rb1 = ttk.Radiobutton(pane_lighting, text="RED", variable=r, value=1).pack(side="left", fill="none", anchor="w", pady=(5, 5), padx=(5, 5))
rb2 = ttk.Radiobutton(pane_lighting, text="GREEN", variable=r, value=2).pack(side="left", fill="none", anchor="w", pady=(5, 5), padx=(5, 5))
rb3 = ttk.Radiobutton(pane_lighting, text="BLUE", variable=r, value=3).pack(side="left", fill="none", anchor="w", pady=(5, 5), padx=(5, 5))

labelThershold = ttk.Label(pane_intensity, text="Light Intensity", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(150, 100))
s1 = TickScale(pane_intensity, variable=v2, orient='horizontal', from_=0, to=100, tickinterval=20, resolution=10, length=250).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(150, 100))
v2.set(0)
buttonSet = ttk.Button(pane_intensity, text="SET", command=doStuff).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(150, 100))

labelExit = ttk.Label(pane_quit, text="Close User Interface", font=("segoe UI", 12, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 10))
buttonExit = ttk.Button(pane_quit, text="QUIT!", command=cancel).pack(side="top", fill="none", anchor="center", pady=(5, 5))

t0 = Thread(target=admin).start()
t1 = Thread(target=login).start()
t2 = Thread(target=smokeValue)
t2.daemon = True
t2.start()
t3 = Thread(target=hint).start()

window.withdraw()
window.mainloop()
