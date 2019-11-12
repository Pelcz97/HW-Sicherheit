import os
import sys

somedir = './puf_data'

filenames = [f for f in os.listdir(somedir) if os.path.isfile(os.path.join(somedir, f))]

#Number of LinesPerFile. This number is extracted manually by looking at one File
linesPerFile = 512


puf_data = [[0 for x in range(linesPerFile)] for y in range(len(filenames))]

for i in range(len(filenames)):
    file = open(somedir + "/" + filenames[i], "r")
    for j in range(512):
        puf_data[i][j] = file.readline()
        #Deletes the \n charakter
        puf_data[i][j] = puf_data[i][j][:-1]
    file.close()

#now every line is stored in puf_data. It is a 2D Array filled with strings. The "Rows" are the different files and the "Columns" are the different lines


def HammingDistance(firstString, secondString):
    return "Test"