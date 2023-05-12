import RPi.GPIO as GPIO
import time

LED_PIN = 4
PERIOD = 0.05
varString = "sss"

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
string_length = len(varString)

def send_byte(my_byte):
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(PERIOD)

    for b in [int(x) for x in '{:08b}'.format(my_byte)][::-1]:
        GPIO.output(LED_PIN, GPIO.LOW if b == 0 else GPIO.HIGH)
        time.sleep(PERIOD)

    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(PERIOD)

try:
    while True:
        for i in range(0, string_length):
            send_byte(ord(varString[i]))
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
