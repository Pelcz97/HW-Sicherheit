#!/usr/bin/python3
import csv
import Hamming
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from Sbox import getSboxValue
from Sbox import getInvSboxValue
from sys import platform
from Correlation import Correlation
from Crypto.Cipher import AES
import binascii

if platform == "linux" or platform == "linux2":
    TRACES = '/home/philipp/workspace/hw-security-course-ws19/Task3-CPA/example_traces/test_traces.csv'
    MSGS = '/home/philipp/workspace/hw-security-course-ws19/Task3-CPA/example_traces/test_msgs.csv'
elif platform == "darwin":
    TRACES = '/Users/janlucavettel/Documents/FPGA/HW-Sicherheit/Task3-CPA/example_traces/test_traces.csv'
    MSGS = '/Users/janlucavettel/Documents/FPGA/HW-Sicherheit/Task3-CPA/example_traces/test_msgs.csv'
#elif platform == "win32":
    # Windows...


traces = genfromtxt(TRACES, delimiter=',')

with open(MSGS, newline='') as csvfile:
    msgs = list(csv.reader(csvfile))


key = msgs[0][0]
key = binascii.unhexlify(key)
cipher = AES.new(key, AES.MODE_ECB)
decipher = AES.new(key, AES.MODE_ECB)
ciphertexts = []

for i in range(len(msgs)):
    text = cipher.encrypt(binascii.unhexlify(msgs[i][1]))
    a = binascii.hexlify(text).lower()
    a = a.decode("utf-8")
    msgs[i].append(a)



msgs = np.array(msgs, dtype=str)


#Set this to the Byte you want to attack
numByte = 0
numBit = 0

numTraces = traces.shape[0]
traceLength = traces.shape[1]

k = np.arange(0, 256)
H = np.zeros((256, len(msgs)))


for i in range(len(k)):
    for j in range(len(msgs)):
        msg = msgs[j, 2]
        msg = msg[2*numByte:2*numByte+2]
        msg = int(msg, 16)
        H[i,j] = getInvSboxValue(msg ^ k[i])
        H[i,j] = np.bitwise_and(np.array(H[i,j]).astype(int), 2**numBit)

HModel = H
for i in range(len(H)):
    HModel[i] = np.array(list(map(Hamming.HammingDistanceInt, H[i])))

HModel = HModel.T

correlationObject = Correlation(HModel,traces)
corrMatrix = correlationObject.correlationTraces(traces, HModel)

maxValue = np.amax(np.abs(corrMatrix))
result = np.where(np.abs(corrMatrix) == maxValue)


plt.plot(corrMatrix.T, color='gray')
plt.plot(corrMatrix[result[0]].T, color='red')
plt.show()

print("Max value is: ", maxValue)

print("Number of traces: ", numTraces)
print("Trace length: ", traceLength)