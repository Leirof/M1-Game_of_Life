
import GameOfLife
from numpy import *
import os
from GoL_utils import *

for i in range(3,50):
    for j in range(i,50):
        for k in range(i*j):
            grid = int_to_grid(k,(i,j))
            # print(f"\n--------------------------------------------------\n")
            print(f"{i}x{j}_{k}")
            # print(grid.astype(int))
            evolution = GameOfLife.start(grid, steps = 1000, verbose = False)
            if not os.path.isdir(f"results/all/{i}x{j}"): os.makedirs(f"results/all/{i}x{j}")
            savez_compressed(f"results/all/{i}x{j}/{grid_to_int(grid)}.npz", evolution)