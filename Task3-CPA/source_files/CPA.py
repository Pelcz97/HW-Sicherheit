#!/usr/bin/python3
import Hamming
import numpy as np
from numpy import genfromtxt
import csv
from Sbox import getSboxValue

traces = genfromtxt('/home/philipp/workspace/hw-security-course-ws19/Task3-CPA/example_traces/test_traces.csv', delimiter=',')

with open('/home/philipp/workspace/hw-security-course-ws19/Task3-CPA/example_traces/test_msgs.csv', newline='') as csvfile:
    msgs = list(csv.reader(csvfile))

msgs = np.array(msgs, dtype=str)

#Set this to the Byte you want to attack
numByte = 1
#Set this to 0 or 1 depending on which column of msgs you wanna use
plainOrCipher = 0

numTraces = traces.shape[0]
traceLength= traces.shape[1]

k = np.arange(0,256)
H = np.zeros((256, len(msgs)))

for i in range(256):
    for j in range(len(msgs)):
        msg = msgs[j,plainOrCipher]
        msg = msg[2*numByte:2*numByte+2]
        msg = int(msg, 16)
        H[i,j] = getSboxValue(msg ^ k[i])


print("Number of traces: ", numTraces)
print("Trace length: ", traceLength)