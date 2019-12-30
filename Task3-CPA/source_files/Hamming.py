#!/usr/bin/python3


def HammingWeightXOR(string1, string2):
    assert len(string1) == len(string2)
    result = []
    for i in range(len(string1)):
        if (string1[i] != string2[i]):
            result.append('1')
        else:
            result.append('0')
    return HammingDistance(result) 

def HammingDistance(string):
    result = 0
    for i in range(len(string)):
        if (string[i] == '1'):
            result += 1
    return result