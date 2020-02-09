#!/usr/bin/python3

import os
import sys
import serial
import time
import serial.tools.list_ports
import random
import csv
from tqdm import tqdm
# import CPA
from multiprocessing import Pool

FILEPATH = ""

KEY = "2b7e151628aed2a6abf7158809cf4f3c"

# Edit UART device if necessary
DEV_UART = '/dev/tty.usbserial-FD1201'

BAUD_RATE=1000000

# Sensor trace length
SENS_LEN = 56

ser = serial.Serial(
    port=DEV_UART,
    baudrate=BAUD_RATE,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# in windows:
if ('-win') in sys.argv:
    # BASEPATH='C:/Users/Xiang/Documents/git/iot-security/'
    plist = list(serial.tools.list_ports.comports())

    if len(plist) <= 0:
        print("The Serial port can't be found!")
    else:
        plist_0 = list(plist[1])
        DEV_UART = plist_0[0]

# if you connect the reset signal in LatticeiCE40HX8K.pcf
# (with set_io RST B13), then you can reset the FPGA like this:
time.sleep(0.001)
ser.setRTS(False)
time.sleep(0.001)
ser.setRTS(True)
time.sleep(0.001)

# consume any bytes up to 32 left on the UART buffer:
ser.read(32).decode('utf8','ignore')

def generateTraceSet(number_of_traces):

    for i in tqdm(range(number_of_traces)):
        plaintext_num = random.randrange(0, 2**128)
        plaintext_hex = hex(plaintext_num)
        plaintext = str(plaintext_hex).replace('0x', '')
        plaintext = plaintext.zfill(32)
        cipher, sense = generateSingleTrace(plaintext)

        with open('messages.csv', mode='a+') as messages:
            messages_writer = csv.writer(messages, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            messages_writer.writerow([KEY, plaintext, cipher])

        with open('traces.csv', mode='a+') as traces:
            traces_writer = csv.writer(traces, delimiter=';', quoting=csv.QUOTE_NONE)
            senseText = str(list(map(int, sense)))
            print(senseText)
            traces_writer.writerow([senseText.replace('[', "").replace(']', "")])

            

def generateSingleTrace(plaintext):



    # Send the example test string from NIST.FIPS.197
    print("Sending plaintext: ", plaintext)
    #ser.write(bytes.fromhex("0123456789abcdef0123456789abcdef"))
    ser.write(bytes.fromhex(plaintext))

    # Receive the 16 byte ciphertext and the 56 byte sensor values
    cipher = ser.read(16)
    sense = ser.read(56)
    if (len(cipher) == 16):
        print("Received ciphertext: " + cipher.hex())        
    else:
        print("Error receiving ciphertext!")
        print("Received: " + c)
        
    if (len(sense) == 56):
        print("Received 56 bytes of sensor values:\n" + str(list(map(int, sense))))
    else:
        print("Error receiving sensor values!")
        print("Received: " + str(list(map(int, sense))))

    cipherstring = cipher.hex()

    return cipherstring, sense

generateTraceSet(30000)

# with Pool(processes=8) as pool:
#     pool.map(CPA.CPA, range(8))
