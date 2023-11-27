import serial
import threading
import sys


if len(sys.argv) < 2:
    print('Not enough args')
    sys.exit(1)

port = sys.argv[1]
tosend = b'b'

# could also send the following data
# x = bytearray()
# x.append(0xFF) # bit string of length 8 with all 1s

# baud is 9600
with serial.Serial(port, timeout=2) as ser:
    for i in tosend:
        print(f'Sending: {i}')
        ser.write(i)

    ret = ser.read(400)
    
    print(f'Recieving: {ret}')
