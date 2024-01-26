import RPi.GPIO as GPIO
import toml
import time


with open('../pins.toml', 'r') as f:
    pins = toml.load(f)

in1 = int(pins['pins']['in1_pin'])
in2 = int(pins['pins']['in2_pin'])

for i in range(100):
    time.sleep(1)
    GPIO.output(in1, i % 2)
    GPIO.output(in2, (i + 1) % 2)
    