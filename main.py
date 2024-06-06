# Servo Drive Application
# main.py

import serial
import struct
import argparse
import threading

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import TextBox

from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=str, default="/dev/ttyACM0")
parser.add_argument("--baud_rate", type=int, default=115200)
args = parser.parse_args()

ser = serial.Serial(args.port, args.baud_rate, timeout=0.05)

rx_struct_format = "ii"
rx_struct_size = struct.calcsize(rx_struct_format)

tx_struct_format = "i"
tx_struct_size = struct.calcsize(tx_struct_format)

plot_len = 1000
xs = deque(maxlen=plot_len)
yset = deque(maxlen=plot_len)
ymeas = deque(maxlen=plot_len)


# Receive
def readSerial():
    global ymeas, yset, xs, ser

    i = 0

    while True:
        data = ser.read(rx_struct_size)

        if len(data) == rx_struct_size:
            unpacked_data = struct.unpack(rx_struct_format, data)

            ymeas.append(unpacked_data[0])
            yset.append(unpacked_data[1])
            xs.append(i)

            i += 1


rx_thread = threading.Thread(target=readSerial)
rx_thread.daemon = True
rx_thread.start()

# Plot
fig = plt.figure("Servo Drive Application")
fig.subplots_adjust(bottom=0.25)
ax1 = fig.add_subplot(1, 1, 1)


def animate(i, xs, ymeas, yset):
    ax1.clear()
    ax1.plot(xs, ymeas, label="measured")
    ax1.plot(xs, yset, "-.", label="setpoint")
    ax1.set_xlabel("Timestep")
    ax1.set_ylabel("Position")


ani = animation.FuncAnimation(
    fig=fig, func=animate, interval=0.25, fargs=(xs, ymeas, yset), save_count=10
)


def submit(text):
    global ser

    data = (int(text),)
    packed_data = struct.pack(tx_struct_format, *data)
    ser.write(packed_data)


text_box_ax = fig.add_axes([0.1, 0.05, 0.8, 0.075])
text_box = TextBox(text_box_ax, "Setpoint", textalignment="center")
text_box.on_submit(submit)

plt.show()

# Exit
ser.close()
