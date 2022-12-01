import numpy as np
import pandas as pd


def make_mask(values, mask_size):

    mask = np.zeros((mask_size, mask_size))
    for v in values:
        mask[v] = 1
    return mask

def get_cord_min(array):
    array = np.array(array)
    rowsize, columnsize = array.shape
    amin = array.argmin()
    row = int(amin/columnsize)
    column = amin % columnsize
    return (row, column) 
# print(make_mask([(0,0), (1, 0)], 4))


data = [[-10, 2], [3, -1], [6, -19]]
print(get_cord_min(data))
# print(np.array(data).flatten())
print(np.array(data))
