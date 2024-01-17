import RPi.GPIO as GPIO
import time


for i in range(100):
    time.sleep(1)
    GPIO.output(23, i % 2)
    GPIO.output(24, (i + 1) % 2)
    