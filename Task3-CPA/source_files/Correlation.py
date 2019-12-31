import numpy as np
import time
import multiprocessing as mp

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

def partOfAttack():


def attackingWithCorrelation(H, T):

    pool = mp.Pool(mp.cpu_count())


    start = time.time()

    mean_h = np.mean(H, axis=0)
    mean_t = np.mean(T, axis=0)

    endMean = time.time()

    print(endMean - start)

    len_T0 = len(T[0])
    len_H0 = len(H[0])

    r = np.zeros((len_T0, len_H0))

    for i in range(len_H0):
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

            print("Step i:{0}, j:{1}".format(i, j))
    
    end = time.time()
    print(end - start)
    return r

