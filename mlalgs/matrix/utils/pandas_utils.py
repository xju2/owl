__author__ = 'xju'
from pandas import DataFrame
import numpy as np


def unpivot(frame):
    n, k = frame.shape
    data = {'rate': frame.values.ravel('F'),
            'user_id': np.asarray(frame.columns).repeat(n),
            'movie_id': np.tile(np.asarray(frame.index), k)}
    return DataFrame(data, columns=['rate', 'movie_id', 'user_id'])