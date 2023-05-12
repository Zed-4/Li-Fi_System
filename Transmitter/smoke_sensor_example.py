# To install: pip3 install adafruit-circuitpython-mcp3xxx
# Tutorial URL: https://learn.adafruit.com/mcp3008-spi-adc/python-circuitpython

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import pygame
import time

MQ2_THRESHOLD = 1.0


pygame.mixer.init()
pygame.mixer.music.load("./LiFiSounds/SmokeAlert.wav")

from adafruit_mcp3xxx.analog_in import AnalogIn
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# MCP3008 chip is conected to GPIO Pin 5
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

# Smoke sensor is connected to channel 0 on the MCP3008 Chip
smokeChannel = AnalogIn(mcp, MCP.P0)


while True:
      print('Raw ADC Value: ', smokeChannel.value)
      if(float(str(smokeChannel.voltage)) > MQ2_THRESHOLD and not pygame.mixer.music.get_busy()):
         # SMOKE SENSOR ABOVE THRESHOLD
         pygame.mixer.music.play()
      time.sleep(0.1)
    
