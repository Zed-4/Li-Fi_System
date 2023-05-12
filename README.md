# Li-Fi_System
TSGC Design Challange Team Mellowship © 2022-2023

The mission of the project was to Investigate and demonstrate a prototype of Li-Fi technology. In order to illustrate how Li-Fi can communicate with multiple systems and send commands to. For the final form of the project, we incorporated voice control. That way, the user may be able to hands free control all the built in functionalities.

## Main Components

**This project requires:** <br>
- `Transmitter`: A Raspery Pi, LED Lights, USB microphone, MQ-2 Gas and Smoke Analog Sensor, Raspberry LCD display <br>
- `Receiver`:    A Raspery Pi, Servo motor, lighting Ring, USB Speakers, I2C Temperature and Humidity Sensor, LPS22 Pressure Sensor <br>
This project requires (main components):

## Setup

**For Linux\pi needed libraries:** <br>

- `vosk:` <br>
```
pip3 install vosk
```
For vosk's language models, follow the link to downlaod desired model: [Voice Models](https://alphacephei.com/vosk/models) <br>

- `pyaudio:` <br>
```
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install ffmpeg libav-tools
sudo pip install pyaudio
```

## TKinter Theme used

`rdbende:` https://github.com/rdbende/Forest-ttk-theme

## Contributors:

**Abtin Ortgoli:** <br>
- `Role:` Lead Software
- `Contact:` abtinortgoli@ymy.unt.edu

**Conor Vanek:** <br>
- `Role:` Team lead
- `Contact:` conorvanek@my.unt.edu <br>

**Daniel Carillo:** <br>
- `Role:` PCB Design
- `Contact:` danielcarrillo3@my.unt.edu

**Vinh Trinh:** <br>
- `Role:` Hardware Design
- `Contact:` vinhtrinh@my.unt.edu
