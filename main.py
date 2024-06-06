# Servo Drive Application
# main.py

import serial
import struct
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=str, default='/dev/ttyACM0')
parser.add_argument('--baud_rate', type=int, default=115200)
args = parser.parse_args()

ser = serial.Serial(args.port, args.baud_rate, timeout=1)

struct_format = 'ii'
struct_size = struct.calcsize(struct_format)

try:
    while True:
        print("Reading serial port")

        data = ser.read(struct_size)

        print(data)

        if len(data) == struct_size:
            unpacked_data = struct.unpack(struct_format, data)

            print(unpacked_data)

except KeyboardInterrupt:
    print("Exiting Program")

finally:
    ser.close()
