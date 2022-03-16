from numpy import *

def tychonov_distance(c,k):
    if c == k:
        return 0
        
    midX,midY = c.shape
    midX = floor(midX/2); midY = floor(midY/2)

    for i in range(midX):
        for j in range(midX):
            if      c[ i, j] != k[ i, j] \
                or  c[ i,-j] != k[ i,-j] \
                or  c[-i, j] != k[-i, j] \
                or  c[-i,-j] != k[-i,-j]:
                break

    return 2**(-max(i,j))