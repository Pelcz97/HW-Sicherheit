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
import time
import multiprocessing as mp
import itertools
import tqdm

def findLasRoundKeyByte(numByte):
    lastRoundkey = 'd014f9a8c9ee2589e13f0cc8b6630ca6'
    return lastRoundkey[2*numByte:2*numByte+2]



def CPA(indices):
    if platform == "linux" or platform == "linux2":
        TRACES = '/home/philipp/workspace/hw-security-course-ws19/Task3-CPA/source_files/36/Threshholds/traces_7.csv'
        MSGS = '/home/philipp/workspace/hw-security-course-ws19/Task3-CPA/source_files/36/messages.csv'
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



    # msgs = np.array(msgs, dtype=str)


    #Set this to the Byte you want to attack
    print("Running ", indices)
    numByte = indices[0]
    numBit = indices[1]

    numTraces = traces.shape[0]
    traceLength = traces.shape[1]


    k = np.arange(0, 256)
    H = np.zeros((256, len(msgs)))

    start = time.time()

    for i in range(len(k)):
        for j in range(len(msgs)):
            msg = msgs[j][2]
            msg = msg[2*numByte:2*numByte+2]
            msg = int(msg, 16)
            H[i,j] = getInvSboxValue(msg ^ k[i])
            H[i,j] = np.bitwise_and(np.array(H[i,j]).astype(int), 2**numBit)

    HModel = H
    for i in range(len(H)):
        HModel[i] = np.array(list(map(Hamming.HammingDistanceInt, H[i])))

    endPower = time.time()

    HModel = HModel.T

    correlationObject = Correlation(HModel,traces)
    corrMatrix = correlationObject.correlationTraces(traces, HModel)

    endCorr = time.time()

    maxValue = np.amax(np.abs(corrMatrix))
    result = np.where(np.abs(corrMatrix) == maxValue)


    filename = str(numByte) + "_" + str(numBit)
    figureNumber = numByte*8 + numBit
    plt.figure(figureNumber)
    plt.plot(corrMatrix.T, color='gray')
    correctByte = findLasRoundKeyByte(numByte)
    correctByte = int(correctByte, 16)
    print(correctByte)
    plt.plot(corrMatrix[correctByte].T, color='red')
    title = "BYTE_BIT: " + filename + " KEYHYP: " + str(result[0]) + " TRACE MOMENT: " + str(result[1]) + " Max CorrValue: " + str(maxValue)
    plt.title(title)
    filename = filename + ".png"
    exportpath = '/home/philipp/workspace/hw-security-course-ws19/Task3-CPA/source_files/48/Threshholds/CorrelationImages35/' + filename
    plt.savefig(filename, dpi=100)
    plt.close(figureNumber)

    print("------------------------------------------")
    print("Byte number is: ", numByte)
    print("Bit number is: ", numBit)
    print("Number of traces: ", numTraces)
    print("Trace length: ", traceLength)
    print("Power took", endPower - start)
    print("Correlation took", endCorr - start)
    print("Max value is: ", maxValue)
    print("The best Key Hyp is: ", result[0])
    print("Korrelation is in point: ", result[1])
    print("------------------------------------------")


a = range(16)
b = range(8)

allCombinations = list(itertools.product(a,b))

# for elem in tqdm.tqdm(allCombinations):
#     CPA(elem)

with mp.Pool(processes=8) as pool:
    pool.map(CPA, allCombinations)