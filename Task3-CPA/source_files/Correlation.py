import numpy as np
import time
import multiprocessing as mp
import ctypes


class Correlation:

    def __init__(self, H, T):
        self.H = H
        self.T = T
        self.mean_h = np.mean(H, axis=0)
        self.mean_t = np.mean(T, axis=0)
        self.len_T = len(T)
        self.len_T0 = len(T[0])
        self.len_H0 = len(H[0])
        self.r = np.zeros((256,87))


    # Even faster correlation trace computation
    # Takes the full matrix of predictions instead of just a column
    # O - (n,t) array of n traces with t samples each
    # P - (n,m) array of n predictions for each of the m candidates
    # returns an (m,t) correaltion matrix of m traces t samples each
    def correlationTraces(self, O, P):
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


    def rowOfAttack(self, i):

        print("New Row")
        print("Shared_LenT0: ", self.len_T0)
        for j in range(self.len_T0):
            print("row {0}, element {1}".format(i, j))
            numerator = 0
            sum1 = 0
            sum2 = 0
            for d in range(self.len_T):
                mul1 = self.H[d][i] - self.mean_h[i]
                mul2 = self.T[d][j] - self.mean_t[j]
                mul = np.multiply(mul1, mul2)
                numerator += mul

                sum1 += np.square(self.H[d][i] - self.mean_h[i])
                sum2 += np.square(self.T[d][j] - self.mean_t[j])

            denominator = np.multiply(sum1, sum2)
            denominator = np.sqrt(denominator)
            self.r[i][j] = np.divide(numerator, denominator)


    def attackingWithCorrelation(self, H, T):

        start = time.time()

        endMean = time.time()

        pool = mp.Pool(mp.cpu_count())

        print(endMean - start)
        print("Shared len H0 ", self.len_H0)
        print(self.len_H0)
        pool.map(self.rowOfAttack, range(self.len_H0))

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
        return self.r

