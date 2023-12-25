import serial
import threading
import sys


if len(sys.argv) < 2:
    port = 'COM5'
else:
    port = sys.argv[1]

# tosend = b'0'

# could also send the following data
x = bytearray()
x.append(0xFF) 
# x.append(0x0F)
tosend = x

# baud is 9600
with serial.Serial(port, timeout=2) as ser:
    ser.baudrate = 9600
    for i in tosend:
        print(f'Sending: {i}')
        ser.write(i)

    ret = ser.read(256)
    
    print(f'Recieving: {ret}, length: {len(ret)}')
