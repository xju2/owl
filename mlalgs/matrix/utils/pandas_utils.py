__author__ = 'xju'
from pandas import DataFrame
import numpy as np


def unpivot(frame, index_name, columns_name, value_name):
    n, k = frame.shape
    data = {value_name: frame.values.ravel('F'),
            columns_name: np.asarray(frame.columns).repeat(n),
            index_name: np.tile(np.asarray(frame.index), k)}
    return DataFrame(data, columns=[value_name, index_name, columns_name])