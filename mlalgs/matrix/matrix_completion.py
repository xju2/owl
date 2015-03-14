#!/usr/bin/env python
from pandas import *
from scipy import linalg
import time


class SVDThreshold:
    def __init__(self):
        self.cut_num = 5
        self.delta = 1.2
        self.tolerance = 8

    def train(self, matrix):
        print("training the matrix, ", matrix.shape)
        start_time = time.time()
        norm = 100
        projector = matrix.notnull()
        m, n = matrix.shape
        counter = 0
        n_keep = self.cut_num
        xk = matrix.T.fillna(method='ffill').fillna(method='bfill').T
        while norm > self.tolerance and counter < 200:
            xk[projector] = matrix[projector]
            u, s, v = linalg.svd(xk)
            sig = linalg.diagsvd(s, m, n)
            cutoff = sig[n_keep-1]
            sig_cut = sig*(sig > cutoff)
            new_matrix = u.dot(sig_cut.dot(v))
            xk = DataFrame(new_matrix, index=matrix.index, columns=matrix.columns)
            diff_matrix = matrix[projector] - xk[projector]
            norm = linalg.norm(diff_matrix.fillna(0))
            counter += 1
            if counter % 50 == 0:
                n_keep += 1
#            if counter % 100 == 0:
#                print('be patient, working on it...')
#                print('time spend: %s'%(time.time()-start_time))
        print("total cost: %s seconds"%(time.time()-start_time))
        print("total loops: ", str(counter))
        return xk