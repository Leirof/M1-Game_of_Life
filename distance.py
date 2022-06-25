from numpy import *

def tychonov_distance(c,k):
    if (c == k).all():
        return 0
        
    midX,midY = c.shape
    midX = int(floor(midX/2)); midY = int(floor(midY/2))

    l = []
    # Break = False
    for i in range(midX):
        for j in range(midX):
            if      c[midX + i, midX + j] != k[midX + i, midX + j] \
                or  c[midX + i, midX - j] != k[midX + i, midX - j] \
                or  c[midX - i, midX + j] != k[midX - i, midX + j] \
                or  c[midX - i, midX - j] != k[midX - i, midX - j]:
                l.append(max(i,j))
    #             break
    #     if Break: break

    # for i in range(midX):
    #     for j in range(midX):
    #         if c[i,j] != k[i,j]: l.append(max(i,j))

    ck = min(l)

    return 2**(-ck)