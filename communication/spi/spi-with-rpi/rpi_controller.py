import RPi.GPIO as GPIO
import toml
import time


bit_string = '10101010'

with open('pins.toml', 'r') as f:
    pins = toml.load(f)

clock_pin = int(pins['pins']['clock_pin'])
select_pin = int(pins['pins']['select_pin'])
copi_pin = int(pins['pins']['copi_pin'])

current_index = 0

def spi_output():
    GPIO.output(copi_pin, int(bit_string[current_index % 8]))
    current_index += 1

GPIO.setclock(clock_pin, 2) # could use slower hz for testing (500_000 for actual maybe) 
GPIO.add_event_detect(clock_pin, GPIO.RISING, callback=spi_output) # might be falling edge

# TRY IMPLEMENTING WITH PWM

try:  
    while True: pass  
except KeyboardInterrupt:
    GPIO.cleanup()

# while True:
#     GPIO.output(clock_pin, GPIO.HIGH)
#     spi_output(bit_string, current_index)
#     time.sleep(0.5)
#     GPIO.output(clock_pin, GPIO.LOW)
#     time.sleep(0.5)
