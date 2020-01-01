import numpy as np
import time
import multiprocessing as mp
import ctypes


# Playground for parallel stuff
#shared_array_base = mp.Array(ctypes.c_double, 256*87)
#shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
#shared_array = shared_array.reshape(256, 87)

shared_r_base = mp.Array(ctypes.c_float, 256*87)
shared_r = np.ctypeslib.as_array(shared_r_base.get_obj())
shared_r = shared_r.reshape(256, 87)

shared_H = np.zeros((6000, 87))
shared_T = np.zeros((6000, 256))
shared_mean_H = np.zeros(87)
shared_mean_T = np.zeros(256)

shared_len_T = 0
shared_lenT0 = 0
shared_lenH0 = 0

# Parallel processing
def my_func(i):
    shared_array[i, :] = i


#pool = mp.Pool(mp.cpu_count())
#pool.map(my_func, range(256))

#print(shared_array)

#pool.close()

###########################################

# Even faster correlation trace computation
# Takes the full matrix of predictions instead of just a column
# O - (n,t) array of n traces with t samples each
# P - (n,m) array of n predictions for each of the m candidates
# returns an (m,t) correaltion matrix of m traces t samples each
def correlationTraces(O, P):
    (n, t) = O.shape  # n traces of t samples
    (n_bis, m) = P.shape  # n predictions for each of m candidates

    DO = O - (np.einsum("nt->t", O, dtype='float64', optimize='optimal') / np.double(n))  # compute O - mean(O)
    DP = P - (np.einsum("nm->m", P, dtype='float64', optimize='optimal') / np.double(n))  # compute P - mean(P)

    numerator = np.einsum("nm,nt->mt", DP, DO, optimize='optimal')
    tmp1 = np.einsum("nm,nm->m", DP, DP, optimize='optimal')
    tmp2 = np.einsum("nt,nt->t", DO, DO, optimize='optimal')
    tmp = np.einsum("m,t->mt", tmp1, tmp2, optimize='optimal')
    denominator = np.sqrt(tmp)

    return numerator / denominator


def rowOfAttack(i):

    print("New Row")
    print("Shared_LenT0: ", shared_lenT0)
    for j in range(shared_lenT0):
        print("row {0}, element {1}".format(i, j))
        numerator = 0
        sum1 = 0
        sum2 = 0
        for d in range(shared_len_T):
            mul1 = shared_H[d][i] - shared_mean_H[i]
            mul2 = shared_T[d][j] - shared_mean_T[j]
            mul = np.multiply(mul1, mul2)
            numerator += mul

            sum1 += np.square(shared_H[d][i] - shared_mean_H[i])
            sum2 += np.square(shared_T[d][j] - shared_mean_T[j])

        denominator = np.multiply(sum1, sum2)
        denominator = np.sqrt(denominator)
        shared_r[j][i] = np.divide(numerator, denominator)


def attackingWithCorrelation(H, T):

    shared_H = H
    shared_T = T

    start = time.time()
    shared_mean_H = np.mean(H, axis=0)
    shared_mean_T = np.mean(T, axis=0)
    endMean = time.time()

    shared_len_T = len(T)
    shared_lenT0 = len(T[0])
    print("ORIGIN T0: ", len(T[0]))
    shared_lenH0 = len(H[0])

    pool = mp.Pool(mp.cpu_count())

    print(endMean - start)
    print("Shared len H0 ", shared_lenH0)
    pool.map(rowOfAttack, range(shared_lenH0))

    '''for i in range(len_H0):
        for j in range(len_T0):
            numerator = 0
            sum1 = 0
            sum2 = 0
            for d in range(len(T)):
                mul1 = H[d][i] - mean_h[i]
                mul2 = T[d][j] - mean_t[j]
                mul = np.multiply(mul1, mul2)
                numerator += mul

                sum1 += np.square(H[d][i] - mean_h[i])
                sum2 += np.square(T[d][j] - mean_t[j])

            denominator = np.multiply(sum1, sum2)
            denominator = np.sqrt(denominator)
            r[j][i] = np.divide(numerator, denominator)

            print("Step i:{0}, j:{1}".format(i, j))'''
    pool.close()
    end = time.time()
    print(end - start)
    return shared_r

