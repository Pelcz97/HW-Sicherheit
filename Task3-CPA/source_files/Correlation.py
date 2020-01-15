import numpy as np
import time
import multiprocessing as mp
import ctypes


class Correlation:

    def __init__(self, H, T):
        self.H = H
        self.T = T


    # Nimmt Traces Matrix und Predictions Matrix entgegen
    # O - (n,t) Array mit n Traces, t samples
    # P - (n,m) Array mit n Predictions für jeden der m Kandidaten
    # Rückgabe: Korrelationsmatrix (m,t) für alle Schlüsselkandidaten & Samples
    def correlationTraces(self, T, P):
        (n, t) = T.shape  # n traces of t samples
        (n_bis, m) = P.shape  # n predictions for each of m candidates

        DT = T - (np.einsum("nt->t", T, dtype='float64', optimize='optimal') / np.double(n))  # T - mean(T)
        DP = P - (np.einsum("nm->m", P, dtype='float64', optimize='optimal') / np.double(n))  # P - mean(P)

        numerator = np.einsum("nm,nt->mt", DP, DT, optimize='optimal')
        tmp1 = np.einsum("nm,nm->m", DP, DP, optimize='optimal')
        tmp2 = np.einsum("nt,nt->t", DT, DT, optimize='optimal')
        tmp = np.einsum("m,t->mt", tmp1, tmp2, optimize='optimal')
        denominator = np.sqrt(tmp)

        return numerator / denominator

