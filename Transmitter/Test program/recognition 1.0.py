import speech_recognition as sr
from datetime import datetime
import pyttsx3


def SpeakText(text):

    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# To see the list of input devices: sr.Microphone.list_microphone_names()


enabler = True
speak = " "
recognizer = sr.Recognizer()

with sr.Microphone() as mic:

    name = input("What should I call you?: ")

    print("Calibrating thershold...")
    print("---------------------------------------------")
    recognizer.adjust_for_ambient_noise(mic, duration=2)
    #recognizer.dynamic_energy_threshold = True
    print("Mic calibrated and ready!")

while enabler == True:

    try:

        with sr.Microphone() as mic:

            #recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio)
            text = text.lower()

            print("---------------------------------------------")
            print(f"User said: {text}")
            # SpeakText(time)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:

        print("Voice not recognized. Try Again!")
        recognizer = sr.Recognizer()
        continue

    if text == "hello" or text == "hey":
        speak = f"Hello, {name}, I'm Lie-fi!"
        print(f"\t[Hello {name}, I'm Li-fi! 👋]")
        SpeakText(speak)

    if text == "what is the time" or text == "time":
        now = datetime.now()
        speak = now.strftime('\t[%I:%M:%S %p]')
        print(now.strftime('\t[%I:%M:%S %p]'), "🕑")
        SpeakText(speak)

    if text == "what is the temperature" or text == "temperature":
        speak = "[Temperature, is: 74°F]"
        print("\t[Temperature : 🌡️ 74°F]")
        SpeakText(speak)

    print("---------------------------------------------")

    speak = "Would you like to speak again?"
    SpeakText(speak)
    userInput = input("Would you like to speak again? [y,n]: ")

    userInput = userInput.replace("y", "True")
    userInput = userInput.replace("n", "False")

    if userInput == "False":
        enabler = False
        speak = "voice recognition ended. Goodbye!"
        print("\n\t[voice recognition ended. Goodbye!]")
        SpeakText(speak)
        print("---------------------------------------------")
