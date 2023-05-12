import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import random
import time
from threading import Thread
from ttkwidgets import TickScale
import sys

tries = 3
triesY_axis = 370
triesColor = "orange"
global stopLoop
loopStart = True


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
    InputLoginUserAdmin = ttk.Entry(tab3, textvariable=varUsernameAdmin, font=('segoe UI', 15, 'bold')).place(x=70, y=150)
    InputLoginPassAdmin = ttk.Entry(tab3, textvariable=varPasswordAdmin, show="*", font=('segoe UI', 15, 'bold')).place(x=70, y=270)
    buttonSendLogin = ttk.Button(tab3, text="Login", command=loginValidateAdmin).place(x=150, y=320)
    loginWindow.update()


def adminLogged():
    panedAdminFirst = ttk.PanedWindow(tab3)
    panedAdminFirst.grid(row=1, column=0, pady=(5, 30), sticky="nw", rowspan=3)
    panedAdminLogin = tk.Frame(panedAdminFirst, highlightbackground="dark green", highlightthickness=0, width=350, height=40)
    panedAdminFirst.add(panedAdminLogin, weight=1)
    panedAdminLogin.pack_propagate(False)

    panedAdmin = ttk.PanedWindow(tab3)
    panedAdmin.grid(row=1, column=0, pady=(50, 100), padx=(40, 50), sticky="n", rowspan=3)
    pane_smokeThershold = tk.Frame(panedAdmin, highlightbackground="dark green", highlightthickness=0, width=350, height=200)
    panedAdmin.add(pane_smokeThershold, weight=1)
    pane_smokeThershold.pack_propagate(False)

    panedAdminOne = ttk.PanedWindow(tab3)
    panedAdminOne.grid(row=1, column=1, pady=(50, 100), padx=(50, 40), sticky="n", rowspan=3)
    pane_lifiThershold = tk.Frame(panedAdminOne, highlightbackground="dark green", highlightthickness=0, width=350, height=200)
    panedAdminOne.add(pane_lifiThershold, weight=1)
    pane_lifiThershold.pack_propagate(False)

    panedThree = ttk.PanedWindow(tab3)
    panedThree.grid(row=2, column=0, pady=(250, 100), sticky="n", rowspan=3)
    pane_SeparatorThree = tk.Frame(panedThree, highlightbackground="dark green", highlightthickness=0, width=512, height=50)
    panedThree.add(pane_SeparatorThree, weight=1)
    pane_SeparatorThree.pack_propagate(False)
    panedFour = ttk.PanedWindow(tab3)
    panedFour.grid(row=2, column=1, pady=(250, 100), sticky="n", rowspan=3)
    pane_SeparatorFour = tk.Frame(panedFour, highlightbackground="dark green", highlightthickness=0, width=512, height=50)
    panedFour.add(pane_SeparatorFour, weight=1)
    pane_SeparatorFour.pack_propagate(False)

    panedAdminTwo = ttk.PanedWindow(tab3)
    panedAdminTwo.grid(row=3, column=0, pady=(320, 10), padx=(50, 100), sticky="n", rowspan=3)
    pane_light = tk.Frame(panedAdminTwo, highlightbackground="dark green", highlightthickness=0, width=350, height=150)
    panedAdminTwo.add(pane_light, weight=1)
    pane_light.pack_propagate(False)

    panedAdminFour = ttk.PanedWindow(tab3)
    panedAdminFour.grid(row=3, column=1, padx=(315, 5), pady=(462, 5), sticky="n", rowspan=3)
    pane_quitAdmin = tk.Frame(panedAdminFour, highlightbackground="dark green", highlightthickness=0, width=200, height=90)
    panedAdminFour.add(pane_quitAdmin, weight=1)
    pane_quitAdmin.pack_propagate(False)

    labelLoginAdmin = ttk.Label(panedAdminLogin, text="ADMIN Logged in!", foreground="green", font=("Consolas", 12, "bold"))
    labelLoginAdmin.pack(side="top", fill="both", anchor="w", pady=(5, 5), padx=(5, 5))

    ttk.Label(pane_smokeThershold, text="Smoke Thershold", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(5, 5))
    TickScale(pane_smokeThershold, variable=v1, orient='horizontal', from_=0, to=1.5, tickinterval=0.5, resolution=0.1, length=250).pack(side="top", fill="none", anchor="center", pady=(5, 5), padx=(5, 5))
    v1.set(0.8)
    ttk.Button(pane_smokeThershold, text="SET", command=doStuff).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(5, 5))

    ttk.Label(pane_lifiThershold, text="Light Thershold", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(5, 5))
    TickScale(pane_lifiThershold, variable=v1, orient='horizontal', from_=0, to=3, tickinterval=1, resolution=0.1, length=250).pack(side="top", fill="none", anchor="center", pady=(5, 5), padx=(5, 5))
    v3.set(2)
    ttk.Button(pane_lifiThershold, text="SET", command=doStuff).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(5, 5))

    ttk.Separator(pane_SeparatorThree, orient="horizontal").pack(fill="x", expand=True)
    ttk.Separator(pane_SeparatorFour, orient="horizontal").pack(fill="x", expand=True)

    ttk.Label(pane_light, text="Light Switch", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(5, 5))
    ttk.Radiobutton(pane_light, text="ON", variable=b, value=1).pack(side="top", fill="none", anchor="nw", pady=(5, 5), padx=(100, 5))
    ttk.Radiobutton(pane_light, text="OFF", variable=b, value=0).pack(side="top", fill="none", anchor="nw", pady=(5, 10), padx=(100, 5))

    ttk.Label(pane_quitAdmin, text="Close User Interface", font=("segoe UI", 12, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 10))
    ttk.Button(pane_quitAdmin, text="QUIT!", command=cancel).pack(side="top", fill="none", anchor="center", pady=(5, 5))


def deletetab():
    for item in window.winfo_children():
        if str(item) == (window.select()):
            item.destroy()
            return


def cancel():
    loopStart = False
    window.destroy()
    sys.exit()


def hint():
    ttk.Label(tab2, text="Valid Commands", foreground="forest green", font=("segoe UI", 38, "bold")).grid(row=0, column=0, sticky="n", padx=(20, 0))
    ttk.Label(tab2, text="hello, clear, time", font=("segoe UI", 20)).grid(row=1, column=0, sticky="n")
    ttk.Label(tab2, text="Smoke", font=("segoe UI", 20)).grid(row=2, column=0, sticky="n")
    ttk.Label(tab2, text="Temperature", font=("segoe UI", 20)).grid(row=3, column=0, sticky="n")
    ttk.Label(tab2, text="Humidity", font=("segoe UI", 20)).grid(row=4, column=0, sticky="n")
    ttk.Label(tab2, text="Pressure", font=("segoe UI", 20)).grid(row=5, column=0, sticky="n")
    ttk.Label(tab2, text="Open", font=("segoe UI", 20)).grid(row=6, column=0, sticky="n")
    ttk.Label(tab2, text="Close", font=("segoe UI", 20)).grid(row=7, column=0, sticky="n")
    ttk.Label(tab2, text="On", font=("segoe UI", 20)).grid(row=8, column=0, sticky="n")
    ttk.Label(tab2, text="Off", font=("segoe UI", 20)).grid(row=9, column=0, sticky="n")
    ttk.Label(tab2, text="RGB", font=("segoe UI", 20)).grid(row=10, column=0, sticky="n")
    ttk.Label(tab2, text="Intensity \"%0-100\"", font=("segoe UI", 20)).grid(row=11, column=0, sticky="n")

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
    while loopStart:
        num = random.random()
        num = round(num, 4)
        var.set(str(round(num, 4)))
        time.sleep(0.3)


window = tk.Tk()
# window = ThemedTk(themebg=True)
# window.set_theme("breeze")
window.title("TRANSMITTER")
tabControl = ttk.Notebook(window)
window.geometry("1024x600")
window.iconbitmap(r"C:\Users\abtin\OneDrive\Documents\Projects\Recognition\Recognition\Images\bulbIcon.ico")

window.tk.call('source', 'forest-light.tcl')
ttk.Style().theme_use('forest-light')

x_cordinate = int((window.winfo_screenwidth()/2) - (window.winfo_width()/2))
y_cordinate = int((window.winfo_screenheight()/2) - (window.winfo_height()/2))
window.geometry("+{}+{}".format(x_cordinate, y_cordinate))

loginWindow = tk.Toplevel(window)
loginWindow.title("LOGIN")
loginWindow.geometry("1024x600")
loginWindow.iconbitmap(r"C:\Users\abtin\OneDrive\Documents\Projects\Recognition\Recognition\Images\bulbIcon.ico")

x_cordinate = int((loginWindow.winfo_screenwidth()/2) - (loginWindow.winfo_width()/2))
y_cordinate = int((loginWindow.winfo_screenheight()/2) - (loginWindow.winfo_height()/2))
loginWindow .geometry("+{}+{}".format(x_cordinate, y_cordinate))

bg = tk.PhotoImage(file=r"C:\Users\abtin\OneDrive\Documents\Projects\Recognition\Recognition\Images\NASA_1_1024x600.png")
my_canvas = tk.Canvas(loginWindow, width=1024, height=600)
my_canvas.pack(fill="both", expand=True)
my_canvas.create_image(0, 0, image=bg, anchor="nw")

global var
var = tk.StringVar()
var.set("N/A")
v1 = tk.DoubleVar()
v2 = tk.DoubleVar()
v3 = tk.DoubleVar()
varEntry = tk.StringVar()
varEntry.set("")

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

r = tk.IntVar()
b = tk.IntVar()

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tabControl.add(tab1, text='MAIN SCREEN')
tabControl.add(tab2, text='HELP SCREEN')
tabControl.add(tab3, text='ADMIN')
tabControl.pack(expand=1, fill="both")

paned = ttk.PanedWindow(tab1)
paned.grid(row=0, column=0, pady=(5, 30), sticky="n", rowspan=3)
pane_login = ttk.Frame(paned, width=512, height=208)
paned.add(pane_login, weight=1)
pane_login.pack_propagate(False)

panedOne = ttk.PanedWindow(tab1)
panedOne.grid(row=1, column=0, pady=(5, 50), sticky="n", rowspan=3)
pane_keyboard = ttk.Frame(panedOne)
panedOne.add(pane_keyboard, weight=1)

panedTwo = ttk.PanedWindow(tab1)
panedTwo.grid(row=1, column=1, pady=(5, 50), padx=(0, 1), sticky="n", rowspan=3)
pane_smoke = tk.Frame(panedTwo, highlightbackground="dark green", highlightthickness=0, width=250, height=208)
panedTwo.add(pane_smoke, weight=1)

panedThree = ttk.PanedWindow(tab1)
panedThree.grid(row=2, column=0, pady=(100, 100), sticky="n", rowspan=3)
pane_SeparatorOne = tk.Frame(panedThree, highlightbackground="dark green", highlightthickness=0, width=512)
panedThree.add(pane_SeparatorOne, weight=1)
pane_SeparatorOne.pack_propagate(False)
panedFour = ttk.PanedWindow(tab1)
panedFour.grid(row=2, column=1, pady=(100, 100), sticky="n", rowspan=3)
pane_SeparatorTwo = tk.Frame(panedFour, highlightbackground="dark green", highlightthickness=0, width=512)
panedFour.add(pane_SeparatorTwo, weight=1)
pane_SeparatorTwo.pack_propagate(False)

panedFive = ttk.PanedWindow(tab1)
panedFive.grid(row=3, column=0, pady=(5, 50), sticky="n", rowspan=3)
pane_lighting = tk.Frame(panedFive)
panedFive.add(pane_lighting, weight=1)

panedSix = ttk.PanedWindow(tab1)
panedSix.grid(row=3, column=1, pady=(5, 50), sticky="n", rowspan=3)
pane_intensity = tk.Frame(panedSix)
panedSix.add(pane_intensity, weight=1)

panedSeven = ttk.PanedWindow(tab1)
panedSeven.grid(row=4, column=1, padx=(5, 20), pady=(220, 5), sticky="se", rowspan=3)
pane_quit = tk.Frame(panedSeven)
panedSeven.add(pane_quit, weight=1)

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
