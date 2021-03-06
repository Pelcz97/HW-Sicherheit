#!/usr/bin/python3
import os


def HammingDistance(firstBinary, secondBinary):
    assert len(firstBinary) == len(secondBinary)
    result = 0
    for i in range(len(firstBinary)):
        if (firstBinary[i] != secondBinary[i]):
            result += 1
    return result

def hexCharToBin(hexChar):
    if (hexChar == '0'): return '0000'
    if (hexChar == '1'): return '0001'
    if (hexChar == '2'): return '0010'
    if (hexChar == '3'): return '0011'
    if (hexChar == '4'): return '0100'
    if (hexChar == '5'): return '0101'
    if (hexChar == '6'): return '0110'
    if (hexChar == '7'): return '0111'
    if (hexChar == '8'): return '1000'
    if (hexChar == '9'): return '1001'
    if (hexChar == 'a'): return '1010'
    if (hexChar == 'b'): return '1011'
    if (hexChar == 'c'): return '1100'
    if (hexChar == 'd'): return '1101'
    if (hexChar == 'e'): return '1110'
    if (hexChar == 'f'): return '1111'
    else: print('Something went wrong')

def hexStringToBinString(hexString):
    result = ""
    for i in range(len(hexString)):
        result += hexCharToBin(hexString[i])
    return result    


somedir = './puf_data'

filenames = [f for f in os.listdir(somedir) if os.path.isfile(os.path.join(somedir, f))]

#Number of LinesPerFile. This number is extracted manually by looking at one File
linesPerFile = 512
n = 256

#Init for the two Arrays
puf_data = [[0 for x in range(linesPerFile)] for y in range(len(filenames))]
puf_data_bin = [[0 for x in range(linesPerFile)] for y in range(len(filenames))]

for i in range(len(filenames)):
    file = open(somedir + "/" + filenames[i], "r")
    for j in range(linesPerFile):
        puf_data[i][j] = file.readline()
        #Deletes the \n charakter
        puf_data[i][j] = puf_data[i][j][:-1]
        puf_data_bin[i][j] = hexStringToBinString(puf_data[i][j])
    file.close()

print('Reading the files complete! Starting the Calcualations!')

#now every line is stored with its HEX-Values in puf_data. It is a 2D Array filled with strings. The "Rows" are the different files and the "Columns" are the different lines. puf_data_bin stores the exact same values as binary string
uniqueness = 0.0
avg_uniqueness = 0.0
for file in range(len(filenames)):
    for line in range(linesPerFile - 1):
        for otherline in range(line + 1, linesPerFile):
            uniqueness += HammingDistance(puf_data_bin[file][line],puf_data_bin[file][otherline])
    faktor = 2.0/(linesPerFile * (linesPerFile - 1) * n)
    uniqueness *= faktor
    avg_uniqueness += uniqueness
avg_uniqueness = avg_uniqueness / len(filenames)

print('The Average Uniqueness of all files is: ' +  str(100 * avg_uniqueness) + '%')


reliability = 0.0
avg_reliabilty = 0.0
for line in range(linesPerFile):
    for file in range(len(filenames) - 1):
        for otherfile in range(file + 1, len(filenames)):
            reliability += HammingDistance(puf_data_bin[file][line], puf_data_bin[otherfile][line])
    faktor = 2.0 / (len(filenames) * (len(filenames) - 1) * n)
    reliability *= faktor
    avg_reliabilty += reliability
avg_reliabilty /= linesPerFile

print('The Average Reliability of all files is: ' +  str( 100 * (1 - avg_reliabilty))+ '%')
    

uniformity = 0.0
avg_uniformity = 0.0
for file in range(len(filenames)):
    for line in range(linesPerFile):
        avg_uniformity += HammingDistance(puf_data_bin[file][line], '0' * n) / float(n)
avg_uniformity /= (linesPerFile * (len(filenames)))

print('The Average Uniformity of all files is: ' +  str(100 * avg_uniformity) + '%')


aliasing = 0.0
avg_aliasing = 0.0
for file in range(len(filenames)):
    for bit in range(n):
        for line in range(linesPerFile):
            aliasing += HammingDistance(puf_data_bin[file][line][bit], '0')
    aliasing /= (linesPerFile * n)
    avg_aliasing += aliasing
avg_aliasing /= len(filenames)

print('The Average Bit-Aliasing of all files is: ' +  str(100 * avg_aliasing) + '%')