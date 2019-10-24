#!/usr/bin/env python3

import os
import sys
import serial
import time
import serial.tools.list_ports

DEV_UART = '/dev/ttyUSB1'

if ('-win') in sys.argv:
    plist = list(serial.tools.list_ports.comports())

    if len(plist) <= 0:
        print("The Serial port can't be found!")
    else:
        plist_0 = list(plist[1])
        DEV_UART = plist_0[0]

BAUD_RATE=115200

ser = serial.Serial(
    port=DEV_UART,
    baudrate=BAUD_RATE,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1 # timeout in seconds
)

# if you connect the reset signal in LatticeiCE40HX8K.pcf
# (with set_io RST B13), then you can reset the FPGA like this:
time.sleep(0.001);
ser.setRTS(False);
time.sleep(0.001);
ser.setRTS(True);
time.sleep(0.001);

# You can also work with the FTDI CTS and DTR signals if you want. Please check the
#  LatticeiCE40HX8K.pcf and the top_level.v how RTS is connected. Similarly you can use
#  the DTR and CTS lines.

# consume data already buffered in the usb-to-serial adapter from before resetting the board
print("Data left on usb-serial adapter from reset: < "+str(ser.read(32).decode('utf8','ignore'))+" >");

# interact with board, send an 's'
ser.write(b's')

# TODO, here you can receive from the board
# this reads two bytes from the uart, timeout in seconds as defined above
data = ser.read(2)


# ..... do stuff ......


ser.close()

print("Finished");
