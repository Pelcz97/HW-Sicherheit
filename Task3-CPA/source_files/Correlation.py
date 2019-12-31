import numpy as np

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


def attackingWithCorrelation(D, i , j, h):
    # 0 oder 1?
    numerator = 0
    sum1 = 0
    sum2 = 0
    for d in range(0, D):
        mul1 = h[d][i] - np.mean(h[i])
        mul2 = t[d][j] - np.mean(t[j])
        mul = np.multiply(mul1, mul2)
        numerator += mul

        sum1 += np.square(h[d][i] - np.mean(h[i]))
        sum2 += np.square(t[d][j] - np.mean(t[j]))

    denominator = np.multiply(sum1, sum2)
    denominator = np.sqrt(denominator)

    return np.divide(numerator, denominator)
