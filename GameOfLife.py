from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from GoL_utils import *
import time
from numba import jit
from numba.typed import List
import analyze
import utils.archive as archive

#   _    _ _   _ _     
#  | |  | | | (_) |    
#  | |  | | |_ _| |___ 
#  | |  | | __| | / __|
#  | |__| | |_| | \__ \
#   \____/ \__|_|_|___/
                
@jit(nopython=True)
def next_cell(grid, x, y):
    if aliveNeighbours(grid,x,y) == 3:
        return True
    if aliveNeighbours(grid,x,y) == 2:
        return grid[x,y]
    return False

@jit(nopython=True)
def next_grid(grid):
    newGrid = empty_like(grid).astype('bool')
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            newGrid[row,column] = next_cell(grid, row, column)
    return newGrid

# @jit(nopython=True,parallel=True)
def detect_stable_pattern(grid, evolution, i, period=10, verbose = False):
    stable_pattern = False
    for j in range(min(i,period)):
            if (grid == evolution[i-j]).all():
                stable_pattern = True
                if j==0 and verbose: print("\n   -> Stable point reached")
                if j!=0 and verbose: print(f"\n   -> Periodic stable point reached with period {j}")
                return stable_pattern, j
    return stable_pattern, None

#    _____               
#   / ____|              
#  | |     ___  _ __ ___ 
#  | |    / _ \| '__/ _ \
#  | |___| (_) | | |  __/
#   \_____\___/|_|  \___|
                       
# @jit(nopython=True)
def start(grid = random.choice(a=[False, True], size=(10, 10), p=[0.5, 0.5]), steps = 100, verbose = False):
    grid.astype('bool')
    evolution = List()
    evolution.append(grid)
    for i in range(steps-1):
        if verbose and i%10 == 0: print(f"👾 Running Game of Life... Step: {i} / {steps} ({i/steps*100:.0f} %)", end='\r')
        
        newGrid = next_grid(grid)
        evolution.append(newGrid)
        stable, period = detect_stable_pattern(newGrid,evolution,i,verbose=verbose)
        if stable:
            for k in range(10):
                for l in range(period):
                    evolution.append(evolution[l-period])
            return evolution
        
        grid = newGrid
    if verbose: print(f"👾 Running Game of Life... Step: {steps}/{steps} (100 %) ✅")
    return evolution
