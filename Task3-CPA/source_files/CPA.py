#!/usr/bin/python3
import Hamming
import numpy as np
from numpy import genfromtxt
import csv
from Sbox import getSboxValue
import matplotlib.pyplot as plt
import Correlation
import multiprocessing as mp


from sys import platform
if platform == "linux" or platform == "linux2":
    TRACES = '/home/philipp/workspace/hw-security-course-ws19/Task3-CPA/example_traces/test_traces.csv'
    MSGS = '/home/philipp/workspace/hw-security-course-ws19/Task3-CPA/example_traces/test_msgs.csv'
elif platform == "darwin":
    TRACES = '/Users/janlucavettel/Documents/FPGA/HW-Sicherheit/Task3-CPA/example_traces/test_traces.csv'
    MSGS = '/Users/janlucavettel/Documents/FPGA/HW-Sicherheit/Task3-CPA/example_traces/test_msgs.csv'
#elif platform == "win32":
    # Windows...
    

print("Number of processors: ", mp.cpu_count())

traces = genfromtxt(TRACES, delimiter=',')

with open(MSGS, newline='') as csvfile:
    msgs = list(csv.reader(csvfile))

msgs = np.array(msgs, dtype=str)

#Set this to the Byte you want to attack
numByte = 0
#Set this to 0 or 1 depending on which column of msgs you wanna use
plainOrCipher = 1

numTraces = traces.shape[0]
traceLength= traces.shape[1]

k = np.arange(0,256)
H = np.zeros((256, len(msgs)))

for i in range(len(k)):
    for j in range(len(msgs)):
        msg = msgs[j,plainOrCipher]
        msg = msg[2*numByte:2*numByte+2]
        msg = int(msg, 16)
        H[i,j] = getSboxValue(msg ^ k[i])

HModel = H
for i in range(len(H)):
    HModel[i] = np.array(list(map(Hamming.HammingDistanceInt, H[i])))

HModel = HModel.T

corrMatrix = Correlation.attackingWithCorrelation(traces, HModel)

Ri = np.zeros(256)
for i in range(len(Ri)):
    Ri[i] = max(abs(corrMatrix[i]))

maxValue = max(Ri)

print(maxValue)

print("Number of traces: ", numTraces)
print("Trace length: ", traceLength)