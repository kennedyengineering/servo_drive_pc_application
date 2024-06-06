# Servo Drive Application
# main.py

import serial
import struct
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=str, default='/dev/ttyACM0')
parser.add_argument('--baud_rate', type=int, default=115200)
args = parser.parse_args()

ser = serial.Serial(args.port,
                    args.baud_rate,
                    timeout=1)

rx_struct_format = 'ii'
rx_struct_size = struct.calcsize(rx_struct_format)

tx_struct_format = 'i'
tx_struct_size = struct.calcsize(tx_struct_format)

# Transmit
data = (999,)
packed_data = struct.pack(tx_struct_format, *data)
ser.write(packed_data)

# Receive
try:
    while True:
        print("Reading serial port")

        data = ser.read(rx_struct_size)

        print(data)

        if len(data) == rx_struct_size:
            unpacked_data = struct.unpack(rx_struct_format, data)

            print(unpacked_data)

except KeyboardInterrupt:
    print("Exiting Program")

finally:
    ser.close()
