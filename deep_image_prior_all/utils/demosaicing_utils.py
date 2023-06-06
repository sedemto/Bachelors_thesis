from PIL import Image
import numpy
from .common_utils import *
import random


def empty_bayer_filter(img_np):
    c,h,w = img_np.shape
    result_array = numpy.zeros((c,h,w),np.dtype('float32'))
    '''
    
    Chosen bayer pattern:   
            R  G1
            G2  B
    
    '''
    result_array[0, ::2, ::2] = 1
    result_array[2, 1::2, 1::2] = 1
    result_array[1, ::2, 1::2] = 1
    result_array[1, 1::2, ::2] = 1
    return result_array


def x_trans_filter(img_np):
    c, h, w = img_np.shape
    result_array = np.zeros((c, h, w), np.dtype('float32'))
    # i == y == row
    # j == x == column
    for i in range(h):
        for j in range(w):
            # green [0,0]; [1;1]; [2;2]
            if i % 3 == 0 and j % 3 == 0 or i % 3 == 1 and j % 3 == 1 or i % 3 == 2 and j % 3 == 2:
                result_array[1][i][j] = 1

            # green [2;1]; [1;2]
            if i % 3 == 1 and j % 3 == 2 or i % 3 == 2 and j % 3 == 1:
                result_array[1][i][j] = 1

            if i % 6 < 3 and j % 6 < 3 or i % 6 >= 3 and j % 6 >= 3:
                # red 1
                if i % 3 == 1 and j % 3 == 0 or i % 3 == 0 and j % 3 == 2:
                    result_array[0][i][j] = 1
                # blue 1
                if i % 3 == 0 and j % 3 == 1 or i % 3 == 2 and j % 3 == 0:
                    result_array[2][i][j] = 1
            # red 2
            if i % 6 == 5 and j % 6 == 0 or i % 6 == 0 and j % 6 == 4 or \
                    i % 6 == 2 and j % 6 == 3 or i % 6 == 3 and j % 6 == 1:
                result_array[0][i][j] = 1

            # blue 2
            if i % 6 == 0 and j % 6 == 5 or i % 6 == 4 and j % 6 == 0 or \
                    i % 6 == 3 and j % 6 == 2 or i % 6 == 1 and j % 6 == 3:
                result_array[2][i][j] = 1
    return result_array


def random_filer(img_np):
    c, h, w = img_np.shape
    result_array = np.zeros((c, h, w), np.dtype('float32'))
    random_sur = set()
    while len(random_sur) != (h*w):
        i = random.randint(0,h-1)
        j = random.randint(0,w-1)
        if (i,j) not in random_sur:
            random_sur.add((i,j))
            colors = [0,1,2]
            color = random.choice(colors)
            result_array[color][i][j] = 1
    return result_array