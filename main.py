# Servo Drive Application
# main.py

import serial
import struct
import argparse
import threading

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=str, default='/dev/ttyACM0')
parser.add_argument('--baud_rate', type=int, default=115200)
args = parser.parse_args()

ser = serial.Serial(args.port,
                    args.baud_rate,
                    timeout=0.05)

rx_struct_format = 'ii'
rx_struct_size = struct.calcsize(rx_struct_format)

tx_struct_format = 'i'
tx_struct_size = struct.calcsize(tx_struct_format)

plot_len = 1000
xs = deque(maxlen=plot_len)
yset = deque(maxlen=plot_len)
ymeas = deque(maxlen=plot_len)

# Transmit
data = (999,)
packed_data = struct.pack(tx_struct_format, *data)
ser.write(packed_data)

# Receive
def readSerial():
    global ymeas, yset, xs

    i = 0

    while True:
        data = ser.read(rx_struct_size)

        if len(data) == rx_struct_size:
            unpacked_data = struct.unpack(rx_struct_format, data)

            ymeas.append(unpacked_data[0])
            yset.append(unpacked_data[1])
            xs.append(i)

            i+=1

rx_thread = threading.Thread(target=readSerial)
rx_thread.daemon = True
rx_thread.start()

# Plot
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i, xs, ymeas, yset):
    ax1.clear()
    ax1.plot(xs, ymeas, label="measured")
    ax1.plot(xs, yset, "-.", label="setpoint")

ani = animation.FuncAnimation(
    fig=fig, func=animate, interval=0.5, fargs=(xs, ymeas, yset), save_count=10
)
plt.show()

# Exit
ser.close()
