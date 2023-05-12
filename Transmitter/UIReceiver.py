import tkinter as tk
from tkinter import ttk
from ttkwidgets import TickScale
from threading import Thread
from random import *
import time
import sys


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

    panedAdminFour = ttk.PanedWindow(tab2)
    panedAdminFour.grid(row=3, column=1, padx=(315, 5), pady=(473, 5), sticky="n", rowspan=3)
    pane_quitAdmin = ttk.Frame(panedAdminFour, width=200, height=90)
    panedAdminFour.add(pane_quitAdmin, weight=1)
    pane_quitAdmin.pack_propagate(False)

    labelLoginAdmin = ttk.Label(panedAdminLogin, text="ADMIN Logged in!", foreground="green", font=("Consolas", 12, "bold"))
    labelLoginAdmin.pack(side="top", fill="both", anchor="w", pady=(5, 5), padx=(5, 5))

    ttk.Label(pane_lifiThershold, text="Light Thershold", font=("segoe UI", 20)).pack(side="top", fill="none", anchor="center", pady=(10, 5), padx=(5, 5))
    TickScale(pane_lifiThershold, variable=v1, orient='horizontal', from_=0, to=3, tickinterval=1, resolution=0.1, length=250).pack(side="top", fill="none", anchor="center", pady=(5, 5), padx=(5, 5))
    v1.set(2)
    ttk.Button(pane_lifiThershold, text="SET", command=doStuff).pack(side="top", fill="none", anchor="center", pady=(5, 10), padx=(5, 5))

    ttk.Separator(pane_SeparatorThree, orient="horizontal").pack(fill="x", expand=True)
    ttk.Separator(pane_SeparatorFour, orient="horizontal").pack(fill="x", expand=True)

    ttk.Label(pane_quitAdmin, text="Close User Interface", font=("segoe UI", 12, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 10))
    ttk.Button(pane_quitAdmin, text="QUIT!", command=cancel).pack(side="top", fill="none", anchor="center", pady=(5, 5))


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


# Static print into console. Replace it with Transmitter sent requests
def loop():
    listbox.insert("end", "Transmission Started:")
    listbox.itemconfig(0, {'fg': 'green'})
    for i in range(50):
        listbox.insert("end", f"Hello, this is a test for scrollbar and size: Test #{i}")
        time.sleep(0.2)


# Clears the Console's screen
def clearConsole():
    listbox.delete(0, "end")
    listbox.insert("end", "Transmission Started:")
    listbox.itemconfig(0, {'fg': 'green'})


# For test purposes for some buttons to work
# remove and replace with needed functions
def doStuff():
    print("Whatever you pressed works!")


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


# Replace bulbicon.ico with bulbicon.xbm for raspberry pi
# update the path accordingly
imageIcon = r"G:\Files\Projects\Recognition\Recognition\Images\bulbIcon.ico"

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

panedAdminFour = ttk.PanedWindow(tab1)
panedAdminFour.grid(row=4, column=2, padx=(160, 5), pady=(140, 5), sticky="ne", rowspan=3)
pane_quitAdmin = ttk.Frame(panedAdminFour, width=200, height=90)
panedAdminFour.add(pane_quitAdmin, weight=1)
pane_quitAdmin.pack_propagate(False)

# Adding label and a Listbox for console
ttk.Label(pane_console, text="Console", font=("Consolas", 20, "bold")).pack(side="top", fill="both")
listbox = tk.Listbox(pane_console, background="white", foreground="black", width=40, height=15, font=18)
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

# Quit button and Label for tab1
ttk.Label(pane_quitAdmin, text="Close User Interface", font=("segoe UI", 12, 'bold')).pack(side="top", fill="none", anchor="center", pady=(5, 10))
ttk.Button(pane_quitAdmin, text="QUIT!", command=cancel).pack(side="top", fill="none", anchor="center", pady=(5, 5))

# Thread for the loop to work with the main window loop
# ".daemon" needed if other while loops inflict with "mainloop()"
t = Thread(target=admin).start()
t1 = Thread(target=loop)
t1.daemon = True
t1.start()
t2 = Thread(target=randomValue)
t2.daemon = True
t2.start()
window.mainloop()
