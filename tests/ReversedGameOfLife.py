import os
from numpy import *
from GoL_utils import *

def generate_possible_cases():
    """The previous state of an isolated cell is contained in the 3x3 grid"""
    for i in range(2**9):
        # convert i into a binary sequence of 9 bits, corresponding to the 9 grid cells
        possible = array(list(binary_repr(i).zfill(9))).astype(int).reshape([3,3])
        
        alive = possible[1,1]
        AN = aliveNeighbours(possible,1,1)

        if not os.path.isdir("rsrc"):
            os.makedirs("rsrc")
        
        if not os.path.isdir("rsrc/1x1_1"):
            os.makedirs("rsrc/1x1_1")
        if not os.path.isdir("rsrc/1x1_0"):
            os.makedirs("rsrc/1x1_0")

        if alive and AN in [2,3] :
            savetxt(f"rsrc/1x1_1/{grid_to_name(possible)}.npy", possible, fmt="%i")
        elif not alive and AN == 3:
            savetxt(f"rsrc/1x1_1/{grid_to_name(possible)}.npy", possible, fmt="%i")
        elif alive and not AN in [2,3]:
            savetxt(f"rsrc/1x1_0/{grid_to_name(possible)}.npy", possible, fmt="%i")
        elif not alive and AN == 2:
            savetxt(f"rsrc/1x1_0/{grid_to_name(possible)}.npy", possible, fmt="%i")

        
if __name__ == "__main__":
    generate_possible_cases()

        

def run_once(grid):
    sizeX, sizeY = grid.shape
    sizeX += 1; sizeY +=1
    previous_grid = zeros([sizeX, sizeY])

