import RPi.GPIO as GPIO
import time

LED_PIN = 4
PERIOD = 0.05
varString = 0x73

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
#string_length = len(varString)

def send_byte(my_byte):
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(PERIOD)

    for x in range(0, 8):
        conditionCheck = (True if(my_byte & (0x01 << x) != 0) else False)
        GPIO.output(LED_PIN, GPIO.HIGH if(my_byte & (0x01 << x) != 0) else GPIO.LOW)
        time.sleep(PERIOD)

    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(PERIOD)

try:
    while True:
        #for i in range(0, string_length):
        send_byte(varString)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
